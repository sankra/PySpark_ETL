from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, when

# Step 1: Initialize Spark Session
spark = SparkSession.builder.appName("DataTransformationExample").getOrCreate()

# Step 2: Create a Sample DataFrame
data = [
    ("Alice", "HR", 5000),
    ("Bob", "IT", 7000),
    ("Charlie", "IT", 6000),
    ("David", "Finance", 6500),
    ("Eve", "HR", 4800)
    ("Frank", "Finance", 7200),
    ("Grace", "IT", 5500),
    ("Heidi", "HR", 4900),
    ("Ivan", "Finance", 8000),
    ("Judy", "IT", 6200)
]
columns = ["Name", "Department", "Salary"]

#creating a dataframe
df = spark.createDataFrame(data, columns)




# Step 3: Data Transformations
df_transformed = (
    df.withColumn("Department", upper(col("Department")))  # Convert department names to uppercase
      .withColumn("Salary Category", when(col("Salary") > 6000, "High").otherwise("Medium"))  # Categorize salaries
      .filter(col("Salary") >= 5000)  # Filter employees with salary >= 5000
      .groupBy("Department")  # Group by Department
      .avg("Salary")  # Calculate average salary per department
      .withColumnRenamed("avg(Salary)", "Avg_Salary")  # Rename column
        .orderBy("Department")  # Order by Department

)

#printing original data frame
print("Original DataFrame Values:")
df.show()

#printing the transformed Dataframe
print("Transformed DataFrame:")
df_transformed.show()


# Stop Spark Session
spark.stop()


'''
Output

+-------+----------+------+
|   Name|Department|Salary|
+-------+----------+------+
|  Alice|       HR|  5000|
|    Bob|       IT|  7000|
|Charlie|       IT|  6000|
|  David|  Finance|  6500|
|    Eve|       HR|  4800|
+-------+----------+------+

+----------+----------+
|Department|Avg_Salary|
+----------+----------+
|      IT  |   6500.0 |
|      HR  |   5000.0 |
|  FINANCE |   6500.0 |
+----------+----------+
'''
