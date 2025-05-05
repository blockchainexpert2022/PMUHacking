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

    for i, cote in enumerate(cotes):
        if cote <= 0:
            erreur = f"La cote du cheval {i + 1} est invalide ({cote}). Elle doit être supérieure à 0."
            break
        mise_cheval = gain_cible / cote
        mises.append(mise_cheval)
        mise_totale += mise_cheval

    if erreur:
        return [], 0.0, 0.0, erreur

    profit_theorique = gain_cible - mise_totale

    return mises, mise_totale, profit_theorique, None

def afficher_resultats(mises, mise_totale, profit_theorique, gain_cible):
    """Affiche les résultats du calcul des mises."""
    print("\n--- Résultats de la Répartition des Mises ---")
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
    cotes = [0.0] * 8 # Initialise une liste pour 8 chevaux
    gain_cible = 0.0
    premier_calcul = True

    print("--- Calcul de Répartition des Mises (Jeu Simple Gagnant) ---")
    print("Entrez les rapports probables (cotes pour 1€) et votre gain cible.")
    print("Le script calculera la mise nécessaire sur chaque cheval.")

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

            # Demander les cotes initiales pour les 8 chevaux
            print("\nEntrez les cotes probables pour chaque cheval (par exemple, 3.5 ou 12.0).")
            for i in range(8):
                while True:
                    try:
                        cote_input = input(f"Cote probable pour le cheval {i + 1} : ").replace(',', '.')
                        cote = float(cote_input)
                        if cote <= 0:
                             print("Veuillez entrer une cote positive.")
                        else:
                            cotes[i] = cote
                            break
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer un nombre pour la cote (par exemple, 4.2).")
            premier_calcul = False

        # Effectuer le calcul
        mises, mise_totale, profit_theorique, erreur = calculer_mises(cotes, gain_cible)

        # Afficher les résultats ou l'erreur
        if erreur:
            print(f"\nErreur de calcul : {erreur}")
        else:
            afficher_resultats(mises, mise_totale, profit_theorique, gain_cible)

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
            cotes = [0.0] * 8
            gain_cible = 0.0
        elif choix == 'm':
            while True:
                try:
                    num_cheval_input = input("Numéro du cheval à modifier (1-8) : ").strip()
                    num_cheval = int(num_cheval_input)
                    if 1 <= num_cheval <= 8:
                        break
                    else:
                        print("Numéro de cheval invalide. Veuillez entrer un nombre entre 1 et 8.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro entre 1 et 8.")

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
