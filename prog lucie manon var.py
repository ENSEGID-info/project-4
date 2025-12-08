# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Script unifié: chargement Figures 6,7,S1 + normalisation + analyse corrélations
Coller dans essai_jesp.py, à côté du dossier DATA.
Created on: 2025-12-08
@author: vhava (fusion Eugénie + Manon + Lucie)
"""

import os
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, linregress

# -----------------------------------------------------------
# 0. Utilitaires
# -----------------------------------------------------------

def get_script_directory():
    """Retourne le répertoire où se trouve ce script."""
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def safe_loadtxt(path):
    """Charge un fichier texte si il existe, sinon lève une erreur claire."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    return np.loadtxt(path)

# -----------------------------------------------------------
# 1. Chargement des données (FIG 6, FIG 7, FIG S1)
# -----------------------------------------------------------

def load_fig6_data(base_dir):
    """Charge les fichiers de Fig_6 et renvoie deux DataFrame (fig6, fig6_samples)."""
    p = lambda *parts: os.path.join(base_dir, *parts)
    h_flow_stage = safe_loadtxt(p("DATA", "Fig_6", "Fig6_h_flow_stage.txt"))
    qs_sample = safe_loadtxt(p("DATA", "Fig_6", "Fig6_Qs_samples.txt"))
    time_flow_stage = safe_loadtxt(p("DATA", "Fig_6", "Fig6_time_flow_stage.txt"))
    time_sample = safe_loadtxt(p("DATA", "Fig_6", "Fig6_time_samples.txt"))

    fig6 = pd.DataFrame({
        "time_flow_stage": time_flow_stage,
        "flow_stage": h_flow_stage
    })

    fig6_samples = pd.DataFrame({
        "time_sample": time_sample,
        "qs_sample": qs_sample
    })

    return fig6, fig6_samples

def load_fig7_data(base_dir):
    """Charge les fichiers de Fig_7 et renvoie (fig7_grains, fig7_freq, fig7_time)."""
    p = lambda *parts: os.path.join(base_dir, *parts)
    frequency = safe_loadtxt(p("DATA", "Fig_7", "Fig7_Frequency.txt"))
    Qs_GSD = safe_loadtxt(p("DATA", "Fig_7", "Fig7_Qs_GSD.txt"))
    time_sample = safe_loadtxt(p("DATA", "Fig_7", "Fig7_Time_samples.txt"))
    time_seismic_power = safe_loadtxt(p("DATA", "Fig_7", "Fig7_Time_seismic_power.txt"))

    # Qs_GSD peut être 1D ou 2D ; si 1D, convertir en 2D (une colonne)
    if Qs_GSD.ndim == 1:
        Qs_GSD = Qs_GSD[:, np.newaxis]

    grain_cols = [f"grain_class_{i+1}" for i in range(Qs_GSD.shape[1])]
    fig7_grains = pd.DataFrame(Qs_GSD, columns=grain_cols)
    fig7_grains.insert(0, "time_sample", time_sample)

    fig7_freq = pd.DataFrame({"frequency": frequency})
    fig7_time = pd.DataFrame({"time_seismic_power": time_seismic_power})

    return fig7_grains, fig7_freq, fig7_time

def load_figS1_data(base_dir):
    """Charge les fichiers de Fig_S1 et renvoie (time, power) numpy arrays.
       power est shape (n_time, n_freq) — si 1D, converti en 2D (n_time, 1)."""
    p = lambda *parts: os.path.join(base_dir, *parts)
    seismic_power = safe_loadtxt(p("DATA", "Fig_S1", "S1_Seismic_power.txt"))
    time_seismic_power = safe_loadtxt(p("DATA", "Fig_S1", "S1_Time_seismic_power.txt"))

    # couper au minimum commun
    min_len = min(len(time_seismic_power), seismic_power.shape[0])
    time = time_seismic_power[:min_len]

    power = seismic_power[:min_len]
    if power.ndim == 1:
        power = power[:, np.newaxis]

    return time, power

# -----------------------------------------------------------
# 2. Traitement sismique : normalisation + standardisation
# -----------------------------------------------------------

def normalize_seismic_power(time, power, background_duration=300.0):
    """
    Soustrait le bruit de fond (moyenne temporelle sur les t < background_duration).
    Retourne power_norm (même shape que 'power') et background_mean (par fréquence).
    """
    background_mask = time < background_duration
    if background_mask.sum() == 0:
        # Si aucune fenêtre de bruit choisie, prendre les 10 premières secondes si possible
        fallback_len = min(10, len(time))
        background_mask = np.arange(len(time)) < fallback_len

    background_mean = power[background_mask, :].mean(axis=0)
    power_norm = power - background_mean[np.newaxis, :]
    return power_norm, background_mean

