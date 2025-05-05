import sys

def calculer_mises(cotes, gain_cible):
    """
    Calcule la mise nécessaire sur chaque cheval pour atteindre un gain cible
    en fonction des cotes probables.

    Args:
        cotes (list): Une liste des cotes probables (rapports pour 1€) pour chaque cheval.
                      Les indices correspondent au numéro du cheval - 1.
        gain_cible (float): Le montant total que l'on souhaite gagner.

    Returns:
        tuple: Un tuple contenant :
               - list: La liste des mises calculées pour chaque cheval.
               - float: La mise totale nécessaire.
               - float: Le profit théorique (gain_cible - mise_totale).
               - str: Un message d'erreur si les calculs ne sont pas possibles.
    """
    mises = []
    mise_totale = 0.0
    erreur = None

    if gain_cible <= 0:
        return [], 0.0, 0.0, "Le gain cible doit être un nombre positif."
    
    if not cotes: # Gérer le cas où aucune cote n'a été entrée
        return [], 0.0, 0.0, "Aucune cote de cheval n'a été entrée."

    for i, cote in enumerate(cotes):
        # On a déjà validé que les cotes entrées sont > 0 lors de la saisie
        mise_cheval = gain_cible / cote
        mises.append(mise_cheval)
        mise_totale += mise_cheval

    profit_theorique = gain_cible - mise_totale

    return mises, mise_totale, profit_theorique, None

def afficher_resultats(mises, mise_totale, profit_theorique, gain_cible, nb_chevaux):
    """Affiche les résultats du calcul des mises."""
    print("\n--- Résultats de la Répartition des Mises ---")
    print(f"Nombre de chevaux considérés : {nb_chevaux}")
    print(f"Gain cible souhaité : {gain_cible:.2f} €")
    print("-" * 38)
    for i, mise in enumerate(mises):
        print(f"Cheval {i + 1} : Miser {mise:.2f} €")
    print("-" * 38)
    print(f"Mise Totale Estimée : {mise_totale:.2f} €")
    print(f"Profit Théorique Estimé : {profit_theorique:.2f} €")
    print("--------------------------------------------")
    if profit_theorique < 0:
        print("Attention : Avec ces cotes et ce gain cible, la mise totale est supérieure au gain cible.")
        print("Vous êtes en perte théorique même si votre cheval arrive premier.")
    print("Note : Ces calculs sont basés sur les rapports probables et peuvent différer des rapports finaux.")
    print("-" * 38)


# --- Boucle principale du script ---
if __name__ == "__main__":
    cotes = [] # Liste vide pour les cotes
    gain_cible = 0.0
    premier_calcul = True
    nb_chevaux = 0

    print("--- Calcul de Répartition des Mises (Jeu Simple Gagnant) ---")
    print("Entrez les rapports probables (cotes pour 1€) pour chaque cheval.")
    print("Entrez 0 pour arrêter la saisie des cotes.")

    while True:
        if premier_calcul:
            # Demander le gain cible au début
            while True:
                try:
                    gain_cible_input = input("Entrez le gain cible souhaité (par exemple, 500) : ").replace(',', '.')
                    gain_cible = float(gain_cible_input)
                    if gain_cible <= 0:
                        print("Veuillez entrer un nombre positif pour le gain cible.")
                    else:
                        break
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un nombre (par exemple, 500 ou 150.5).")

            # Demander les cotes pour un nombre indéfini de chevaux
            print("\nEntrez les cotes probables (par exemple, 3.5 ou 12.0). Entrez 0 pour terminer.")
            cotes = [] # Réinitialiser la liste des cotes
            i = 0
            while True:
                i += 1
                while True:
                    try:
                        cote_input = input(f"Cote probable pour le cheval {i} : ").replace(',', '.')
                        cote = float(cote_input)
                        if cote == 0:
                            break # Sortie de la boucle de saisie des cotes
                        if cote < 0:
                             print("Veuillez entrer une cote positive ou 0 pour terminer.")
                        else:
                            cotes.append(cote)
                            break # Sortie de la boucle de validation de la cote
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer un nombre pour la cote (par exemple, 4.2).")
                if cote == 0:
                    break # Sortie de la boucle de saisie des chevaux

            nb_chevaux = len(cotes) # Mettre à jour le nombre de chevaux
            if nb_chevaux == 0:
                 print("Aucune cote de cheval n'a été entrée. Nouveau calcul.")
                 continue # Revenir au début de la boucle principale pour redemander le gain cible
                 
            premier_calcul = False # La première saisie est terminée

        # Effectuer le calcul
        mises, mise_totale, profit_theorique, erreur = calculer_mises(cotes, gain_cible)

        # Afficher les résultats ou l'erreur
        if erreur:
            print(f"\nErreur de calcul : {erreur}")
        else:
            afficher_resultats(mises, mise_totale, profit_theorique, gain_cible, nb_chevaux)

        # Demander à l'utilisateur ce qu'il veut faire ensuite
        print("\nOptions :")
        print("  [n] Nouveau calcul (tout effacer)")
        print("  [m] Modifier la cote d'un cheval")
        print("  [g] Modifier le gain cible")
        print("  [q] Quitter")

        choix = input("Votre choix : ").lower().strip()

        if choix == 'q':
            break
        elif choix == 'n':
            premier_calcul = True # Recommence tout
            cotes = []
            gain_cible = 0.0
            nb_chevaux = 0
        elif choix == 'm':
            if nb_chevaux == 0:
                print("Aucune cote n'a été entrée pour le moment.")
                continue

            while True:
                try:
                    num_cheval_input = input(f"Numéro du cheval à modifier (1-{nb_chevaux}) : ").strip()
                    num_cheval = int(num_cheval_input)
                    if 1 <= num_cheval <= nb_chevaux:
                        break
                    else:
                        print(f"Numéro de cheval invalide. Veuillez entrer un nombre entre 1 et {nb_chevaux}.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro.")

            while True:
                try:
                    nouvelle_cote_input = input(f"Nouvelle cote pour le cheval {num_cheval} : ").replace(',', '.')
                    nouvelle_cote = float(nouvelle_cote_input)
                    if nouvelle_cote <= 0:
                         print("Veuillez entrer une cote positive.")
                    else:
                        cotes[num_cheval - 1] = nouvelle_cote # Mettre à jour la cote
                        break
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un nombre pour la cote.")

        elif choix == 'g':
             if nb_chevaux == 0 and not premier_calcul: # Gérer le cas où il n'y a pas encore de chevaux mais on est en mode modification
                 print("Veuillez d'abord entrer les cotes des chevaux.")
                 continue
             
             while True:
                try:
                    nouveau_gain_input = input("Nouveau gain cible souhaité : ").replace(',', '.')
                    nouveau_gain = float(nouveau_gain_input)
                    if nouveau_gain <= 0:
                        print("Veuillez entrer un nombre positif pour le gain cible.")
                    else:
                        gain_cible = nouveau_gain # Mettre à jour le gain cible
                        break
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un nombre.")
        else:
            print("Choix invalide. Veuillez réessayer.")

    print("Fin du script.")
