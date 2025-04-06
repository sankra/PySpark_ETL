#importing required modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, lit
import boto3
from sqlalchemy import create_engine

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("S3_to_RDS_ETL") \
    .config("spark.jars", "/path/to/mysql-connector-java-8.0.33.jar") \  # Update JDBC driver path. Without this, Spark cannot connect to MySQL (AWS RDS) via JDBC.
    .getOrCreate()

# S3 Configurations
s3_bucket = "your-s3-bucket-name"
s3_file_path = "s3a://" + s3_bucket + "/data/input_data.csv"


# Read Data from S3 (CSV format)
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(s3_file_path)

print("Original DataFrame:")
df.show()

# 🔹 Data Transformation
df_transformed = df \
    .withColumnRenamed("old_column_name", "new_column_name") \  # Rename column
    .withColumn("processed_date", current_date()) \  # Add new column with current date
    .filter(col("value") > 1000)  # Filter records where 'value' > 1000

print("Transformed DataFrame:")
df_transformed.show()

# Load Data into AWS RDS (MySQL/PostgreSQL)
rds_host = "your-rds-endpoint"
rds_port = "3306"  # MySQL (Use 5432 for PostgreSQL)
rds_dbname = "your_database"
rds_user = "your_username"
rds_password = "your_password"


jdbc_url = f"jdbc:mysql://{rds_host}:{rds_port}/{rds_dbname}"
properties = {
    "user": rds_user,
    "password": rds_password,
    "driver": "com.mysql.cj.jdbc.Driver"
}


# Write DataFrame to RDS Table
df_transformed.write \
    .jdbc(url=jdbc_url, table="your_table_name", mode="append", properties=properties)

print("Data successfully loaded into AWS RDS!")

# Stop Spark Session
spark.stop()
