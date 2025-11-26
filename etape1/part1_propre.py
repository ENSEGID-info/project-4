import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import os, inspect


# -----------------------------------------------------------
# 0. Fonction utilitaire : chemin du script
# -----------------------------------------------------------

def get_script_directory():
    """Retourne le répertoire où se trouve part_1.py."""
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# -----------------------------------------------------------
# FIGURE 6 — Chargement des données
# -----------------------------------------------------------

def load_fig6_data(dir_path):
    """Charge les données de la Figure 6 et renvoie deux DataFrame."""
    flow_stage = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_6", "Fig6_h_flow_stage.txt"))
    qs_sample = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_6", "Fig6_Qs_samples.txt"))
    time_flow_stage = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_6", "Fig6_time_flow_stage.txt"))
    time_sample = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_6", "Fig6_time_samples.txt"))

    fig6 = pd.DataFrame({
        "time_flow_stage": time_flow_stage,
        "flow_stage": flow_stage
    })
    fig6_samples = pd.DataFrame({
        "time_sample": time_sample,
        "qs_sample": qs_sample
    })

    return fig6, fig6_samples


# -----------------------------------------------------------
# FIGURE 7 — Chargement des données
# -----------------------------------------------------------

def load_fig7_data(dir_path):
    """Charge les données de la Figure 7 et renvoie trois DataFrame."""
    frequency = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Frequency.txt"))
    Qs_GSD = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Qs_GSD.txt"))
    time_sample = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Time_samples.txt"))
    time_seismic_power = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Time_seismic_power.txt"))

    fig7_grains = pd.DataFrame(Qs_GSD, columns=[f"grain_class_{i+1}" for i in range(Qs_GSD.shape[1])])
    fig7_grains.insert(0, "time_sample", time_sample)

    fig7_freq = pd.DataFrame({"frequency": frequency})
    fig7_time_seismic = pd.DataFrame({"time_seismic_power": time_seismic_power})

    return fig7_grains, fig7_freq, fig7_time_seismic


# -----------------------------------------------------------
# FIGURE S1 — Chargement des données
# -----------------------------------------------------------

def load_figS1_data(dir_path):
    """Charge les données de la Figure S1 et les retourne sous forme numpy."""
    seismic_power = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_S1", "S1_Seismic_power.txt"))
    time_seismic_power = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_S1", "S1_Time_seismic_power.txt"))

    min_len = min(len(time_seismic_power), seismic_power.shape[0])
    time = time_seismic_power[:min_len]
    power = seismic_power[:min_len, :] if seismic_power.ndim == 2 else seismic_power[:min_len]

    if power.ndim == 1:
        power = power[:, np.newaxis]

    return time, power


# -----------------------------------------------------------
# Normalisation de la puissance sismique
# -----------------------------------------------------------

def normalize_seismic_power(time, power, background_duration=300):
    """Normalise la puissance sismique en soustrayant le bruit de fond."""
    background_window = time < background_duration
    background_mean = power[background_window, :].mean(axis=0)
    power_norm = power - background_mean
    return power_norm


# -----------------------------------------------------------
# Affichage (raw + normalized)
# -----------------------------------------------------------

def plot_seismic_power(time, power, power_norm):
    """Affiche la puissance sismique brute et normalisée."""
    freqs = np.linspace(0, 400, power.shape[1])

    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # (a) Raw
    im1 = axs[0].imshow(
        power.T, aspect='auto', origin='lower',
        extent=[time[0], time[-1], freqs[0], freqs[-1]],
        cmap='viridis', vmin=-180, vmax=-80
    )
    axs[0].set_ylabel('Frequency (Hz)')
    axs[0].set_title('(a) Raw seismic power')
    fig.colorbar(im1, ax=axs[0], label='Seismic power (dB rel. m$^2$/s$^4$/Hz)')

    # (b) Normalized
    im2 = axs[1].imshow(
        power_norm.T, aspect='auto', origin='lower',
        extent=[time[0], time[-1], freqs[0], freqs[-1]],
        cmap='viridis', vmin=-10, vmax=50
    )
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Frequency (Hz)')
    axs[1].set_title('(b) Normalized seismic power')
    fig.colorbar(im2, ax=axs[1], label='Normalized seismic power (dB rel. 0.5 Hz)')

    plt.tight_layout()
    plt.show()


# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------

def main():
    dir_path = get_script_directory()
    print("Dossier du script =", dir_path)

    # FIGURE 6
    fig6, fig6_samples = load_fig6_data(dir_path)
    print("\n=== FIGURE 6 ===")
    print(fig6.head())
    print(fig6_samples.head())

    # FIGURE 7
    fig7_grains, fig7_freq, fig7_time = load_fig7_data(dir_path)
    print("\n=== FIGURE 7 ===")
    print(fig7_grains.head())
    print(fig7_freq.head())
    print(fig7_time.head())

    # FIGURE S1
    time, power = load_figS1_data(dir_path)
    power_norm = normalize_seismic_power(time, power)

    plot_seismic_power(time, power, power_norm)


# -----------------------------------------------------------
# Lancer le programme
# -----------------------------------------------------------

if __name__ == "__main__":
    main()

