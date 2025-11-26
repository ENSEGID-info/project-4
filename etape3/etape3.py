import matplotlib as plt

def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

def heatmap(matrice_corr,n_vars,noms_variables):
    # -----------------------------------------------------------
    # Visualisation rapide avec heatmap
    # -----------------------------------------------------------
    plt.figure(figsize=(10, 8))
    plt.imshow(matrice_corr, cmap='bwr', vmin=-1, vmax=1)
    plt.colorbar(label='Corrélation de Pearson')
    plt.xticks(range(n_vars), noms_variables, rotation=45, ha='right')
    plt.yticks(range(n_vars), noms_variables)
    plt.title("Matrice de corrélation entre toutes les variables (en français)")
    plt.tight_layout()
    plt.show()