import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr  # pour les corrélations

def etape1_main():
    print("Exécution de l'étape 1...")
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data

# -----------------------------------------------------------
# 1. Chargement des données
# -----------------------------------------------------------

## FIGURE 6
flow_stage = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_h_flow_stage.txt")
qs_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_Qs_samples.txt")
time_flow_stage = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_time_flow_stage.txt")
time_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_6/Fig6_time_samples.txt")

fig6 = pd.DataFrame({
    "time_flow_stage": time_flow_stage,
    "flow_stage": flow_stage
})
fig6_samples = pd.DataFrame({
    "time_sample": time_sample,
    "qs_sample": qs_sample
})

print("\n=== FIGURE 6 ===")
print("Tableau 1 : évolution du flow stage")
print(fig6.head())
print("\nTableau 2 : échantillons de débit solide")
print(fig6_samples.head())

## FIGURE 7
frequency = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Frequency.txt")
Qs_GSD = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Qs_GSD.txt")
time_sample = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Time_samples.txt")
time_seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_7/Fig7_Time_seismic_power.txt")

fig7_grains = pd.DataFrame(Qs_GSD, columns=[f"grain_class_{i+1}" for i in range(Qs_GSD.shape[1])])
fig7_grains.insert(0, "time_sample", time_sample)
fig7_freq = pd.DataFrame({"frequency": frequency})
fig7_time_seismic = pd.DataFrame({"time_seismic_power": time_seismic_power})

print("\n=== FIGURE 7 ===")
print("Granulométrie :")
print(fig7_grains.head(), "\n")
print("Axe des fréquences :")
print(fig7_freq.head(), "\n")
print("Axe temporel du signal sismique :")
print(fig7_time_seismic.head())

## FIGURE S1
seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_S1/S1_Seismic_power.txt")
time_seismic_power = np.loadtxt("C:/Users/vhava/Documents/Scolarité Eugénie/Ingé/1A/Cours/GE5SCING Sciences de l'Ingénieur/GE5MATHS Mathématiques pour les Sciences du Milieu Naturel/GE5MATHS Mathématiques pour les géosciences/Projet info/Fig_S1/S1_Time_seismic_power.txt")

# --- Vérification des dimensions ---
min_len = min(len(time_seismic_power), seismic_power.shape[0])
time_seismic_power = time_seismic_power[:min_len]
seismic_power = seismic_power[:min_len, :] if seismic_power.ndim == 2 else seismic_power[:min_len]

if seismic_power.ndim == 1:
    seismic_power = seismic_power[:, np.newaxis]

print("\n--- FIGURE S1 ---")
print("Seismic power shape:", seismic_power.shape)
print("Time seismic power shape:", time_seismic_power.shape)

# -----------------------------------------------------------
# 2. Normalisation de la puissance sismique
# -----------------------------------------------------------

# ---- Normalisation par bruit de fond (premières 300s) ----
background_window = time_seismic_power < 300
background_mean = seismic_power[background_window, :].mean(axis=0)
seismic_power_norm = seismic_power - background_mean

# --- Préparer les axes ---
time = time_seismic_power
freqs = np.linspace(0, 400, seismic_power.shape[1])  # adapter à ton max réel

# --- Figure à deux sous-graphes ---
fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# ---- (a) Raw seismic power ----
im1 = axs[0].imshow(
    seismic_power.T,
    aspect='auto',
    origin='lower',
    extent=[time[0], time[-1], freqs[0], freqs[-1]],
    cmap='viridis',
    vmin=-180, vmax=-80
)
axs[0].set_ylabel('Frequency (Hz)')
axs[0].set_title('(a) Raw seismic power')
cbar1 = fig.colorbar(im1, ax=axs[0])
cbar1.set_label('Seismic power (dB rel. m$^2$/s$^4$/Hz)')

# ---- (b) Normalized seismic power ----
im2 = axs[1].imshow(
    seismic_power_norm.T,
    aspect='auto',
    origin='lower',
    extent=[time[0], time[-1], freqs[0], freqs[-1]],
    cmap='viridis',
    vmin=-10, vmax=50
)
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Frequency (Hz)')
axs[1].set_title('(b) Normalized seismic power')
cbar2 = fig.colorbar(im2, ax=axs[1])
cbar2.set_label('Normalized seismic power (dB rel. 0.5 Hz)')

plt.tight_layout()
plt.show()
