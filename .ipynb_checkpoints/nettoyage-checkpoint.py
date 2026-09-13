import pandas as pd

# 1. Chargement et premier diagnostic
df = pd.read_csv("data.csv")
print("Dimensions brutes : ", df.shape)
print(df.info())
print("Doublons détectés : ", df.duplicated().sum())
print("Valeurs manquantes par colonne : \n", df.isnull().sum())

# 2. Suppression des doublons
df = df.drop_duplicates()

# 3. Uniformisation du texte (colonne ville)
df["ville"] = df["ville"].str.strip().str.title()

# 4. Traitement des valeurs manquantes 
median_age = df["age"].median()
df["age"] = df["age"].fillna(median_age)
df["ville"] = df["ville"].fillna("Inconnue")
df["derniere_commande"] = df["derniere_commande"].fillna("Jamais")

# 5. Conversion des types de dates
df["date_inscription"] = pd.to_datetime(df["date_inscription"])
df["derniere_commande"] = pd.to_datetime(df["derniere_commande"], errors="coerce")

# 6. Export du fichier nettoyé
df.to_csv("data_clean.csv", index=False)
print("Dimensions finales :", df.shape)

# Chargement des données nettoyées
df = pd.read_csv("data_clean.csv")
df["segment"] = pd.cut(
        df["montant_total"],
        bins=[0,200,500, float("inf")],
        labels=["Faible", "Moyen","Fort"]
)
print(df["segment"].value_counts())

# Clients inactifs depuis plus de 300 jours
df["derniere_commande"] = pd.to_datetime(
    df["derniere_commande"],
    errors="coerce"
)
reference = pd.Timestamp("2026-09-01")
df["jours_inactivite"] = (reference - df["derniere_commande"]).dt.days
inactifs = df[df["jours_inactivite"] > 300]
pct = len(inactifs)/len(df) * 100
print(f"Clients inatifs : {len(inactifs)} sur {len(df)} {pct:.1f}%")

# Graphique pour le portfolio
import matplotlib.pyplot as plt

df["segment"].value_counts().plot(
    kind="bar", title="Répartition des clients par segment de valeur"
)

plt.savefig("segmentation_clients.png", dpi=150, bbox_inches="tight")