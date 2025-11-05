import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr #en fait c'est l'histoire de ce qu'on a fait en stat, avec les corrélations donc si c'est >0 les variables varient dans le même sens et sinon en sens inverse



def etape1_main():
    print("Exécution de l'étape 1...")
    # Exemple : lecture d’un fichier ou génération de données
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data



# -----------------------------------------------------------
# 1. Chargement des données
# -----------------------------------------------------------

##FIGURE 6

import numpy as np
import pandas as pd

# === Figure 6 ===

# Chargement des fichiers (sans en-têtes)
flow_stage = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_h_flow_stage.txt")

qs_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_Qs_samples.txt")

time_flow_stage = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_time_flow_stage.txt")

time_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_time_samples.txt")


# numpy.load(fichier, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII', *, max_header_size=10000) [source]  Charger des tableaux ou des objets pickled à partir de fichiers
# Création d'un DataFrame clair
fig6 = pd.DataFrame({
    "time_flow_stage": time_flow_stage,
    "flow_stage": flow_stage
})

# On ajoute aussi un tableau séparé pour les échantillons
fig6_samples = pd.DataFrame({
    "time_sample": time_sample,
    "qs_sample": qs_sample
})

print("\n=== FIGURE 6 ===")
print("Tableau 1 : évolution du flow stage")
print(fig6.head())
print("\nTableau 2 : échantillons de débit solide")
print(fig6_samples.head())

##FIGURE 7
# === FIGURE 7 ===

frequency = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Frequency.txt")

Qs_GSD = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Qs_GSD.txt")

time_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Time_samples.txt")

time_seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Time_seismic_power.txt")


print("frequency :", frequency.shape)
print("Qs_GSD :", Qs_GSD.shape)
print("time_sample :", time_sample.shape)
print("time_seismic_power :", time_seismic_power.shape)

# Tableau 1 : granulométrie (OK : 74x8 + 74)
fig7_grains = pd.DataFrame(Qs_GSD, columns=[f"grain_class_{i+1}" for i in range(Qs_GSD.shape[1])])
fig7_grains.insert(0, "time_sample", time_sample)

# Tableau 2 : axe fréquentiel seul
fig7_freq = pd.DataFrame({"frequency": frequency})

# Tableau 3 : axe temporel du signal sismique seul
fig7_time_seismic = pd.DataFrame({"time_seismic_power": time_seismic_power})

print("\n=== FIGURE 7 ===")
print("Granulométrie :")
print(fig7_grains.head(), "\n")
print("Axe des fréquences :")
print(fig7_freq.head(), "\n")
print("Axe temporel du signal sismique :")
print(fig7_time_seismic.head())


##FIGURE S1

# === FIGURE S1 ===

seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_S1/S1_Seismic_power.txt")
time_seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_S1/S1_Time_seismic_power.txt")

print("seismic_power shape:", np.shape(seismic_power))
print("time_seismic_power shape:", np.shape(time_seismic_power))

# === Cas 1 : 1D ===
if seismic_power.ndim == 1 and len(seismic_power) == len(time_seismic_power):
    figS1 = pd.DataFrame({
        "time_seismic_power": time_seismic_power,
        "seismic_power": seismic_power
    })
    print(" Signal sismique 1D reconnu")

# === Cas 2 : 2D ===
elif seismic_power.ndim == 2 and seismic_power.shape[0] == len(time_seismic_power):
    figS1 = pd.DataFrame(seismic_power,
                         columns=[f"freq_bin_{i+1}" for i in range(seismic_power.shape[1])])
    figS1.insert(0, "time_seismic_power", time_seismic_power)
    print(f" Spectrogramme détecté : {seismic_power.shape[0]} instants × {seismic_power.shape[1]} fréquences")

# === Cas 3 : dimensions incompatibles ===
else:
    print("Incohérence de dimensions — stockage séparé")
    figS1_time = pd.DataFrame({"time_seismic_power": np.ravel(time_seismic_power)})
    figS1_power = pd.DataFrame(seismic_power)
    figS1 = None

print("\n--- FIGURE S1 ---")
if figS1 is not None:
    print(figS1.head())
else:
    print("Temps :")
    print(figS1_time.head())
    print("Puissance :")
    print(figS1_power.head())

# -----------------------------------------------------------
# 2. Normalisation de la puissance sismique
# -----------------------------------------------------------
import numpy as np
import pandas as pd

# ---- Normalisation Z-score de la puissance sismique ----
# Chaque colonne (fréquence) est centrée et réduite indépendamment
seismic_power_z = (seismic_power - seismic_power.mean(axis=0)) / seismic_power.std(axis=0)

# Création d'un DataFrame uniquement pour la puissance normalisée
figS1_power_z = pd.DataFrame(seismic_power_z,
                             columns=[f"freq_{i+1}" for i in range(seismic_power_z.shape[1])])

print(" Z-score calculé pour la puissance sismique")
print(figS1_power_z.head())

##BONUS: Visualisation
import matplotlib.pyplot as plt
import numpy as np

# --- Préparer les axes ---
# Temps : tronqué pour correspondre au nombre de lignes de la puissance
time = time_seismic_power[:figS1_power_z.shape[0]]
freqs = np.arange(1, figS1_power_z.shape[1]+1)

plt.figure(figsize=(12, 5))

# --- Affichage du spectrogramme transposé ---
plt.imshow(
    seismic_power_z.T,       # Transpose pour avoir fréquence en y, temps en x
    aspect='auto',
    origin='lower',
    extent=[time[0], time[-1], freqs[0], freqs[-1]],
    cmap='jet'             # ou 'jet' pour se rapprocher de la figure d’origine sinon c'était turbo
)

plt.colorbar(label='Normalized seismic power (dB rel. 0.5 Hz)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Seismic power (normalized)')
plt.tight_layout()
plt.show()

