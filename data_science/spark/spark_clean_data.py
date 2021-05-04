# Import the PySpark module
from pyspark.sql import SparkSession

# Create SparkSession object
spark = SparkSession.builder \
                    .master('local[*]') \
                    .appName('test') \
                    .getOrCreate()

# What version of Spark?
# (Might be different to what you saw in the presentation!)
print(spark.version)

# Read data from CSV file
flights = spark.read.csv('flights.csv',
                         sep=',',
                         header=True,
                         inferSchema=True,
                         nullValue='NA')

# Get number of records
print("The data contain %d records." % flights.count())

# View the first five records
flights.show(5)

# +---+---+---+-------+------+---+----+------+--------+-----+
# |mon|dom|dow|carrier|flight|org|mile|depart|duration|delay|
# +---+---+---+-------+------+---+----+------+--------+-----+
# | 11| 20|  6|     US|    19|JFK|2153|  9.48|     351| null|
# |  0| 22|  2|     UA|  1107|ORD| 316| 16.33|      82|   30|
# +---+---+---+-------+------+---+----+------+--------+-----+
# only showing top 2 rows

# Check column data types
print(flights.dtypes)

# Removendo dados

# Remove the 'flight' column
flights_drop_column = flights.drop('flight')

# Number of records with missing 'delay' values
flights_drop_column.filter('delay IS NULL').count()

# Remove records with missing 'delay' values
flights_valid_delay = flights_drop_column.filter('delay IS NOT NULL')

# Remove records with missing values in any column and get the number of remaining rows
flights_none_missing = flights_valid_delay.dropna()
print(flights_none_missing.count())

# criando colunas

# Import the required function
from pyspark.sql.functions import round

# Convert 'mile' to 'km' and drop 'mile' column
flights_km = flights.withColumn('km', round(flights.mile * 1.60934, 0)) \
                    .drop('mile')

# Create 'label' column indicating whether flight delayed (1) or not (0)
flights_km = flights_km.withColumn('label', (flights.delay >=15).cast('integer'))

# Check first five records
flights_km.show(5)

# +---+---+---+-------+---+------+--------+-----+------+-----+
# | mon | dom | dow | carrier | org | depart | duration | delay | km | label |
# +---+---+---+-------+---+------+--------+-----+------+-----+
# | 0 | 22 | 2 | UA | ORD | 16.33 | 82 | 30 | 509.0 | 1 |
# | 2 | 20 | 4 | UA | SFO | 6.17 | 82 | -8 | 542.0 | 0 |
# | 9 | 13 | 1 | AA | ORD | 10.33 | 195 | -5 | 1989.0 | 0 |
# | 5 | 2 | 1 | UA | SFO | 7.98 | 102 | 2 | 885.0 | 0 |
# | 7 | 2 | 6 | AA | ORD | 10.83 | 135 | 54 | 1180.0 | 1 |
# +---+---+---+-------+---+------+--------+-----+------+-----+


# assembler vector

# Import the necessary class
from pyspark.ml.feature import VectorAssembler

# Create an assembler object
assembler = VectorAssembler(inputCols=[
    'mon', 'dom', 'dow', 'carrier_idx', 'org_idx', 'km', 'depart', 'duration'
], outputCol='features')

# Consolidate predictor columns
flights_assembled = assembler.transform(flights)

# Check the resulting column
flights_assembled.select('features', 'delay').show(5, truncate=False)

# quebrando o modelo

# Split into training and testing sets in a 80:20 ratio
flights_train, flights_test = flights.randomSplit([0.8,0.2], seed=23)

# Check that training set has around 80% of records
training_ratio = flights_train.count() / flights_test.count()
print(training_ratio)

# treinando o modelo

# Import the Decision Tree Classifier class
from pyspark.ml.classification import DecisionTreeClassifier

# Create a classifier object and fit to the training data
tree = DecisionTreeClassifier()
tree_model = tree.fit(flights_train)

# Create predictions for the testing data and take a look at the predictions
prediction = tree_model.transform(flights_test)
prediction.select('label', 'prediction', 'probability').show(5, False)

# +-----+----------+----------------------------------------+
# | label | prediction | probability |
# +-----+----------+----------------------------------------+
# | 1 | 1.0 | [0.2911010558069382, 0.7088989441930619] |
# | 1 | 1.0 | [0.3875, 0.6125] |
# | 1 | 1.0 | [0.3875, 0.6125] |
# | 0 | 0.0 | [0.6337448559670782, 0.3662551440329218] |
# | 0 | 0.0 | [0.9368421052631579, 0.06315789473684211] |
# +-----+----------+----------------------------------------+

# matriz de confusao

# Create a confusion matrix
prediction.groupBy('label', 'prediction').count().show()

# Calculate the elements of the confusion matrix
TN = prediction.filter('prediction = 0 AND label = prediction').count()
TP = prediction.filter('prediction = 1 AND label = prediction').count()
FN = prediction.filter('prediction = 0 AND label != prediction').count()
FP = prediction.filter('prediction = 1 AND label != prediction').count()

# Accuracy measures the proportion of correct predictions
accuracy = (TN + TP) / (TN + TP + FN + FP)
print(accuracy)

# +-----+----------+-----+
# | label | prediction | count |
# +-----+----------+-----+
# | 1 | 0.0 | 154 |
# | 0 | 0.0 | 289 |
# | 1 | 1.0 | 328 |
# | 0 | 1.0 | 190 |
# +-----+----------+-----+
#
# 0.6420395421436004


# logistic regression

# Import the logistic regression class
from pyspark.ml.classification import LogisticRegression

# Create a classifier object and train on training data
logistic = LogisticRegression().fit(flights_train)

# Create predictions for the testing data and show confusion matrix
prediction = logistic.transform(flights_test)
prediction.groupBy('label', 'prediction').count().show()

# Evaluate the logistic

from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# Calculate precision and recall
precision = TP / (TP + FP)
recall = TP / (TP + FN)
print('precision = {:.2f}\nrecall    = {:.2f}'.format(precision, recall))

# Find weighted precision
multi_evaluator = MulticlassClassificationEvaluator()
weighted_precision = multi_evaluator.evaluate(prediction, {multi_evaluator.metricName: "weightedPrecision"})

# Find AUC
binary_evaluator = BinaryClassificationEvaluator()
auc = binary_evaluator.evaluate(prediction, {binary_evaluator.metricName: "areaUnderROC"})

# Terminate the cluster
spark.stop()
