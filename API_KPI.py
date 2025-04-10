import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from collections import defaultdict

# Traductions
kpi_traductions = {
    "Lead Time": "Délai d'exécution",
    "Order Fulfillment Rate": "Taux de satisfaction des commandes",
    "Inventory Turnover": "Rotation des stocks",
    "Perfect Order Rate": "Taux de commandes parfaites",
    "ISR (Stock/Ventes)": "Ratio stock/ventes",
    "On-time Delivery Rate": "Livraisons à l'heure",
    "Transportation Cost per Ton": "Coût transport/tonne",
    "DSI (jours)": "Durée rotation des stocks",
    "Supplier Lead Time": "Délai fournisseurs"
}

# Seuils pour normalisation
seuils_max_defaut = {
    "Lead Time": 10,
    "Supplier Lead Time": 10,
    "Order Fulfillment Rate": 100,
    "Inventory Turnover": 6,
    "Perfect Order Rate": 100,
    "ISR (Stock/Ventes)": 0.5,
    "On-time Delivery Rate": 100,
    "Transportation Cost per Ton": 100,
    "DSI (jours)": 150
}

def normaliser(kpi_name, value):
    max_val = seuils_max_defaut.get(kpi_name, value)
    if any(key in kpi_name for key in ["Turnover", "DSI", "Cost", "Lead Time"]):
        return max(0, 1 - (value / max_val))
    else:
        return min(1, value / max_val)

def generer_radar_depuis_api():
    url = entry_url.get().strip()

    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer l'URL de l'API.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Format de données invalide.")

        # Regrouper les KPI par nom
        grouped_kpis = defaultdict(list)
        for item in data:
            name = item['kpi_name']
            val = item['value']
            grouped_kpis[name].append(val)

        # Ne garder que les 8 premiers KPI
        selected_kpis = dict(list(grouped_kpis.items())[:8])

        if len(selected_kpis) < 3:
            raise ValueError("Pas assez de KPI pour générer un radar chart (minimum 3).")

        # Étiquettes originales et traduites
        labels_en = list(selected_kpis.keys())
        labels_fr = [kpi_traductions.get(k, k) for k in labels_en]

        # Valeurs pour chaque KPI
        max_values = [max(vals) for vals in selected_kpis.values()]
        avg_values = [sum(vals) / len(vals) for vals in selected_kpis.values()]

        norm_max = [normaliser(k, v) for k, v in zip(labels_en, max_values)]
        norm_avg = [normaliser(k, v) for k, v in zip(labels_en, avg_values)]

        values_max = norm_max + [norm_max[0]]
        values_avg = norm_avg + [norm_avg[0]]

        angles = np.linspace(0, 2 * np.pi, len(labels_fr), endpoint=False).tolist()
        angles += angles[:1]

        # Affichage
        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
        ax.set_facecolor('#f4f4f4')
        fig.patch.set_facecolor('white')

        # Tracer superposition en VERT
        for i in range(len(angles)-1):
            pts_angle = [angles[i], angles[i+1]]
            pts_max = [values_max[i], values_max[i+1]]
            pts_avg = [values_avg[i], values_avg[i+1]]
            if pts_max[0] >= pts_avg[0] and pts_max[1] >= pts_avg[1]:
                ax.fill(pts_angle + pts_angle[::-1],
                        pts_avg + pts_max[::-1], color='green', alpha=0.3)

        # Tracer la moyenne (BLEU)
        ax.plot(angles, values_avg, color='blue', linewidth=2, linestyle='--', label="Moyenne")
        ax.fill(angles, values_avg, color='blue', alpha=0.15)

        # Tracer les max (ROUGE)
        ax.plot(angles, values_max, color='red', linewidth=2, label="Valeur max")
        ax.fill(angles, values_max, color='red', alpha=0.25)

        # Titres autour du cercle
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(["" for _ in labels_fr])
        for angle, label in zip(angles[:-1], labels_fr):
            x = np.cos(angle) * 1.15
            y = np.sin(angle) * 1.15
            ha = 'center'
            va = 'center'
            if angle == 0:
                va = 'bottom'
            elif angle == np.pi:
                va = 'top'
            elif angle < np.pi:
                ha = 'left'
            else:
                ha = 'right'
            ax.text(angle, 1.12, label, size=10, ha=ha, va=va, fontweight='bold')

        # Valeurs sur les max
        for angle, val in zip(angles, max_values + [max_values[0]]):
            ax.text(angle, 1.02, f"{val:.1f}", ha='center', va='center', fontsize=9,
                    bbox=dict(facecolor='white', alpha=0.6, boxstyle='round'))

        ax.set_ylim(0, 1)
        ax.set_title("Radar des KPI Logistiques (Max vs Moyenne)", size=16, pad=20, fontweight='bold')
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur API", f"Impossible de récupérer ou traiter les données :\n{e}")

# Interface Tkinter
root = tk.Tk()
root.title("📈 Radar KPI Supply Chain (API)")

frame = tk.Frame(root, padx=12, pady=12)
frame.pack()

tk.Label(frame, text="Adresse de l'API (ex: http://10.101.1.116:8000/kpis)", font=("Arial", 11)).pack(anchor="w")
entry_url = tk.Entry(frame, width=60)
entry_url.pack(pady=5)

tk.Button(frame, text="Générer le Radar Chart", command=generer_radar_depuis_api,
          bg="#28a745", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

root.mainloop()
