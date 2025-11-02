# ===============================
# Projet Informatique
# Structure du programme principal
# ===============================

# Import des modules écrits par les sous-groupes
import etape1
import etape2
import etape3

def main():
    print("=== Début du programme ===")
    
    # Étape 1 – Préparation ou lecture de données
    print("\n--- Étape 1 : Lecture ou préparation ---")
    data = etape1.etape1_main()
    
    # Étape 2 – Traitement ou analyse
    print("\n--- Étape 2 : Traitement principal ---")
    result = etape2.etape2_main(data)
    
    # Étape 3 – Résultats ou affichage final
    print("\n--- Étape 3 : Résultats ou sortie ---")
    etape3.etape3_main(result)
    
    print("\n=== Fin du programme ===")

if __name__ == "__main__":
    main()

