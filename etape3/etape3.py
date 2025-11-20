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
