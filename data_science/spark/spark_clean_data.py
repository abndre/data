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

# Terminate the cluster
spark.stop()
