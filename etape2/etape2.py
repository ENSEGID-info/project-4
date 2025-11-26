
# Programme figure 6

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os


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
# ---------------------------------------------------------------
# 1️⃣ CHARGEMENT DES FICHIERS UTILISATEUR
# ---------------------------------------------------------------

# 📍 🔽 Modifie ici les noms de tes fichiers 🔽
file_times_samples = "E:\ENSEGID\Projet de programmation\Figure 6\Fig6_time_samples.txt"
file_Qs_samples = "E:\ENSEGID\Projet de programmation\Figure 6\Fig6_Qs_samples.txt"
file_times_flow_stage = "E:\ENSEGID\Projet de programmation\Figure 6\Fig6_time_flow_stage.txt"
file_h_flow_stage = "E:\ENSEGID\Projet de programmation\Figure 6\Fig6_h_flow_stage.txt"

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

Qs_inlet_value = np.mean(len(Qs_samples)) # Flux constant d’entrée (ligne bleue)

# ---------------------------------------------------------------
# 3️⃣ DÉTECTION AUTOMATIQUE DES ZONES SANS MESURES
# ---------------------------------------------------------------

# Calcul des écarts de temps entre mesures
time_gaps = np.diff(times_samples)

# Seuil automatique : 3× la moyenne des écarts
gap_threshold = 3 * np.mean(time_gaps)

# Détection des intervalles sans mesures
no_measure_periods = []
time_gaps = np.diff(times_samples)
gap_treshold = 3*np.mean(time_gaps)
for i in range(len(times_samples) - 1):
    if times_samples[i + 1] - times_samples[i] >= gap_threshold:
        start = times_samples[i]+0.001
        end = times_samples[i+1]-0.001
        no_measure_periods.append((start, end))
        last_measure_time = times_samples[-1]
        end_of_time = max(times_flow_stage[-1], last_measure_time*1.05)
        no_measure_periods.append((last_measure_time + 0.001, end_of_time))
        

print("\n Zones sans mesures détectées :", no_measure_periods, "\n")


# ---------------------------------------------------------------
# 3️⃣ CRÉATION DU GRAPHIQUE
# ---------------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# ---- (a) Flow surface elevation ----
ax1.plot(times_flow_stage, h_flow_stage, color='royalblue', linewidth=2)
ax1.set_ylabel("H(cm)", fontsize=12)
ax1.set_title("(a) Flow surface elevation", fontsize=13)


# ---- (b) Sediment flux ----
# Zones grisées = pas de mesures
for (start, end) in no_measure_periods:
    ax2.axvspan(start, end, color='lightgray', alpha=0.4,label="No measures" if start == no_measure_periods[0][0] else "")
    

# On ne garde que les valeurs dans les zones mesurées
mask_valid = np.ones_like(Qs_samples, dtype=bool)
for (start, end) in no_measure_periods:
    mask_valid &= ~((times_samples >= start) & (times_samples <= end))


# Barres rouges uniquement sur les zones avec mesures
ax2.bar(times_samples[mask_valid], Qs_samples[mask_valid],width=3, color='lightcoral', label='Sampled outlet sediment flux')


# Ligne bleue : flux constant d’entrée
ax2.axhline(Qs_inlet_value, color='blue', linewidth=1, label='Storage area inlet sediment flux')

# Titres, axes, légendes
ax2.set_ylabel("Qs (g/s)", fontsize=12)
ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_title("(b) Solid discharge", fontsize=13)
ax2.legend(loc='upper right', fontsize=9)



if no_measure_periods:
    # La fin de la dernière zone grise
    end_time = no_measure_periods[-1][1]
    ax2.set_xlim(left=0, right=end_time)
    ax1.set_xlim(left=0, right=end_time)


plt.tight_layout()
plt.show()

# Programme figure 7

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# 1) CHARGEMENT DES DONNEES
# -------------------------------------------------------------------

# Fichiers principaux
file_gsd = r"E:\ENSEGID\Projet de programmation\Figure 7\Fig7_Qs_GSD.txt"              # GSD (66 x 8)
file_times = r"E:\ENSEGID\Projet de programmation\Figure 7\Fig7_Time_samples.txt"              # Temps (66 lignes)


GSD = np.loadtxt(file_gsd)
times = np.loadtxt(file_times)

if GSD.shape[0] != len(times):
    raise ValueError("Nombre de lignes GSD != nombre de temps.")

# -------------------------------------------------------------------
# 2) DEFINITIONS DES CLASSES GRANULOMETRIQUES ET COULEURS
# -------------------------------------------------------------------

grain_classes = [
    "D > 12.5 mm",
    "10 mm < D < 12.5 mm",
    "8 mm < D < 10 mm",
    "6.3 mm < D < 8 mm",
    "4 mm < D < 6.3 mm",
    "3.15 mm < D < 4 mm",
    "2 mm < D < 3.15 mm",
    "D < 2 mm"
]

colors = [
    "#1a1a1a",
    "#4c2b1f",
    "#6b3c25",
    "#8d522d",
    "#b56a2d",
    "#d68d3a",
    "#f2b45b",
    "#ffcc80"
]

# -------------------------------------------------------------------
# 3) FIGURE PRINCIPALE : GSD EMPILEE AVEC BARRES EPAISSES
# -------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14,6))

# Largeur des barres optimisée pour 66 points
bar_width = 5 # valeurs >0.8 rendent les barres plus épaisses

# Empilement des barres avec contours noirs
ax.bar(times, GSD[:,0], color=colors[0], edgecolor='black', linewidth=0.8, width=bar_width, label=grain_classes[0])
bottom = GSD[:,0].copy()
for i in range(1, GSD.shape[1]):
    ax.bar(times, GSD[:,i], bottom=bottom, color=colors[i],
           edgecolor='black', linewidth=0.5, width=bar_width, label=grain_classes[i])
    bottom += GSD[:,i]

# Labels et titre
ax.set_xlabel("Time (s)", fontsize=12)
ax.set_ylabel("Q$_s$ (g s$^{-1}$)", fontsize=12)
ax.set_title("Solid Discharge and Grain Size Distribution ", fontsize=14)
ax.set_xlim(times.min(), times.max())

# Limites de l'axe du temps étendues jusqu'à 1977
ax.set_xlim(400, 1450)
ax.set_ylim(0,400)


# Légende
ax.legend(fontsize=15, framealpha=1, loc='upper center', ncol=1)

plt.tight_layout()
plt.show()