def standardize_power_over_time(power_norm):
    """
    Standardisation par fréquence (centrer/réduire sur chaque colonne = fréquence).
    Retourne power_z (shape identique).
    """
    mean_per_freq = np.mean(power_norm, axis=0)
    std_per_freq = np.std(power_norm, axis=0)
    std_per_freq[std_per_freq == 0] = 1e-12  # éviter division par 0
    power_z = (power_norm - mean_per_freq[np.newaxis, :]) / std_per_freq[np.newaxis, :]
    return power_z

# -----------------------------------------------------------
# 3. Affichage sismique (raw et normalisé)
# -----------------------------------------------------------

def plot_seismic_power(time, power, power_norm):
    """Affiche deux panels : raw power et normalized power (puissance brute & normalisée)."""
    # fréquences hypothétiques si non disponibles
    n_freq = power.shape[1]
    freqs = np.linspace(0, 400, n_freq)

    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    im1 = axs[0].imshow(
        power.T, aspect='auto', origin='lower',
        extent=[time[0], time[-1], freqs[0], freqs[-1]],
        cmap='viridis'
    )
    axs[0].set_ylabel('Frequency (Hz)')
    axs[0].set_title('(a) Raw seismic power')
    fig.colorbar(im1, ax=axs[0], label='Seismic power (units)')

    im2 = axs[1].imshow(
        power_norm.T, aspect='auto', origin='lower',
        extent=[time[0], time[-1], freqs[0], freqs[-1]],
        cmap='viridis'
    )
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Frequency (Hz)')
    axs[1].set_title('(b) Normalized seismic power (background subtracted)')
    fig.colorbar(im2, ax=axs[1], label='Normalized seismic power (units)')

    plt.tight_layout()
    plt.show()

# -----------------------------------------------------------
# 4. Analyse des corrélations + plots (Manon & Lucie)
# -----------------------------------------------------------

