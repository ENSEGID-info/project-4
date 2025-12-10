import os
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# 0. Fonction utilitaire : répertoire du script
# -----------------------------------------------------------

def get_script_directory():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# -----------------------------------------------------------
# FIGURE 7 — Chargement des données
# -----------------------------------------------------------

def load_fig7_data(dir_path):
    freq = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Frequency.txt"))
    spec_norm = np.loadtxt(os.path.join(dir_path, "DATA", "Fig_7", "Fig7_Seismic_power_normalized.txt"))

    # transpose: (time, freq) → (freq, time)
    spec_norm = spec_norm.T

    return freq, spec_norm


# -----------------------------------------------------------
# FIGURE 7 — Affichage Seismic power normalisé
# -----------------------------------------------------------

def plot_seismic_power(freqs, spec_norm):
    """
    Reproduit la figure (c) Seismic power avec l'axe temps allant
    de 400 s à 1450 s.
    """

    n_freq, n_time = spec_norm.shape

    # Axe de temps demandé
    times = np.linspace(400, 1450, n_time)

    plt.figure(figsize=(14, 4))

    im = plt.imshow(
        spec_norm,
        origin='lower',
        aspect='auto',
        extent=[times.min(), times.max(), freqs.min(), freqs.max()],
        cmap='viridis',
        vmin=-10,
        vmax=50
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("(c) Seismic power (normalized)")

    cbar = plt.colorbar(im, pad=0.02)
    cbar.set_label("Normalized seismic power\n dB rel. (m² s⁻² Hz⁻¹)")

    plt.tight_layout()
    plt.show()


# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------

def main():
    dir_path = get_script_directory()
    print("Répertoire du script :", dir_path)

    freqs, spec_norm = load_fig7_data(dir_path)

    print("Fréquences :", freqs.shape)
    print("Spectrogramme normalisé :", spec_norm.shape)

    plot_seismic_power(freqs, spec_norm)


# exécution
if __name__ == "__main__":
    main()




