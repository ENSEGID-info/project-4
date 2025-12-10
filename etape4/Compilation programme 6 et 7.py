# ================================================================
# IMPORTS
# ================================================================
import os
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================================================================
# 0. FONCTION UTILITAIRE — Répertoire du script
# ================================================================
def get_script_directory():
    """
    Retourne le répertoire contenant ce script.

    Parameters
    ----------
    None.

    Returns
    -------
    str
        Chemin complet du dossier où se trouve le script.
    """
    return os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())
    ))

# ================================================================
# FONCTION UTILITAIRE — AUTO-DETECTION DES FICHIERS
# ================================================================
def find_file(root_folder, pattern):
    """
    Recherche récursivement le premier fichier dont le nom contient
    un motif donné.

    Parameters
    ----------
    root_folder : str
        Répertoire racine pour la recherche.
    pattern : str
        Motif à rechercher dans le nom du fichier.

    Returns
    -------
    str
        Chemin complet du premier fichier trouvé.

    Raises
    ------
    FileNotFoundError
        Si aucun fichier ne correspond au motif.
    """
    pattern = pattern.lower()
    for root, dirs, files in os.walk(root_folder):
        for f in files:
            if pattern in f.lower():
                return os.path.join(root, f)
    raise FileNotFoundError(f"❌ Fichier introuvable contenant : {pattern}")

# ================================================================
# 1. CHARGEMENT DES DONNÉES — FIGURE 6 (AUTO-DETECT)
# ================================================================
def load_fig6_data(dir_path):
    """
    Charge les fichiers de données pour la Figure 6.

    Parameters
    ----------
    dir_path : str
        Chemin du répertoire contenant les fichiers.

    Returns
    -------
    fig6 : pd.DataFrame
        Colonnes : 'time_flow_stage' et 'flow_stage'.
    fig6_samples : pd.DataFrame
        Colonnes : 'time_sample' et 'qs_sample'.
    """
    f_flow_stage = find_file(dir_path, "fig6_h_flow_stage")
    f_qs_sample = find_file(dir_path, "fig6_qs_samples")
    f_time_flow = find_file(dir_path, "fig6_time_flow_stage")
    f_time_sample = find_file(dir_path, "fig6_time_samples")

    flow_stage = np.loadtxt(f_flow_stage)
    qs_sample = np.loadtxt(f_qs_sample)
    time_flow_stage = np.loadtxt(f_time_flow)
    time_sample = np.loadtxt(f_time_sample)

    fig6 = pd.DataFrame({
        "time_flow_stage": time_flow_stage,
        "flow_stage": flow_stage
    })
    fig6_samples = pd.DataFrame({
        "time_sample": time_sample,
        "qs_sample": qs_sample
    })

    return fig6, fig6_samples

# ================================================================
# 2. CHARGEMENT DES DONNÉES — FIGURE 7 (AUTO-DETECT)
# ================================================================
def load_fig7_data(dir_path):
    """
    Charge les fichiers de données pour la Figure 7.

    Parameters
    ----------
    dir_path : str
        Chemin du répertoire contenant les fichiers.

    Returns
    -------
    fig7_grains : pd.DataFrame
        Contient 'time_sample' et chaque colonne de classe de grains.
    fig7_freq : pd.DataFrame
        Contient la colonne 'frequency'.
    fig7_time_seismic : pd.DataFrame
        Contient la colonne 'time_seismic_power'.
    """
    f_frequency = find_file(dir_path, "fig7_frequency")
    f_gsd = find_file(dir_path, "fig7_qs_gsd")
    f_time_sample = find_file(dir_path, "fig7_time_samples")
    f_time_seismic = find_file(dir_path, "fig7_time_seismic_power")

    frequency = np.loadtxt(f_frequency)
    Qs_GSD = np.loadtxt(f_gsd)
    time_sample = np.loadtxt(f_time_sample)
    time_seismic_power = np.loadtxt(f_time_seismic)

    fig7_grains = pd.DataFrame(
        Qs_GSD, columns=[f"grain_class_{i+1}" for i in range(Qs_GSD.shape[1])]
    )
    fig7_grains.insert(0, "time_sample", time_sample)
    fig7_freq = pd.DataFrame({"frequency": frequency})
    fig7_time_seismic = pd.DataFrame(
        {"time_seismic_power": time_seismic_power}
    )

    return fig7_grains, fig7_freq, fig7_time_seismic

