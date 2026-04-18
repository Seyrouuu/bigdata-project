# stockage_donnees.py
# Membre 4 - Stockage des données dans MongoDB + Visualisation

from pyspark.sql import SparkSession
import sys
sys.path.insert(0, '/tmp/packages')

from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================
# 1. CONNEXION SPARK
# ============================================
spark = SparkSession.builder.appName("Stockage_Donnees").getOrCreate()

print("="*60)
print("📦 STOCKAGE DES DONNÉES - MEMBRE 4")
print("="*60)

# ============================================
# 2. CONNEXION MONGODB
# ============================================
client = MongoClient('mongodb://mongodb:27017/')
db = client['projet_bigdata']

# ============================================
# 3. STOCKAGE DES DONNÉES NETTOYÉES (MEMBRE 2)
# ============================================
print("\n📖 MEMBRE 2 - Chargement des données nettoyées depuis HDFS...")

try:
    df_clean = spark.read.parquet("hdfs://namenode:8020/user/project/yelp/processed")
    count = df_clean.count()
    print(f"✅ Données trouvées: {count:,} enregistrements")
    
    collection_data = db['membre2_donnees_nettoyees']
    collection_data.delete_many({})
    echantillon = df_clean.limit(1000).toPandas()
    collection_data.insert_many(echantillon.to_dict('records'))
    print(f"✅ {len(echantillon)} enregistrements stockés dans MongoDB")
    
except Exception as e:
    print(f"⚠️ Erreur: {e}")

# ============================================
# 4. STOCKAGE DES MÉTRIQUES (MEMBRE 3)
# ============================================
print("\n📊 MEMBRE 3 - Stockage des métriques...")

metriques = [
    {"modele": "Logistic Regression", "accuracy": 0.884, "f1": 0.883, 
     "precision": 0.883, "recall": 0.884, "rmse": 0.34, "best": True},
    {"modele": "Decision Tree", "accuracy": 0.73, "f1": 0.682, 
     "precision": 0.74, "recall": 0.73, "rmse": 0.52, "best": False},
    {"modele": "Random Forest", "accuracy": 0.682, "f1": 0.566, 
     "precision": 0.769, "recall": 0.682, "rmse": 0.564, "best": False}
]

collection_metriques = db['membre3_metriques']
collection_metriques.delete_many({})
collection_metriques.insert_many(metriques)
print("✅ 3 modèles stockés dans MongoDB")

# ============================================
# 5. STOCKAGE DES INFORMATIONS PROJET
# ============================================
print("\n📋 Stockage des informations du projet...")

info_projet = {
    "nom_projet": "Big Data approach for Predictive Analytics using Machine Learning",
    "date_stockage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "meilleur_modele": "Logistic Regression (88.4%)",
    "pipeline": "Data → HDFS → Spark → ML → Evaluation → MongoDB"
}

collection_info = db['info_projet']
collection_info.delete_many({})
collection_info.insert_one(info_projet)
print("✅ Informations projet stockées")

# ============================================
# 6. GÉNÉRATION DES GRAPHIQUES
# ============================================
print("\n📊 Génération des graphiques...")

modeles = [m["modele"] for m in metriques]
accuracies = [m["accuracy"] for m in metriques]
f1_scores = [m["f1"] for m in metriques]
precisions = [m["precision"] for m in metriques]
recalls = [m["recall"] for m in metriques]
rmse = [m["rmse"] for m in metriques]

plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#2E86AB', '#A23B72', '#F18F01']

# Graphique 1: Accuracy vs F1 Score
fig1, ax1 = plt.subplots(figsize=(10, 6))
x = np.arange(len(modeles))
width = 0.35

ax1.bar(x - width/2, accuracies, width, label='Accuracy', color=colors[0], edgecolor='black')
ax1.bar(x + width/2, f1_scores, width, label='F1 Score', color=colors[1], edgecolor='black')

ax1.set_xlabel('Modèles', fontsize=12)
ax1.set_ylabel('Scores', fontsize=12)
ax1.set_title('Comparaison Accuracy vs F1 Score', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels(modeles, rotation=15)
ax1.legend()
ax1.set_ylim(0, 1)

for i, v in enumerate(accuracies):
    ax1.text(i - width/2, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
for i, v in enumerate(f1_scores):
    ax1.text(i + width/2, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('comparaison_accuracy_f1.png', dpi=300)
print("✅ Graphique 1: comparaison_accuracy_f1.png")

# Graphique 2: Heatmap
fig2, ax2 = plt.subplots(figsize=(10, 6))
data = [accuracies, f1_scores, precisions, recalls]
labels = ['Accuracy', 'F1', 'Precision', 'Recall']

im = ax2.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=1)
ax2.set_xticks(np.arange(len(modeles)))
ax2.set_yticks(np.arange(len(labels)))
ax2.set_xticklabels(modeles, rotation=15)
ax2.set_yticklabels(labels)

for i in range(len(labels)):
    for j in range(len(modeles)):
        ax2.text(j, i, f'{data[i][j]:.3f}', ha='center', va='center', color='black', fontweight='bold')

plt.colorbar(im)
plt.title('Heatmap des Performances', fontsize=14)
plt.tight_layout()
plt.savefig('heatmap_performances.png', dpi=300)
print("✅ Graphique 2: heatmap_performances.png")

# Graphique 3: RMSE
fig3, ax3 = plt.subplots(figsize=(10, 6))
bars = ax3.bar(modeles, rmse, color=colors[2], edgecolor='black')

ax3.set_xlabel('Modèles', fontsize=12)
ax3.set_ylabel('RMSE', fontsize=12)
ax3.set_title('Erreur RMSE (plus bas = meilleur)', fontsize=14)

for bar, val in zip(bars, rmse):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{val:.3f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('comparaison_rmse.png', dpi=300)
print("✅ Graphique 3: comparaison_rmse.png")

# Graphique 4: Radar
fig4, ax4 = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
categories = ['Accuracy', 'F1', 'Precision', 'Recall']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

for i, modele in enumerate(modeles):
    valeurs = [accuracies[i], f1_scores[i], precisions[i], recalls[i]]
    valeurs += valeurs[:1]
    ax4.plot(angles, valeurs, 'o-', linewidth=2, label=modele, color=colors[i])
    ax4.fill(angles, valeurs, alpha=0.1, color=colors[i])

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(categories, fontsize=11)
ax4.set_ylim(0, 1)
ax4.set_title('Diagramme Radar - Comparaison des Modèles', fontsize=14, pad=20)
ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

plt.tight_layout()
plt.savefig('radar_comparison.png', dpi=300)
print("✅ Graphique 4: radar_comparison.png")

# ============================================
# 7. RÉSUMÉ FINAL
# ============================================
best_model = modeles[accuracies.index(max(accuracies))]
print("\n" + "="*60)
print("🎉 STOCKAGE DES DONNÉES TERMINÉ !")
print("="*60)
print(f"🏆 Meilleur modèle: {best_model} (Accuracy: {max(accuracies)*100:.1f}%)")
print("\n💾 MongoDB - Base: projet_bigdata")
print("   ├── membre2_donnees_nettoyees (données nettoyées)")
print("   ├── membre3_metriques (3 modèles avec métriques)")
print("   └── info_projet (métadonnées)")
print("\n📁 Graphiques générés:")
print("   ├── comparaison_accuracy_f1.png")
print("   ├── heatmap_performances.png")
print("   ├── comparaison_rmse.png")
print("   └── radar_comparison.png")
print("="*60)

spark.stop()
