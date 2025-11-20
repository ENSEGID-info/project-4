<<<<<<< Updated upstream
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
=======
import numpy as np
import matplotlib.pyplot as plt

# ================================================================
# 1) CHARGEMENT DES DONNÉES
# ================================================================

file_gsd = r"E:\ENSEGID\Projet de programmation\Figure 7\Fig7_Qs_GSD.txt"
file_times = r"E:\ENSEGID\Projet de programmation\Figure 7\Fig7_Time_samples.txt"
>>>>>>> Stashed changes

GSD = np.loadtxt(file_gsd)
times = np.loadtxt(file_times)

if GSD.shape[0] != len(times):
    raise ValueError("Nombre de lignes GSD != nombre de temps.")

# Débit solide total Qs(t)
Qs_total = np.sum(GSD, axis=1)


<<<<<<< Updated upstream
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

=======
# ================================================================
# 2) EXTRACTION DU SEGMENT ENTRE t1 = 472.4 s ET t2 = 617.1 s
# ================================================================

t1 = 472.4
t2 = 617.1
mask = (times >= t1) & (times <= t2)
>>>>>>> Stashed changes

times_sel = times[mask]
Qs_sel = Qs_total[mask]

# Normalisation pour le schéma
Qs_norm = Qs_sel / np.max(Qs_sel)

<<<<<<< Updated upstream
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

=======

# ================================================================
# 3) CRÉATION DU SCHÉMA DU PULSE
# ================================================================

# Ligne de sol légèrement inclinée
x = np.linspace(0, 1, len(times_sel))
ground = 0.15 - 0.10 * x

# Couleurs GSD (identiques à ton graphique)
colors = [
    "#1a1a1a", "#4c2b1f", "#6b3c25", "#8d522d",
    "#b56a2d", "#d68d3a", "#f2b45b", "#ffcc80"
]

# Génération aléatoire contrôlée des grains
np.random.seed(42)

grain_x = []
grain_y = []
grain_sizes = []
grain_colors = []

for i in range(len(times_sel)):
    n_grains = int(20 * Qs_norm[i]) + 1

    for g in range(n_grains):
        gx = x[i] + np.random.uniform(-0.015, 0.015)
        gy = ground[i] + np.random.uniform(0.0, 0.10)

        class_index = np.random.randint(0, 8)
        size = (class_index + 1) * 30 + np.random.uniform(0, 15)

        grain_x.append(gx)
        grain_y.append(gy)
        grain_sizes.append(size)
        grain_colors.append(colors[class_index])


# ================================================================
# 4) FIGURE IDENTIQUE AU PANEL (a)
# ================================================================

fig, ax = plt.subplots(figsize=(10, 4))

# Sol
ax.plot(x, ground, color="black", linewidth=2)

# Grains
ax.scatter(grain_x, grain_y, s=grain_sizes, c=grain_colors, alpha=0.85)

# Flèche g
ax.annotate("", xy=(0.95, 0.80), xytext=(0.95, 0.95),
            arrowprops=dict(arrowstyle="->", lw=2),
            xycoords="axes fraction")
ax.text(0.96, 0.87, "g", fontsize=12, ha="left", va="center", transform=ax.transAxes)

# Zones Tail / Body / Front
ax.annotate("Tail",  xy=(0.10, 0.15), xytext=(0.10, -0.05), ha="center", fontsize=12)
ax.annotate("Body",  xy=(0.45, 0.15), xytext=(0.45, -0.05), ha="center", fontsize=12)
ax.annotate("Front", xy=(0.80, 0.15), xytext=(0.80, -0.05), ha="center", fontsize=12)

# Cadre rouge comme sur la figure
for spine in ax.spines.values():
    spine.set_edgecolor("#7a0e0e")
    spine.set_linewidth(2)

ax.set_title("(a) Sketch of a pulse", fontsize=16, pad=20)

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.1, 0.45)
ax.axis("off")
>>>>>>> Stashed changes

plt.tight_layout()
plt.show()