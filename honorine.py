# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 15:39:27 2025
@author: vhava
"""

import os
import inspect
import numpy as np
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

    # Transposition nécessaire : (time, freq) → (freq, time)
    spec_norm = spec_norm.T

    return freq, spec_norm

# -----------------------------------------------------------
# FIGURE 7 — Affichage Seismic power normalisé avec annotations
# -----------------------------------------------------------

def plot_seismic_power(freqs, spec_norm, t_start=350, t_end=1400, event_times=None):
    """
    Affiche la figure (c) Seismic power avec extension à gauche et lignes verticales.
    """

    n_freq, n_time = spec_norm.shape

    # Axe temporel brut (supposé linéaire)
    times_scaled = np.linspace(0, 1450, n_time)

    # Masque temporel étendu
    mask = (times_scaled >= t_start) & (times_scaled <= t_end)
    spec_cut = spec_norm[:, mask]
    times_cut = times_scaled[mask]

    plt.figure(figsize=(14, 4))

    im = plt.imshow(
        spec_cut,
        origin='lower',
        aspect='auto',
        extent=[times_cut.min(), times_cut.max(), freqs.min(), freqs.max()],
        cmap='viridis',
        vmin=-10,
        vmax=50
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("(c) Seismic power")

    # Ajout des lignes verticales si spécifiées
    if event_times:
        for t in event_times:
            if t_start <= t <= t_end:
                plt.axvline(x=t, color='white', linestyle='--', linewidth=1)

    cbar = plt.colorbar(im, pad=0.02)
    cbar.set_label("Normalized seismic power\n dB rel. (m² s⁻² Hz⁻¹)", fontsize=12)

    plt.tight_layout()
    plt.show()

    print("Min =", np.min(spec_cut))
    print("Max =", np.max(spec_cut))
    print("Mean =", np.mean(spec_cut))
    print("Std  =", np.std(spec_cut))

# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------

def main():
    dir_path = get_script_directory()
    print("Répertoire du script :", dir_path)

    freqs, spec_norm = load_fig7_data(dir_path)

    print("Fréquences :", freqs.shape)
    print("Spectrogramme normalisé :", spec_norm.shape)

    # Exemple d'événements à annoter
    event_times = [520, 780, 1020, 1260]

    plot_seismic_power(freqs, spec_norm, t_start=350, t_end=1400, event_times=event_times)

# Exécution
if __name__ == "__main__":
    main()
