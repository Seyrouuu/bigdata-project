# 🚀 Big Data Project - Infrastructure Setup

## 📌 Project Overview

This project implements a **Big Data pipeline** using:

* Docker (Environment)
* Hadoop HDFS (Storage)
* Apache Spark (Processing)
* MongoDB (NoSQL Database)

The goal is to build an **end-to-end system** from raw data to analysis and machine learning.

> This project is designed to be easily reproducible using Docker.

---

## ⚙️ Requirements

Make sure you have installed:

* Docker Desktop
* Git (optional)
* Anaconda (for PySpark users)

---

## 🐳 Step 1: Clone the Project

```bash
git clone https://github.com/Seyrouuu/bigdata-project.git
cd bigdata-project
```

---

## ▶️ Step 2: Start the Environment

```bash
docker-compose up -d
```

---

## 🔍 Step 3: Verify Containers

```bash
docker ps
```

You should see:

* namenode
* datanode
* spark
* mongodb

---

## 🌐 Step 4: Access Web Interfaces

* Hadoop UI: http://localhost:9870
* Spark UI: http://localhost:8080

---

## 📂 Step 5: Upload Yelp Dataset to HDFS

### 1. Copy dataset from your machine to container

```bash
docker cp "path/to/yelp_dataset_review.json" namenode:/review.json
```

---

### 2. Upload file to HDFS

```bash
docker exec -it namenode hdfs dfs -mkdir -p /user/dell/
docker exec -it namenode hdfs dfs -put /review.json /user/dell/
```

---

### 3. Verify upload

```bash
docker exec -it namenode hdfs dfs -ls /user/dell/
```

You should see:

```
/user/dell/review.json
```

---

## 🔗 Connection Information

* HDFS:

```
hdfs://namenode:8020/user/dell/review.json
```

* Spark Master:

```
spark://spark:7077
```

* MongoDB:

```
mongodb://mongodb:27017
```

---

## 👥 Team Usage

Each member should:

1. Clone the project
2. Run environment:

```bash
docker-compose up -d
```

3. Use the same configuration
4. Access data from HDFS

---

## 🧪 Notes

* Make sure all containers are running before coding
* Do not change ports or container names
* Use the same dataset path
* First test with small dataset, then big dataset

---

## 📦 Project Structure

```
bigdata-project/
│
├── docker-compose.yml
├── README.md

```

---

## ✅ Deliverables (Member 1)

* Docker environment working
* HDFS configured
* Yelp dataset uploaded
* README documentation

---




