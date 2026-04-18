
# Member 4 – NoSQL Storage + Visualization + Report

## 1. Objective
🎯 **Objectif :** Stocker les résultats du preprocessing (Membre 2) et du Machine Learning (Membre 3) dans MongoDB, générer des visualisations et produire le rapport d'architecture.

---

## 2. Environnement utilisé

| Outil | Rôle |
|-------|------|
| MongoDB | Base de données NoSQL pour le stockage des résultats |
| PyMongo | Bibliothèque Python pour connecter Spark à MongoDB |
| Matplotlib | Bibliothèque pour générer les graphiques |
| Apache Spark | Lecture des données nettoyées depuis HDFS |
| Docker | Conteneurisation de l'environnement |

---

## 3. Étapes réalisées

### Étape 1 : Connexion à MongoDB
```python
from pymongo import MongoClient
client = MongoClient('mongodb://mongodb:27017/')
db = client['projet_bigdata']
```

### Étape 2 : Lecture des données nettoyées depuis HDFS (Membre 2)
```python
df_clean = spark.read.parquet("hdfs://namenode:8020/user/project/yelp/processed")
count = df_clean.count()  # 100,000 enregistrements
echantillon = df_clean.limit(1000).toPandas()
```

### Étape 3 : Stockage des données nettoyées dans MongoDB
```python
collection_data = db['membre2_donnees_nettoyees']
collection_data.delete_many({})
collection_data.insert_many(echantillon.to_dict('records'))
# ✅ 1,000 documents stockés
```

### Étape 4 : Stockage des métriques des modèles (Membre 3)
```python
metriques = [
    {"modele": "Logistic Regression", "accuracy": 0.884, "f1": 0.883, 
     "precision": 0.883, "recall": 0.884, "rmse": 0.34, "best": True},
    {"modele": "Decision Tree", "accuracy": 0.73, "f1": 0.682, 
     "precision": 0.74, "recall": 0.73, "rmse": 0.52, "best": False},
    {"modele": "Random Forest", "accuracy": 0.682, "f1": 0.566, 
     "precision": 0.769, "recall": 0.682, "rmse": 0.564, "best": False}
]
db.membre3_metriques.insert_many(metriques)
# ✅ 3 modèles stockés
```

### Étape 5 : Stockage des informations du projet
```python
info_projet = {
    "nom_projet": "Big Data approach for Predictive Analytics using Machine Learning",
    "date_stockage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "meilleur_modele": "Logistic Regression (88.4%)",
    "pipeline": "Data → HDFS → Spark → ML → Evaluation → MongoDB"
}
db.info_projet.insert_one(info_projet)
```

### Étape 6 : Génération des graphiques

#### Graphique 1 : Accuracy vs F1 Score
```python
plt.bar(x - width/2, accuracies, width, label='Accuracy', color='blue')
plt.bar(x + width/2, f1_scores, width, label='F1 Score', color='orange')
plt.savefig('comparaison_accuracy_f1.png')
```

#### Graphique 2 : Heatmap des performances
```python
plt.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=1)
plt.savefig('heatmap_performances.png')
```

#### Graphique 3 : Comparaison RMSE
```python
plt.bar(modeles, rmse, color='red')
plt.savefig('comparaison_rmse.png')
```

#### Graphique 4 : Diagramme radar
```python
# Comparaison des 4 métriques (Accuracy, F1, Precision, Recall)
plt.savefig('radar_comparison.png')
```

---

## 4. Résultats obtenus

### 4.1 Collections MongoDB créées

| Collection | Contenu | Nombre de documents |
|------------|---------|---------------------|
| `membre2_donnees_nettoyees` | Données nettoyées (review_id, stars, sentiment, clean_text) | 1,000 |
| `membre3_metriques` | Métriques des 3 modèles | 3 |
| `info_projet` | Métadonnées du projet | 1 |

### 4.2 Tableau comparatif des modèles

| Modèle | Accuracy | F1 | Precision | Recall | RMSE |
|--------|----------|-----|-----------|--------|------|
| **Logistic Regression** | **0.884** | **0.883** | 0.883 | 0.884 | 0.34 |
| Decision Tree | 0.73 | 0.682 | 0.74 | 0.73 | 0.52 |
| Random Forest | 0.682 | 0.566 | 0.769 | 0.682 | 0.564 |

**🏆 Meilleur modèle : Logistic Regression (88.4%)**

### 4.3 Graphiques générés

| Fichier | Description |
|---------|-------------|
| `comparaison_accuracy_f1.png` | Comparaison Accuracy vs F1 Score |
| `heatmap_performances.png` | Heatmap des performances |
| `comparaison_rmse.png` | Erreur RMSE par modèle |
| `radar_comparison.png` | Diagramme radar des métriques |

### 4.4 Vérification dans MongoDB

```javascript
> use projet_bigdata
> show collections
membre2_donnees_nettoyees
membre3_metriques
info_projet

> db.membre3_metriques.find().pretty()
{
    modele: 'Logistic Regression',
    accuracy: 0.884,
    f1: 0.883,
    precision: 0.883,
    recall: 0.884,
    rmse: 0.34,
    best: true
}
...
```

---

## 5. Comment reproduire (Membre 4)

```bash
# 1. Démarrer l'environnement
docker-compose up -d

# 2. Entrer dans le conteneur Spark
docker exec -it spark-master bash

# 3. Installer les dépendances
pip install --target=/tmp/packages pymongo matplotlib pandas

# 4. Exécuter le script de stockage
export PYTHONPATH=/tmp/packages:$PYTHONPATH
/opt/spark/bin/spark-submit stockage_donnees.py

# 5. Vérifier MongoDB
docker exec -it mongodb mongosh
use projet_bigdata
show collections
db.membre3_metriques.find().pretty()
```

---

## 6. Structure des fichiers (Membre 4)

```
bigdata-project/
│
├── stockage_donnees.py          # Script principal de stockage
├── README_stockage.md           # Documentation (ce fichier)
├── comparaison_accuracy_f1.png  # Graphique 1
├── heatmap_performances.png     # Graphique 2
├── comparaison_rmse.png         # Graphique 3
├── radar_comparison.png         # Graphique 4
└── Architecture_Report.pdf      # Rapport final (2 pages)
```

---

## 7. Deliverables (Membre 4)

- ✅ Script `stockage_donnees.py` (code commenté)
- ✅ Documentation `README_stockage.md`
- ✅ 4 graphiques de visualisation (PNG)
- ✅ Rapport d'architecture (2 pages PDF)
- ✅ Données stockées dans MongoDB (collections vérifiables)