# ================================================================
# 3. FIGURE 6 — Flow Elevation + Sediment Flux
# ================================================================
def figure_6(fig6, fig6_samples):
    """
    Trace la Figure 6 : hauteur de surface et débit solide.

    Les périodes sans mesures sont détectées automatiquement et mises
    en gris. La ligne bleue représente le flux constant d’entrée
    (moyenne des mesures).

    Parameters
    ----------
    fig6 : pd.DataFrame
        Contient 'time_flow_stage' et 'flow_stage'.
    fig6_samples : pd.DataFrame
        Contient 'time_sample' et 'qs_sample'.

    Returns
    -------
    None.
    """
    times_flow_stage = fig6["time_flow_stage"].values
    h_flow_stage = fig6["flow_stage"].values
    times_samples = fig6_samples["time_sample"].values
    Qs_samples = fig6_samples["qs_sample"].values

    Qs_inlet_value = np.mean(len(Qs_samples))
    time_gaps = np.diff(times_samples)
    gap_threshold = 3 * np.mean(time_gaps)
    no_measure_periods = []

    for i in range(len(times_samples) - 1):
        if times_samples[i + 1] - times_samples[i] >= gap_threshold:
            start = times_samples[i] + 0.001
            end = times_samples[i + 1] - 0.001
            no_measure_periods.append((start, end))

    end_of_time = max(times_flow_stage[-1], times_samples[-1] * 1.05)
    no_measure_periods.append((times_samples[-1] + 0.001, end_of_time))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(times_flow_stage, h_flow_stage, color='royalblue', linewidth=2)
    ax1.set_ylabel("H (cm)")
    ax1.set_title("(a) Flow surface elevation")

    for start, end in no_measure_periods:
        ax2.axvspan(start, end, color='lightgray', alpha=0.4)

    mask_valid = np.ones_like(Qs_samples, dtype=bool)
    for start, end in no_measure_periods:
        mask_valid &= ~((times_samples >= start) & (times_samples <= end))

    ax2.bar(times_samples[mask_valid], Qs_samples[mask_valid], width=3,
            color='lightcoral', label='Sampled outlet sediment flux')
    ax2.axhline(Qs_inlet_value, color='blue', linewidth=1,
                label='Storage area inlet sediment flux')

    ax2.set_ylabel("Qs (g/s)")
    ax2.set_xlabel("Time (s)")
    ax2.set_title("(b) Solid discharge")
    ax2.legend(fontsize=9, loc='upper right')

    ax1.set_xlim(0, no_measure_periods[-1][1])
    ax2.set_xlim(0, no_measure_periods[-1][1])

    plt.tight_layout()
    plt.show()

# ================================================================
# 4. FIGURE 7 — GSD + Débit solide total
# ================================================================
def figure_7(fig7_grains):
    """
    Trace la Figure 7 : distribution granulométrique du débit solide
    sous forme de barres empilées avec lignes verticales pour les
    temps d'échantillonnage.

    Parameters
    ----------
    fig7_grains : pd.DataFrame
        Contient 'time_sample' et les colonnes des classes de grains.

    Returns
    -------
    None.
    """
    times = fig7_grains["time_sample"].values
    GSD = fig7_grains.iloc[:, 1:].values

    grain_classes = [
        "D > 12.5 mm", "10 mm < D < 12.5 mm", "8 mm < D < 10 mm",
        "6.3 mm < D < 8 mm", "4 mm < D < 6.3 mm", "3.15 mm < D < 4 mm",
        "2 mm < D < 3.15 mm", "D < 2 mm"
    ]
    colors = [
        "#1a1a1a", "#4c2b1f", "#6b3c25", "#8d522d",
        "#b56a2d", "#d68d3a", "#f2b45b", "#ffcc80"
    ]

    fig, ax = plt.subplots(figsize=(14, 6))
    bar_width = 5

    ax.bar(times, GSD[:, 0], color=colors[0], edgecolor='black',
           linewidth=0.8, width=bar_width, label=grain_classes[0])
    bottom = GSD[:, 0].copy()
    for i in range(1, GSD.shape[1]):
        ax.bar(times, GSD[:, i], bottom=bottom, color=colors[i],
               edgecolor='black', linewidth=0.5, width=bar_width,
               label=grain_classes[i])
        bottom += GSD[:, i]

    sampling_times = [472.4, 617.1, 1112.4, 1241.9, 1327.6, 1413.3]
    for t in sampling_times:
        ax.axvline(t, color='black', linestyle='--', linewidth=1)

    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Q$_s$ (g s$^{-1}$)", fontsize=12)
    ax.set_title("Solid Discharge and Grain Size Distribution", fontsize=14)

    ax.set_xlim(400, 1450)
    ax.set_ylim(0, np.max(bottom) * 1.1)

    ax.legend(fontsize=9, framealpha=1, loc='upper center', ncol=1)
    plt.tight_layout()
    plt.show()

# ================================================================
# 5. POINT D'ENTRÉE DU SCRIPT
# ================================================================
if __name__ == "__main__":
    dir_path = get_script_directory()

    fig6, fig6_samples = load_fig6_data(dir_path)
    figure_6(fig6, fig6_samples)

    fig7_grains, fig7_freq, fig7_time_seismic = load_fig7_data(dir_path)
    figure_7(fig7_grains)
