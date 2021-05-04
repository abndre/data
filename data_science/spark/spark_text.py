# Import the PySpark module
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
# Import the PySpark module
from pyspark.sql import SparkSession

# Create SparkSession object
spark = SparkSession.builder \
                    .master('local[*]') \
                    .appName('test') \
                    .getOrCreate()

# Specify column names and types
schema = StructType([
    StructField("id", IntegerType()),
    StructField("text", StringType()),
    StructField("label", IntegerType())
])

# Load data from a delimited file
sms = spark.read.csv('sms.csv', sep=';', header=False, schema=schema)

# Print schema of DataFrame
sms.printSchema()
# +---+-------------------------------------------+-----+
# |id |text                                       |label|
# +---+-------------------------------------------+-----+
# |1  |Sorry, I'll call later in meeting          |0    |
# |2  |Dont worry. I guess he's busy.             |0    |
# |3  |Call FREEPHONE 0800 542 0578 now!          |1    |
# |4  |Win a 1000 cash prize or a prize worth 5000|1    |
# +---+-------------------------------------------+-----+

# Import the necessary functions
from pyspark.sql.functions import regexp_replace
from pyspark.ml.feature import Tokenizer

# Remove punctuation (REGEX provided) and numbers
wrangled = sms.withColumn('text', regexp_replace(sms.text, '[_():;,.!?\\-]', ' '))
wrangled = wrangled.withColumn('text', regexp_replace(wrangled.text, '[0-9]', ' '))

# Merge multiple spaces
wrangled = wrangled.withColumn('text', regexp_replace(wrangled.text, ' +', ' '))

# Split the text into words
wrangled = Tokenizer(inputCol='text', outputCol='words').transform(wrangled)

wrangled.show(4, truncate=False)

# script.py> output:
#     +---+----------------------------------+-----+------------------------------------------+
#     |id |text                              |label|words                                     |
#     +---+----------------------------------+-----+------------------------------------------+
#     |1  |Sorry I'll call later in meeting  |0    |[sorry, i'll, call, later, in, meeting]   |
#     |2  |Dont worry I guess he's busy      |0    |[dont, worry, i, guess, he's, busy]       |
#     |3  |Call FREEPHONE now                |1    |[call, freephone, now]                    |
#     |4  |Win a cash prize or a prize worth |1    |[win, a, cash, prize, or, a, prize, worth]|
#     +---+----------------------------------+-----+------------------------------------------+
#     only showing top 4 rows

from pyspark.ml.feature import StopWordsRemover, HashingTF, IDF

# Remove stop words.
wrangled = StopWordsRemover(inputCol='words', outputCol='terms') \
    .transform(sms)

# Apply the hashing trick
wrangled = HashingTF(inputCol='terms', outputCol='hash', numFeatures=1024) \
    .transform(wrangled)

# Convert hashed symbols to TF-IDF
tf_idf = IDF(inputCol='hash', outputCol='features') \
    .fit(wrangled).transform(wrangled)

tf_idf.select('terms', 'features').show(4, truncate=False)

# +--------------------------------+----------------------------------------------------------------------------------------------------+
# |terms                           |features                                                                                            |
# +--------------------------------+----------------------------------------------------------------------------------------------------+
# |[sorry, call, later, meeting]   |(1024,[138,344,378,1006],[2.2391682769656747,2.892706319430574,3.684405173719015,4.244020961654438])|
# |[dont, worry, guess, busy]      |(1024,[53,233,329,858],[4.618714411095849,3.557143394108088,4.618714411095849,4.937168142214383])   |
# |[call, freephone]               |(1024,[138,396],[2.2391682769656747,3.3843005812686773])                                            |
# |[win, cash, prize, prize, worth]|(1024,[31,69,387,428],[3.7897656893768414,7.284881949239966,4.4671645129686475,3.898659777615979])  |
# +--------------------------------+----------------------------------------------------------------------------------------------------+
# only showing top 4 rows


# training a spam classifier

# Split the data into training and testing sets
sms_train, sms_test = sms.randomSplit([0.8, 0.2], seed=13)

# Fit a Logistic Regression model to the training data
logistic = LogisticRegression(regParam=0.2).fit(sms_train)

# Make predictions on the testing data
prediction = logistic.transform(sms_test)

# Create a confusion matrix, comparing predictions to known labels
prediction.groupBy('label', 'prediction').count().show()

# +-----+----------+-----+
# |label|prediction|count|
# +-----+----------+-----+
# |    1|       0.0|   47|
# |    0|       0.0|  987|
# |    1|       1.0|  124|
# |    0|       1.0|    3|
# +-----+----------+-----+