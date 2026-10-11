
import pandas as pd
import matplotlib.pyplot as plt

# 1. Charger et préparer les données
df = pd.read_csv("ventes.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 2. Calculer le chiffre d'affaires
df["Chiffre_Affaires"] = df["Quantite"] * df["Prix_Unitaire"]

# 3. Calculer les KPI globaux
chiffre_affaires_total = df["Chiffre_Affaires"].sum()
quantite_totale = df["Quantite"].sum()
nombre_ventes = len(df)

print("=== INDICATEURS CLÉS ===")
print(f"Chiffre d'affaires total : {chiffre_affaires_total:,.0f}")
print(f"Quantité totale vendue : {quantite_totale}")
print(f"Nombre de lignes de vente : {nombre_ventes}")

# 4. Chiffre d'affaires par produit
ca_produit = (
    df.groupby("Produit")["Chiffre_Affaires"]
    .sum()
    .sort_values(ascending=False)
)

print("\n=== CHIFFRE D'AFFAIRES PAR PRODUIT ===")
print(ca_produit)

# 5. Chiffre d'affaires par mois
df["Mois"] = df["Date"].dt.to_period("M").astype(str)
ca_mois = df.groupby("Mois")["Chiffre_Affaires"].sum()

print("\n=== CHIFFRE D'AFFAIRES PAR MOIS ===")
print(ca_mois)

# 6. Exporter les résultats
ca_produit.to_csv("ca_par_produit.csv", header=["Chiffre_Affaires"])
ca_mois.to_csv("ca_par_mois.csv", header=["Chiffre_Affaires"])

df.to_excel("rapport_ventes.xlsx", index=False)

print("\nFichiers créés : ca_par_produit.csv, ca_par_mois.csv et rapport_ventes.xlsx")


# Graphique du chiffre d'affaires par produit
plt.figure(figsize=(9, 5))

ca_produit.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Chiffre d'affaires par produit", fontsize=15)
plt.xlabel("Chiffre d'affaires")
plt.ylabel("Produit")
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig("graphique_ca_produit.png", dpi=300)
plt.show()

print("Graphique créé : graphique_ca_produit.png")


# Analyse commerciale complémentaire

# 1. Produit qui génère le plus de chiffre d'affaires
meilleur_produit = ca_produit.idxmax()
ca_meilleur_produit = ca_produit.max()

# 2. Mois qui génère le plus de chiffre d'affaires
meilleur_mois = ca_mois.idxmax()
ca_meilleur_mois = ca_mois.max()

# 3. Part du chiffre d'affaires par produit
part_produit = (ca_produit / chiffre_affaires_total * 100).round(2)

print("\n=== ANALYSE COMMERCIALE ===")
print(f"Meilleur produit : {meilleur_produit}")
print(f"Son chiffre d'affaires : {ca_meilleur_produit:,.0f}")
print(f"Meilleur mois : {meilleur_mois}")
print(f"Chiffre d'affaires du meilleur mois : {ca_meilleur_mois:,.0f}")

print("\n=== PART DU CHIFFRE D'AFFAIRES PAR PRODUIT ===")
print(part_produit.astype(str) + " %")

# Exporter les parts vers un CSV
part_produit.to_csv("part_ca_produit.csv", header=["Part_Pourcentage"])

print("\nFichier créé : part_ca_produit.csv")


# Générer des recommandations commerciales automatiques

with open("recommandations_commerciales.txt", "w", encoding="utf-8") as fichier:
    fichier.write("RAPPORT DE RECOMMANDATIONS COMMERCIALES\n")
    fichier.write("=" * 45 + "\n\n")

    fichier.write(
        f"1. Produit leader : {meilleur_produit}, "
        f"avec un chiffre d'affaires de {ca_meilleur_produit:,.0f}.\n"
    )
    fichier.write(
        "   Recommandation : analyser la demande pour ce produit "
        "et vérifier la disponibilité du stock.\n\n"
    )

    fichier.write(
        f"2. Meilleur mois : {meilleur_mois}, "
        f"avec un chiffre d'affaires de {ca_meilleur_mois:,.0f}.\n"
    )
    fichier.write(
        "   Recommandation : examiner les campagnes commerciales "
        "et les facteurs qui pourraient expliquer cette performance.\n\n"
    )

    fichier.write(
        f"3. Part du produit leader dans le chiffre d'affaires : "
        f"{part_produit.loc[meilleur_produit]:.2f} %.\n"
    )
    fichier.write(
        "   Recommandation : surveiller la dépendance au produit leader "
        "et évaluer les possibilités de développer les autres produits.\n"
    )

print("Rapport créé : recommandations_commerciales.txt")
