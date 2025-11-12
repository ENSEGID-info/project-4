import matplotlib


def etape2_main(data):
    print("Exécution de l'étape 2...")
    # Exemple : traitement de la donnée
    result = max(data)
    return result




# ===============================================================
# Reproduction du graphique : Flow surface elevation & Sediment flux
# ---------------------------------------------------------------
# Ce script lit 4 fichiers texte/CSV :
#  1. times_samples.txt      → Temps (s) des mesures de flux sédimentaire
#  2. Qs_samples.txt         → Flux sédimentaire (g/s)
#  3. times_flow_stage.txt   → Temps (s) des mesures de hauteur d’eau
#  4. h_flow_stage.txt       → Hauteur d’eau (cm)
#
# ⚠️ Format attendu pour chaque fichier : une colonne de valeurs numériques
# ---------------------------------------------------------------
# Le programme génère une figure à deux sous-graphiques :
# (a) Flow surface elevation
# (b) Sediment flux
# ===============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------
# 1️⃣ CHARGEMENT DES FICHIERS UTILISATEUR
# ---------------------------------------------------------------

# 📍 🔽 Modifie ici les noms de tes fichiers 🔽
file_times_samples = "times_samples.txt"
file_Qs_samples = "Qs_samples.txt"
file_times_flow_stage = "times_flow_stage.txt"
file_h_flow_stage = "h_flow_stage.txt"

# Vérification de l’existence des fichiers
for f in [file_times_samples, file_Qs_samples, file_times_flow_stage, file_h_flow_stage]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Le fichier '{f}' est introuvable. Vérifie son nom et son emplacement.")

# Lecture des données
times_samples = np.loadtxt(file_times_samples)
Qs_samples = np.loadtxt(file_Qs_samples)
times_flow_stage = np.loadtxt(file_times_flow_stage)
h_flow_stage = np.loadtxt(file_h_flow_stage)

# Vérifications de cohérence
if len(times_samples) != len(Qs_samples):
    raise ValueError("Les fichiers 'times_samples' et 'Qs_samples' doivent avoir la même longueur.")
if len(times_flow_stage) != len(h_flow_stage):
    raise ValueError("Les fichiers 'times_flow_stage' et 'h_flow_stage' doivent avoir la même longueur.")

# ---------------------------------------------------------------
# 2️⃣ PARAMÈTRES PERSONNALISABLES
# ---------------------------------------------------------------

# Valeur constante de flux à l’entrée (ligne bleue)
Qs_inlet_value = 80  # 💡 à ajuster selon tes données

# Intervalles de temps sans mesures (zones grisées)
no_measure_periods = [(750, 1100), (1300, 1500)]  # 💡 adapte selon ton cas

# ---------------------------------------------------------------
# 3️⃣ CRÉATION DU GRAPHIQUE
# ---------------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# ---- (a) Flow surface elevation ----
ax1.plot(times_flow_stage, h_flow_stage, color='royalblue', linewidth=2)
ax1.set_ylabel("h (cm)", fontsize=12)
ax1.set_title("(a) Flow surface elevation", fontsize=13)
ax1.grid(True, linestyle='--', alpha=0.5)

# ---- (b) Sediment flux ----
# Zones grisées = pas de mesures
for (start, end) in no_measure_periods:
    ax2.axvspan(start, end, color='gray', alpha=0.4,
                label="No measures" if start == no_measure_periods[0][0] else "")

# Barres rouges : flux mesurés
ax2.bar(times_samples, Qs_samples, width=5, color='lightcoral', label='Sampled outlet sediment flux')

# Ligne bleue : flux constant d’entrée
ax2.axhline(Qs_inlet_value, color='blue', linewidth=1.5, label='Storage area inlet sediment flux')

# Titres, axes, légendes
ax2.set_ylabel("Qs (g/s)", fontsize=12)
ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_title("(b) Sediment flux", fontsize=13)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
    
    
    