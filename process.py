from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lower, regexp_replace

# ============================================
# 1. Initialize Spark Session with memory settings
# ============================================
spark = SparkSession.builder \
    .appName("YelpPreprocessing_Basic") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "20") \
    .getOrCreate()

# ============================================
# 2. Read raw data from HDFS
# ============================================
input_path = "hdfs://namenode:8020/user/project/yelp/review.json"
df = spark.read.json(input_path)

print("✅ Data loaded successfully. Total records:", df.count())
df.printSchema()

# ============================================
# 3. Select relevant columns
# ============================================
df_selected = df.select("review_id", "user_id", "stars", "text")

# ============================================
# 4. Create sentiment column based on stars
# ============================================
df_sentiment = df_selected.withColumn("sentiment",
    when(col("stars") >= 4, "positive")
    .when(col("stars") == 3, "neutral")
    .otherwise("negative"))

# ============================================
# 5. Basic text cleaning
#    - Convert to lowercase
#    - Remove non-alphabetic characters (keep letters and spaces)
# ============================================
df_clean = df_sentiment.withColumn("clean_text",
    lower(regexp_replace(col("text"), "[^a-zA-Z\\s]", "")))

# ============================================
# 6. Preliminary statistics (for documentation)
# ============================================
print("\n=== Sentiment distribution ===")
df_clean.groupBy("sentiment").count().show()

print("\n=== Stars distribution ===")
df_clean.groupBy("stars").count().orderBy("stars").show()

print("\n=== Sample of processed data (10 rows) ===")
df_clean.select("stars", "sentiment", "clean_text").show(10, truncate=60)

# ============================================
# 7. Save processed data to HDFS (Parquet format)
# ============================================
output_path = "hdfs://namenode:8020/user/project/yelp/processed"
df_clean.write.mode("overwrite").parquet(output_path)

print(f"\n✅ Processing completed. Clean data saved to: {output_path}")

# ============================================
# 8. Stop Spark session
# ============================================
spark.stop()