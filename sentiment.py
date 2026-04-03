from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer

spark = SparkSession.builder \
    .appName("SentimentPreprocessing") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

df = spark.read.parquet("hdfs://namenode:8020/user/project/yelp/processed/")

# Indexer les labels
indexer = StringIndexer(inputCol="sentiment", outputCol="label")

# Prétraitement texte
tokenizer = Tokenizer(inputCol="text", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
hashingTF = HashingTF(inputCol="filtered_words", outputCol="rawFeatures", numFeatures=5000)
idf = IDF(inputCol="rawFeatures", outputCol="features")

pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf])
df_features = pipeline.fit(df).transform(df)

# Sauvegarder en Parquet
df_features.select("features", "label").write.mode("overwrite").parquet("sentiment_parquet")

print("✅ Prétraitement terminé et sauvegardé en Parquet")
spark.stop()