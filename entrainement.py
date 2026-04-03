# train_models.py
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, RegressionEvaluator

import os

# =========================
# Créer SparkSession
# =========================
spark = SparkSession.builder \
    .appName("bigdata - Membre3") \
    .getOrCreate()

# =========================
# Lire le dataset parquet
# =========================
df = spark.read.parquet("sentiment_parquet")
print("Aperçu des données :")
df.show(5)

# =========================
# Train / Test split
# =========================
train_df, test_df = df_sample.randomSplit([0.8, 0.2], seed=42)

# =========================
# Définir les modèles
# =========================
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20)
dt = DecisionTreeClassifier(featuresCol="features", labelCol="label", maxDepth=5)
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=20, maxDepth=5)

# =========================
# Entraînement
# =========================
print("Entraînement Logistic Regression...")
lr_model = lr.fit(train_df)
lr_pred = lr_model.transform(test_df)
print("✅ LR terminé")

print("Entraînement Decision Tree...")
dt_model = dt.fit(train_df)
dt_pred = dt_model.transform(test_df)
print("✅ DT terminé")

print("Entraînement Random Forest...")
rf_model = rf.fit(train_df)
rf_pred = rf_model.transform(test_df)
print("✅ RF terminé")

# =========================
# Évaluation sur 5 métriques
# =========================
acc_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
f1_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
recall_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")
precision_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
rmse_eval = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")

metrics = []
for name, pred in [("Logistic Regression", lr_pred), ("Decision Tree", dt_pred), ("Random Forest", rf_pred)]:
    metrics.append({
        "Model": name,
        "Accuracy": round(acc_eval.evaluate(pred), 3),
        "F1": round(f1_eval.evaluate(pred), 3),
        "Recall": round(recall_eval.evaluate(pred), 3),
        "Precision": round(precision_eval.evaluate(pred), 3),
        "RMSE": round(rmse_eval.evaluate(pred), 3)
    })

print("\n=== Tableau comparatif des modèles ===")
for m in metrics:
    print(m)
# =========================
# Choisir le meilleur modèle (selon Accuracy)
# =========================
best_model_name = max(metrics, key=lambda x: x['Accuracy'])['Model']
print(f"\nMeilleur modèle : {best_model_name}")

if best_model_name == "Logistic Regression":
    best_model = lr_model
elif best_model_name == "Decision Tree":
    best_model = dt_model
else:
    best_model = rf_model

# =========================
# Sauvegarde du meilleur modèle
# =========================
tmp_model_path = "/tmp/best_model"
best_model.write().overwrite().save(tmp_model_path)
print(f"Meilleur modèle sauvegardé dans {tmp_model_path}")

# =========================
# Sauvegarde du parquet 
# =========================
tmp_parquet_path = "/tmp/sentiment_parquet_copy"
df.write.mode("overwrite").parquet(tmp_parquet_path)
print(f"Parquet sauvegardé dans {tmp_parquet_path}")

# =========================
# Fin
# =========================
print("✅ Script terminé !")

# =========================
# Stop Spark
# =========================
spark.stop()