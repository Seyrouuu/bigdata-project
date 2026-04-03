# Member 3 – Feature Engineering (TF-IDF)+ Model Training (Yelp Sentiment Analysis)


## 1. Objective
🎯 Objectif

Ce projet consiste à :

Prétraiter les données Yelp (texte → features)
Transformer les données avec TF-IDF
Entraîner plusieurs modèles Machine Learning
Comparer leurs performances
Sauvegarder le meilleur modèle
## ⚙️ Environnement
Apache Spark (PySpark)
Hadoop (HDFS)
Docker
MLlib (Machine Learning)
📂 Source des données

Dataset chargé depuis HDFS :
```bash
hdfs://namenode:8020/user/project/yelp/processed/
```
Contient :

text → texte du commentaire
sentiment → (positive / neutral / negative)

🔹 PARTIE 1 : PRÉTRAITEMENT (Feature Engineering)
📌 Étapes réalisées
## 1. Chargement des données
```bash
df = spark.read.parquet("hdfs://namenode:8020/user/project/yelp/processed/")
```
## 2. Transformation du label
```bash
StringIndexer(inputCol="sentiment", outputCol="label")
```
👉 Convertit :

positive → 1
neutral → 2
negative → 0
## 3. Tokenization (👉 Découpe le texte en mots)
```bash
Tokenizer(inputCol="text", outputCol="words")
```

## 4. Suppression des stop words (👉 Supprime les mots inutiles (the, is, …)
```bash
StopWordsRemover(inputCol="words", outputCol="filtered_words")
```

## 5. Vectorisation (TF-IDF) 👉 Transformation texte → vecteurs numériques
```bash
HashingTF(numFeatures=5000)
IDF()
```


## 6. Pipeline complet
```bash
pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf])
```
## 7. Résultat final
```bash
df_features.select("features", "label").write.parquet("sentiment_parquet")
```

## 📁 Output : sentiment_parquet


🔹 PARTIE 2 : ENTRAÎNEMENT DES MODÈLES
## 1. Chargement des données
```bash
df = spark.read.parquet("sentiment_parquet")
```
## 2. train/test
```bash
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
```
##  Modèles utilisés
 Modèles utilisés
1. Logistic Regression
```bash
LogisticRegression(maxIter=20)
```
3. Decision Tree
```bash
DecisionTreeClassifier(maxDepth=5)
```
5. Random Forest
```bash
RandomForestClassifier(numTrees=20)
```
##  Évaluation des modèles

Métriques utilisées :

Accuracy
F1-score
Recall
Precision
RMSE
## Les resultats

| Model               | Accuracy | F1   | Recall | Precision | RMSE |
| ------------------- | -------- | ---- | ------ | --------- | ---- |
| Logistic Regression | 0.884    | 0.883| 0.884  | 0.883     | 0.34 |
| Decision Tree       | 0.73     | 0.682| 0.73   | 0.74      | 0.52 |
| Random Forest       | 0.682    | 0.566| 0.682  | 0.769     | 0.564|

## 🏆 Sélection du meilleur modèle
best_model_name = max(metrics, key=lambda x: x['Accuracy'])['Model']

👉 Meilleur modèle = Logistic Regression
# Sauvegarde du meilleur modèle
# =========================
```bash
tmp_model_path = "/tmp/best_model"
best_model.write().overwrite().save(tmp_model_path)
print(f"Meilleur modèle sauvegardé dans {tmp_model_path}")
```
# =========================
# Sauvegarde du parquet 
# =========================
```bash
tmp_parquet_path = "/tmp/sentiment_parquet_copy"
df.write.mode("overwrite").parquet(tmp_parquet_path)
print(f"Parquet sauvegardé dans {tmp_parquet_path}")
```