def analyse_correls_and_plots(fig6, fig6_samples, fig7_grains, fig7_freq, seismic_time, power_norm, power_z):
    """Construit variables, calcule corrélations, fait heatmap + régressions et autres plots."""
    print("\n--- Début de l'analyse des corrélations ---")

    # Préparer variables (en respectant les noms français demandés)
    # On s'assure que chaque vecteur est 1D numpy
    def to_1d(a):
        a = np.asarray(a)
        if a.ndim == 2 and a.shape[1] == 1:
            return a[:, 0]
        return a.ravel()

    hauteur_flux = to_1d(fig6["flow_stage"].values)
    debit_solide = to_1d(fig6_samples["qs_sample"].values)
    temps_niveau_eau = to_1d(fig6["time_flow_stage"].values)
    temps_echantillons = to_1d(fig6_samples["time_sample"].values)
    frequences_sismiques = to_1d(fig7_freq["frequency"].values) if ("frequency" in fig7_freq.columns) else np.array([])
    # taille moyenne des grains (d50 approximatif par moyenne des classes)
    grain_cols = [c for c in fig7_grains.columns if c != "time_sample"]
    if len(grain_cols) == 0:
        taille_moyenne = np.array([])
        time_d50 = np.array([])
    else:
        taille_moyenne = fig7_grains[grain_cols].mean(axis=1).values
        time_d50 = fig7_grains["time_sample"].values

    # P_norm : moyenne spectrale (ici moyenne de power_z sur les fréquences pour chaque instant)
    P_norm = power_z.mean(axis=1) if power_z is not None else np.array([])

    temps_sismique = seismic_time
    # quelques statistiques sur power_z
    puissance_max = power_z.max(axis=1) if power_z is not None else np.array([])
    puissance_min = power_z.min(axis=1) if power_z is not None else np.array([])
    puissance_std = power_z.std(axis=1) if power_z is not None else np.array([])

    variables_fr = {
        "hauteur_flux_materiau": hauteur_flux,
        "debit_solide_echantillons": debit_solide,
        "temps_niveau_eau": temps_niveau_eau,
        "temps_echantillons": temps_echantillons,
        "frequences_sismiques": frequences_sismiques,
        "taille_particules_moyenne": taille_moyenne,
        "puissance_sismique_normalisee_moyenne": P_norm,
        "temps_sismique": temps_sismique,
        "puissance_sismique_max": puissance_max,
        "puissance_sismique_min": puissance_min,
        "ecart_type_puissance_sismique": puissance_std
    }

    noms_variables = list(variables_fr.keys())
    n_vars = len(noms_variables)

    # Calcul matrice de corrélation (Pearson) — matrice carrée n_vars x n_vars
    matrice_corr = np.full((n_vars, n_vars), np.nan)
    signe_corr = np.full((n_vars, n_vars), "NA", dtype=object)

    for i in range(n_vars):
        for j in range(n_vars):
            x = np.asarray(variables_fr[noms_variables[i]])
            y = np.asarray(variables_fr[noms_variables[j]])
            # si fréquence est vide (vecteur vide) on skip
            if x.size == 0 or y.size == 0:
                continue
            # découper au minimum commun
            min_len = min(len(x), len(y))
            if min_len < 2:
                continue
            x2 = x[:min_len]
            y2 = y[:min_len]
            # vérifier variance non nulle
            if np.nanstd(x2) == 0 or np.nanstd(y2) == 0:
                continue
            try:
                r, p = pearsonr(x2, y2)
            except Exception:
                continue
            matrice_corr[i, j] = r
            if abs(r) > 0.5:
                signe_corr[i, j] = "positive" if r > 0 else "negative"
            else:
                signe_corr[i, j] = "faible"

    df_corr = pd.DataFrame(matrice_corr, index=noms_variables, columns=noms_variables)
    df_signe = pd.DataFrame(signe_corr, index=noms_variables, columns=noms_variables)

    print("\n=== Matrice de corrélation (Pearson) ===")
    print(df_corr.round(2))
    print("\n=== Type de corrélation (positive / negative / faible) ===")
    print(df_signe)

    # Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_corr.astype(float), vmin=-1, vmax=1, cmap="bwr", annot=True, fmt=".2f",
                xticklabels=noms_variables, yticklabels=noms_variables)
    plt.xticks(rotation=45, ha='right')
    plt.title("Matrice de corrélation (Pearson) — variables en français")
    plt.tight_layout()
    plt.show()

    # Extraire paires fortement corrélées |r|>0.5
    print("\n=== Paires fortement corrélées (|r| > 0.5) ===")
    found = False
    for i in range(n_vars):
        for j in range(i+1, n_vars):
            r = matrice_corr[i, j]
            if not np.isnan(r) and abs(r) > 0.5:
                found = True
                print(f"{noms_variables[i]} ↔ {noms_variables[j]} : r = {r:.2f}, type = {signe_corr[i,j]}")
    if not found:
        print("Aucune paire avec |r| > 0.5 trouvée.")

    # -----------------------------------------------------------
    # Régressions et plots ciblés
    # 1) Débit solide (Qs) ↔ taille moyenne d50 (on interpole d50 aux temps de Qs)
    # -----------------------------------------------------------
    try:
        if (len(debit_solide) > 1) and (len(taille_moyenne) > 1):
            # Interpolation de d50 aux instants de Qs
            d50_interp_at_qs = np.interp(temps_echantillons, time_d50, taille_moyenne)
            slope, intercept, r_value, p_value, std_err = linregress(debit_solide, d50_interp_at_qs)
            fit = intercept + slope * debit_solide

            plt.figure(figsize=(7,5))
            plt.scatter(debit_solide, d50_interp_at_qs, alpha=0.7, s=40)
            plt.plot(debit_solide, fit, color='k', lw=1.5, label=f"r={r_value:.2f}")
            plt.xlabel("Débit solide Qs (units)")
            plt.ylabel("Taille moyenne des grains (d50, units)")
            plt.title("Qs ↔ d50 (interpolé)")
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("Erreur Qs↔d50 :", e)

    # -----------------------------------------------------------
    # 2) Puissance sismique moyenne P_norm vs Qs
    # -----------------------------------------------------------
    try:
        if (P_norm.size > 1) and (len(debit_solide) > 1):
            # Interpoler P_norm aux temps de Qs
            P_interp = np.interp(temps_echantillons, temps_sismique[:len(P_norm)], P_norm)
            slope, intercept, r_value, p_value, std_err = linregress(debit_solide, P_interp)
            fit = intercept + slope * debit_solide

            plt.figure(figsize=(7,5))
            plt.scatter(debit_solide, P_interp, alpha=0.7, s=40)
            plt.plot(debit_solide, fit, color='k', lw=1.5, label=f"r={r_value:.2f}")
            plt.xlabel("Débit solide (Qs)")
            plt.ylabel("Puissance sismique normalisée (P_norm)")
            plt.title("Puissance sismique vs Débit solide")
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("Erreur P_norm vs Qs :", e)

    # -----------------------------------------------------------
    # 3) P_norm vs d50
    # -----------------------------------------------------------
    try:
        if (P_norm.size > 1) and (len(taille_moyenne) > 1):
            P_interp = np.interp(time_d50, temps_sismique[:len(P_norm)], P_norm)
            slope, intercept, r_value, p_value, std_err = linregress(taille_moyenne, P_interp)
            fit = intercept + slope * taille_moyenne

            plt.figure(figsize=(7,5))
            plt.scatter(taille_moyenne, P_interp, alpha=0.7, s=40)
            plt.plot(taille_moyenne, fit, color='k', lw=1.5, label=f"r={r_value:.2f}")
            plt.xlabel("Taille moyenne des grains (d50)")
            plt.ylabel("Puissance sismique normalisée (P_norm)")
            plt.title("Puissance sismique vs Taille moyenne des grains")
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("Erreur P_norm vs d50 :", e)

    # -----------------------------------------------------------
    # 4) P_norm vs flow_stage
    # -----------------------------------------------------------
    try:
        if (P_norm.size > 1) and (len(hauteur_flux) > 1):
            P_interp = np.interp(temps_niveau_eau, temps_sismique[:len(P_norm)], P_norm)
            slope, intercept, r_value, p_value, std_err = linregress(hauteur_flux, P_interp)
            fit = intercept + slope * hauteur_flux

            plt.figure(figsize=(7,5))
            plt.scatter(hauteur_flux, P_interp, alpha=0.7, s=40)
            plt.plot(hauteur_flux, fit, color='k', lw=1.5, label=f"r={r_value:.2f}")
            plt.xlabel("Flow stage")
            plt.ylabel("Puissance sismique normalisée (P_norm)")
            plt.title("Puissance sismique vs Flow stage")
            plt.legend()
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("Erreur P_norm vs flow_stage :", e)

    # -----------------------------------------------------------
    # 5) Boxplot hypothétique de phases (front/corps/queue) — si on veut le simuler
    # Ici on n'a pas d'annotation réelle de phase : j'ai gardé un exemple synthétique
    # -----------------------------------------------------------
    try:
        # Si l'utilisateur a une colonne de phase réelle, remplacer ici.
        # Ici on simule pour illustrer la méthode (ne modifie pas les résultats principaux).
        phases = ["front"] * 20 + ["corps"] * 20 + ["queue"] * 20
        power_values = np.concatenate([
            np.random.normal(1.2, 0.2, 20),
            np.random.normal(0.8, 0.2, 20),
            np.random.normal(0.4, 0.2, 20)
        ])
        phase_df = pd.DataFrame({"phase": phases, "P_norm": power_values})
        plt.figure(figsize=(6, 4))
        sns.boxplot(x="phase", y="P_norm", data=phase_df)
        plt.title("Exemple: Puissance sismique selon la phase du pulse (simulée)")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Erreur boxplot phases :", e)

    print("\n--- Fin de l'analyse des corrélations et plots ---")

