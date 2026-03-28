# Member 2 – Data Preprocessing (Yelp Sentiment Analysis)

## 1. Objective
Prepare Yelp reviews for sentiment classification by:
- Reading raw JSON data from HDFS.
- Adding a sentiment column based on star ratings.
- Basic text cleaning (lowercase, remove non‑alphabetic characters).
- Saving the processed data to HDFS in Parquet format.

## 2. Tools & Environment
- PySpark (Spark 3.5.0)
- HDFS (Hadoop 3.2.1)
- Docker containers: namenode, datanode, spark-master, spark-worker, mongodb

## 3. Processing Steps

### 3.1 Read raw data
- Source: hdfs://namenode:8020/user/project/yelp/review.json
- Total records: 6,990,280 reviews

### 3.2 Column selection
Kept only relevant columns: eview_id, user_id, stars, 	ext

### 3.3 Create sentiment column
- stars >= 4 → positive
- stars == 3 → 
eutral
- stars <= 2 → 
egative

### 3.4 Basic text cleaning
- Convert to lowercase
- Remove all non‑alphabetic characters (keep letters and spaces)

### 3.5 Save processed data
- Format: **Parquet** (Snappy compression)
- Path: hdfs://namenode:8020/user/project/yelp/processed
- Columns available: eview_id, user_id, stars, 	ext, sentiment, clean_text

## 4. Results (Statistics)

| Sentiment | Count    |
|-----------|----------|
| positive  | 4,684,545|
| neutral   | 691,934  |
| negative  | 1,613,801|

| Stars | Count    |
|-------|----------|
| 1.0   | 1,069,561|
| 2.0   | 544,240  |
| 3.0   | 691,934  |
| 4.0   | 1,452,918|
| 5.0   | 3,231,627|

**Sample of cleaned data (first 10 rows):**
+-----+---------+------------------------------------------------------------+
|stars|sentiment|clean_text |
+-----+---------+------------------------------------------------------------+
| 3.0|neutral |if you decide to eat here just be aware it is going to ta...|
| 5.0|positive |ive taken a lot of spin classes over the years and nothin...|
| 3.0|neutral |family diner had the buffet eclectic assortment a large c...|
| 5.0|positive |wow yummy different delicious our favorite is the lam...|
| 4.0|positive |cute interior and owner gave us tour of upcoming patioro...|
| 1.0|negative |i am a long term frequent customer of this establishment ...|
| 5.0|positive |loved this tour i grabbed a groupon and the price was gre...|
| 5.0|positive |amazingly amazing wings and homemade bleu cheese had the ...|
| 3.0|neutral |this easter instead of going to lopez lake we went to los...|
| 3.0|neutral |had a party of here for hibachi our waitress brought our...|
+-----+---------+------------------------------------------------------------+

## 5. How to Access the Processed Data

In PySpark (after starting the containers):
`python
df = spark.read.parquet("hdfs://namenode:8020/user/project/yelp/processed")
df.printSchema()
df.show(5)
6. How to Reproduce the Preprocessing (Optional)
bash
docker cp process.py spark-master:/opt/spark/
docker exec -it spark-master bash
cd /opt/spark
spark-submit process.py
7. Notes for Other Team Members
Member 3 (Model Training): Use the sentiment column as label and clean_text as feature. You can improve results with additional NLP (stopwords, stemming, TF‑IDF).

Member 4 (NoSQL Storage): The processed data is ready to be written to MongoDB using the Mongo Spark Connector if needed.

Date: 28 March 2026
Member 2
