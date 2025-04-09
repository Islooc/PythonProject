import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import numpy as np

# Fonction de traitement et affichage du radar
def generer_radar_depuis_api():
    url = entry_url.get().strip()

    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer l'URL de l'API.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or not all('kpi_name' in d and 'value' in d for d in data):
            raise ValueError("Format de données invalide.")

        # Construction des KPI à afficher
        kpis = {d['kpi_name']: d['value'] for d in data}

        # Normalisation manuelle (à adapter selon les KPI disponibles)
        seuils_max = {
            "Lead Time": 10,                    # en jours
            "Order Fulfillment Rate": 100,      # %
            "Inventory Turnover": 6,            # idéal > 4
            "Ponctualité client (%)": 100,
            "ISR (Stock/Ventes)": 0.5,
            "Coût possession stock (€)": 50000,
            "Ponctualité fournisseurs (%)": 100,
            "DSI (jours)": 150,
            "Coût transport/tonne (€)": 100,
            "Commandes parfaites (%)": 100
        }

        labels = list(kpis.keys())
        normalized_kpis = []

        for label in labels:
            val = kpis[label]
            max_val = seuils_max.get(label, val)  # fallback = no normalization
            if "Turnover" in label or "DSI" in label or "Coût" in label or "Lead Time" in label:
                normalized = max(0, 1 - (val / max_val))  # moins c'est mieux
            else:
                normalized = min(1, val / max_val)        # plus c'est mieux
            normalized_kpis.append(normalized)

        # Radar chart
        values = normalized_kpis + [normalized_kpis[0]]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='blue', linewidth=2)
        ax.fill(angles, values, color='skyblue', alpha=0.4)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_title("Radar des KPI Supply Chain (via API)", size=15, pad=20)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur API", f"Impossible de récupérer ou traiter les données :\n{e}")

# Interface Tkinter
root = tk.Tk()
root.title("KPI Supply Chain - Récupération via API")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Adresse de l'API KPI (ex: http://10.101.1.116:8000/kpis)").pack(anchor="w")
entry_url = tk.Entry(frame, width=60)
entry_url.pack()

tk.Button(frame, text="Générer le graphique radar", command=generer_radar_depuis_api, bg="green", fg="white").pack(pady=10)

root.mainloop()