# -----------------------------------------------------------
# 5. main
# -----------------------------------------------------------

def main():
    base_dir = get_script_directory()
    print("Dossier du script :", base_dir)

    # Charger Fig6, Fig7, FigS1
    try:
        fig6, fig6_samples = load_fig6_data(base_dir)
        print("\nFig6 et échantillons chargés.")
    except Exception as e:
        print("Erreur chargement Fig_6 :", e)
        return

    try:
        fig7_grains, fig7_freq, fig7_time = load_fig7_data(base_dir)
        print("Fig7 chargée.")
    except Exception as e:
        print("Erreur chargement Fig_7 :", e)
        return

    try:
        seismic_time, seismic_power = load_figS1_data(base_dir)
        print("Fig_S1 chargée.")
    except Exception as e:
        print("Erreur chargement Fig_S1 :", e)
        return

    # Normalisation puissance sismique (background)
    power_norm, bg_mean = normalize_seismic_power(seismic_time, seismic_power, background_duration=300.0)
    print("Normalisation sismique effectuée (power_norm calculé).")

    # Standardisation (z-score) par fréquence — utile pour calculs statistiques
    power_z = standardize_power_over_time(power_norm)
    print("Standardisation (z-score) calculée : power_z.")

    # Afficher panels sismiques
    try:
        plot_seismic_power(seismic_time, seismic_power, power_norm)
    except Exception as e:
        print("Erreur lors du tracé sismique :", e)

    # Lancer l'analyse des corrélations et visualisations complémentaires
    try:
        analyse_correls_and_plots(fig6, fig6_samples, fig7_grains, fig7_freq, seismic_time, power_norm, power_z)
    except Exception as e:
        print("Erreur dans analyse_correls_and_plots :", e)

if __name__ == "__main__":
    main()


