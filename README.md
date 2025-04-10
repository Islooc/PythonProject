# 📊 Application Radar KPI Supply Chain (Tkinter + API + Matplotlib)

Cette application permet de **récupérer des KPI logistiques depuis une API**, de les **normaliser** et de les afficher dans un **radar chart interactif** à l’aide de **Tkinter** et **Matplotlib**.

---

## 🚀 Fonctionnalités

- Interface utilisateur simple avec **Tkinter**
- Récupération des données KPI depuis une API REST
- Normalisation des valeurs (selon seuils par défaut)
- Traduction automatique des noms de KPI en français
- Génération d’un **graphe radar superposé** (moyenne vs. maximum)
- Visualisation intuitive des performances logistiques

---

## 📦 Technologies utilisées

- Python 3.x
- Tkinter (interface graphique)
- `requests` (requêtes API)
- `matplotlib`, `numpy` (graphiques radar)
- `collections.defaultdict` (regroupement des KPI)

---

## 📈 Exemple de KPI supportés

| KPI (EN)                    | Traduction FR                    |
|-----------------------------|----------------------------------|
| Lead Time                   | Délai d'exécution                |
| Order Fulfillment Rate      | Taux de satisfaction des commandes |
| Inventory Turnover          | Rotation des stocks              |
| Perfect Order Rate          | Taux de commandes parfaites      |
| ISR (Stock/Ventes)          | Ratio stock/ventes               |
| On-time Delivery Rate       | Livraisons à l'heure             |
| Transportation Cost per Ton | Coût transport/tonne             |
| DSI (jours)                 | Durée rotation des stocks        |
| Supplier Lead Time          | Délai fournisseurs               |

---

## 📊 Exemple d’affichage

- **Courbe bleue** : Moyenne des valeurs
- **Courbe rouge** : Valeurs maximales
- **Zone verte** : Zone de progrès possible entre moyenne et max
- Étiquettes traduites automatiquement en français
- Valeurs numériques affichées au bord du radar

---

## 🔧 Comment utiliser le projet

1. Cloner ou télécharger le projet
2. Installer les dépendances :

```bash
pip install requests matplotlib
