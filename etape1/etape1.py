def etape1_main():
    print("Exécution de l'étape 1...")
    # Exemple : lecture d’un fichier ou génération de données
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data


# -----------------------------------------------------------
# Analyse de glissements de terrain à partir de données sismiques
# Inspiré de Piantini et al. (2021)

# -----------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr #en fait c'est l'histoire de ce qu'on a fait en stat, avec les corrélations donc si c'est >0 les variables varient dans le même sens et sinon en sens inverse

# -----------------------------------------------------------
# 1. Chargement des données
# -----------------------------------------------------------
