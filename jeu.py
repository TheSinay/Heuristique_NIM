# fichier: jeu.py
import heapq
import csv
import random
from datetime import datetime

def afficher_etat(etat_jeu):
    """
    Affiche l'état actuel du jeu en indiquant le nombre d'objets dans chaque tas.
    """
    for i, tas in enumerate(etat_jeu):
        if tas == 1:
            print(f"Tas {i+1}: {tas} objet")
        else:
            print(f"Tas {i+1}: {tas} objets")


def generer_mouvements(etat_jeu):
    """
    Génère tous les mouvements possibles à partir d'un état donné.
    Retourne une liste de nouveaux états obtenus après un mouvement légal.
    """
    mouvements_possibles = []
    
    # Pour chaque tas, essayer de retirer de 1 à n objets
    for i, tas in enumerate(etat_jeu):
        for nb_objets_a_retirer in range(1, min(4,tas + 1)):  # Retirer de 1 à tas objets
            nouvel_etat = etat_jeu.copy()  # Copier l'état actuel du jeu
            nouvel_etat[i] -= nb_objets_a_retirer  # Retirer les objets du tas i
            mouvements_possibles.append(nouvel_etat)  # Ajouter à la liste des mouvements possibles
    
    return mouvements_possibles

def appliquer_mouvement(etat_jeu, tas_index, nb_objets):
    if tas_index < 0 or tas_index >= len(etat_jeu):
        return None
    if nb_objets <= 0 or etat_jeu[tas_index] < nb_objets or nb_objets>4:
        return None
    nouvel_etat = etat_jeu.copy()
    nouvel_etat[tas_index] -= nb_objets
    return nouvel_etat

def heuristique(etat_jeu):
    """
    Fonction heuristique pour estimer le coût restant pour atteindre l'état final (victoire).
    L'heuristique retourne la somme des objets restants dans tous les tas.
    
    Paramètres :
    etat_jeu : liste représentant les tas et le nombre d'objets dans chaque tas
    
    Retourne :
    Une estimation du coût restant pour atteindre la victoire (la somme des objets restants).
    """
    return sum(etat_jeu)


def heuristique_combinee(etat_jeu):
    somme_restante = sum(etat_jeu)
    xor_value = 0
    for tas in etat_jeu:
        xor_value ^= tas
    return somme_restante + xor_value  # Combinaison des deux heuristiques

def etat_final(etat_jeu):
    """
    Vérifie si l'état actuel du jeu est un état final (victoire).
    L'état est final si tous les tas sont vides.
    
    Paramètres :
    etat_jeu : liste représentant les tas et le nombre d'objets dans chaque tas
    
    Retourne :
    True si tous les tas sont vides, sinon False.
    """
    return all(tas == 0 for tas in etat_jeu)

def cout_mouvement(etat_courant, etat_suivant):
    """
    Retourne le coût pour passer d'un état à un autre.
    Dans ce cas, chaque mouvement a un coût fixe de 1.
    
    Paramètres :
    etat_courant : l'état du jeu avant le mouvement
    etat_suivant : l'état du jeu après le mouvement
    
    Retourne :
    Le coût de la transition, ici 1.
    """
    return 1


class Noeud:
    def __init__(self, etat, parent=None, g=0, h=0):
        self.etat = etat
        self.parent = parent
        self.g = g  # Coût réel pour atteindre ce nœud
        self.h = h  # Heuristique
        self.f = g + h  # Coût total f(n) = g(n) + h(n)
    
    def __lt__(self, autre):
        return self.f < autre.f  # Pour la comparaison dans la file de priorité

    def __eq__(self, autre):
        return self.etat == autre.etat  # Pour vérifier si deux états sont identiques

def reconstruire_chemin(self):
        chemin = []
        noeud_actuel = self
        while noeud_actuel is not None:
            chemin.append(noeud_actuel.etat)
            noeud_actuel = noeud_actuel.parent
        return chemin[::-1]



def algorithme_a_star(etat_initial):
    h_initial = heuristique(etat_initial)
    noeud_initial = Noeud(etat=etat_initial, g=0, h=h_initial)
    open_list = []
    heapq.heappush(open_list, noeud_initial)
    closed_set = set()

    while open_list:
        noeud_courant = heapq.heappop(open_list)

        if etat_final(noeud_courant.etat):
            return reconstruire_chemin(noeud_courant)[1]  # Retourne le prochain état optimal

        closed_set.add(tuple(noeud_courant.etat))

        for nouvel_etat in generer_mouvements(noeud_courant.etat):
            nouvel_etat_tuple = tuple(nouvel_etat)
            if nouvel_etat_tuple in closed_set:
                continue

            g_nouveau = noeud_courant.g + 1  # Chaque mouvement a un coût de 1
            h_nouveau = heuristique(nouvel_etat)
            nouveau_noeud = Noeud(etat=nouvel_etat, parent=noeud_courant, g=g_nouveau, h=h_nouveau)

            heapq.heappush(open_list, nouveau_noeud)

    return None


def sauvegarder_historique(id_partie, historique, gagnant):
    """
    Sauvegarde l'historique d'une partie dans un fichier CSV avec encodage UTF-8.
    """
    nom_fichier = f"historique_partie.csv"
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
        
        # Écrire les en-têtes
        writer.writerow(["ID Partie", "Tour", "État Avant Coup", "Action", "Joueur", "État Après Coup"])
        
        # Écrire l'historique
        for ligne in historique:
            writer.writerow([id_partie] + ligne)
        
        # Ajouter le gagnant à la fin
        writer.writerow([id_partie, "Fin", "", "", "", f"Gagnant : {gagnant}"])
    
    print(f"Historique sauvegardé dans {nom_fichier}")

    
def mouvement_aleatoire(etat_jeu):
    """
    Génère un mouvement aléatoire pour l'IA aléatoire.
    
    Paramètres :
    etat_jeu : Liste représentant les tas du jeu de Nim.
    
    Retourne :
    Le nouvel état après un mouvement aléatoire.
    """
    tas_non_vides = [i for i, tas in enumerate(etat_jeu) if tas > 0]  # Trouver les tas non vides
    if not tas_non_vides:
        return None  # Aucun mouvement possible (le jeu est terminé)
    
    # Choisir un tas au hasard parmi les tas non vides
    tas_index = random.choice(tas_non_vides)
    
    # Choisir un nombre d'objets aléatoire à retirer (entre 1 et le nombre d'objets dans ce tas)
    nb_objets_a_retirer = random.randint(1, min(3, etat_jeu[tas_index]))

    
    # Appliquer le mouvement
    nouvel_etat = appliquer_mouvement(etat_jeu, tas_index, nb_objets_a_retirer)
    return nouvel_etat

def boucle_de_jeu_contre_ia(etat_initial):
    etat_jeu = etat_initial
    tour = 1  # 1 = joueur humain, 2 = IA
    num_tour = 0  # Compteur de tours
    historique = []  # Liste pour stocker l'historique des coups
    id_partie = datetime.now().strftime("%Y%m%d%H%M%S")  # Utilisation de la date/heure comme identifiant unique

    while not etat_final(etat_jeu):
        print("\nÉtat actuel du jeu :", etat_jeu)
        etat_avant = etat_jeu.copy()
        num_tour += 1
        if tour == 1:
            print("\nC'est votre tour.")
            # Demander à l'utilisateur de choisir un tas et combien d'objets retirer
            try:
                tas_index = int(input("Choisissez un tas (1, 2 ou 3) : ")) - 1
                nb_objets = int(input("Combien d'objets voulez-vous retirer ? "))
                nouvel_etat = appliquer_mouvement(etat_jeu, tas_index, nb_objets)

                if nouvel_etat is None:
                    print("Mouvement invalide, veuillez réessayer.")
                    continue
                else:
                    etat_jeu = nouvel_etat
                    historique.append([num_tour, etat_avant, f"tas {tas_index + 1}, {nb_objets} objets retirés", "Joueur", etat_jeu])
                    tour = 2  # Passer le tour à l'IA
            except ValueError:
                print("Entrée non valide. Veuillez entrer un nombre entier.")
                continue
        else:
            print("\nTour de l'IA...")
            etat_jeu_suivant = algorithme_a_star(etat_jeu)
            historique.append([num_tour, etat_avant, f"IA joue", "IA", etat_jeu_suivant])
            etat_jeu = etat_jeu_suivant
            print(f"L'IA a joué : {etat_jeu}")
            tour = 1  # Repasser le tour au joueur humain

    # Déterminer le gagnant
    if tour == 1:
        gagnant = "IA"
        print("L'IA a gagné !")
    else:
        gagnant = "Joueur"
        print("Vous avez gagné !")
    
    # Sauvegarder l'historique à la fin de la partie
    sauvegarder_historique(id_partie, historique, gagnant)
    
def boucle_de_jeu_contre_joueur_aleatoire(etat_initial):
    etat_jeu = etat_initial
    tour = 1  # 1 = joueur humain, 2 = IA aléatoire
    num_tour = 0  # Compteur de tours
    historique = []  # Liste pour stocker l'historique des coups
    id_partie = datetime.now().strftime("%Y%m%d%H%M%S")  # Utilisation de la date/heure comme identifiant unique

    while not etat_final(etat_jeu):
        print("\nÉtat actuel du jeu :", etat_jeu)
        etat_avant = etat_jeu.copy()
        num_tour += 1
        if tour == 1:
            print("\nC'est votre tour.")
            # Demander à l'utilisateur de choisir un tas et combien d'objets retirer
            try:
                tas_index = int(input("Choisissez un tas (1, 2 ou 3) : ")) - 1
                nb_objets = int(input("Combien d'objets voulez-vous retirer ? "))
                nouvel_etat = appliquer_mouvement(etat_jeu, tas_index, nb_objets)

                if nouvel_etat is None:
                    print("Mouvement invalide, veuillez réessayer.")
                    continue
                else:
                    etat_jeu = nouvel_etat
                    historique.append([num_tour, etat_avant, f"tas {tas_index + 1}, {nb_objets} objets retirés", "Joueur", etat_jeu])
                    tour = 2  # Passer le tour au joueur aléatoire
            except ValueError:
                print("Entrée non valide. Veuillez entrer un nombre entier.")
                continue
        else:
            print("\nTour du joueur aléatoire...")
            etat_jeu_suivant = mouvement_aleatoire(etat_jeu)
            historique.append([num_tour, etat_avant, f"IA aléatoire joue", "IA Aléatoire", etat_jeu_suivant])
            etat_jeu = etat_jeu_suivant
            print(f"L'IA aléatoire a joué : {etat_jeu}")
            tour = 1  # Repasser le tour au joueur humain

    # Déterminer le gagnant
    if tour == 1:
        gagnant = "IA Aléatoire"
        print("Le joueur aléatoire a gagné !")
    else:
        gagnant = "Joueur"
        print("Vous avez gagné !")
    
    # Sauvegarder l'historique à la fin de la partie
    sauvegarder_historique(id_partie, historique, gagnant)
    
def choix_mode_de_jeu():
    print("Choisissez le mode de jeu :")
    print("1. Jouer contre l'IA (algorithme A*)")
    print("2. Jouer contre un joueur aléatoire")
    print("3. IA (algorithme A*) contre IA aléatoire")
    choix = input("Entrez 1, 2 ou 3 : ")
    return choix



def generer_etat_initial_aleatoire(min_tas=2, max_tas=3, min_objets=1, max_objets=10):
    """
    Génère un état initial aléatoire pour le jeu de Nim.
    
    Paramètres :
    min_tas : Le nombre minimum de tas.
    max_tas : Le nombre maximum de tas.
    min_objets : Le nombre minimum d'objets dans un tas.
    max_objets : Le nombre maximum d'objets dans un tas.
    
    Retourne :
    Une liste représentant les tas avec un nombre d'objets aléatoire.
    """
    # Générer un nombre aléatoire de tas
    nombre_de_tas = random.randint(min_tas, max_tas)
    
    # Générer un nombre d'objets aléatoire pour chaque tas
    etat_initial = [random.randint(min_objets, max_objets) for _ in range(nombre_de_tas)]
    
    return etat_initial


def boucle_ia_vs_ia(etat_initial):
    etat_jeu = etat_initial
    tour = 1  # 1 = IA avec A*, 2 = IA aléatoire
    num_tour = 0  # Compteur de tours
    historique = []  # Liste pour stocker l'historique des coups
    id_partie = datetime.now().strftime("%Y%m%d%H%M%S")  # Utilisation de la date/heure comme identifiant unique

    while not etat_final(etat_jeu):
        print("\nÉtat actuel du jeu :", etat_jeu)
        etat_avant = etat_jeu.copy()
        num_tour += 1

        if tour == 1:
            print("\nTour de l'IA avec A*...")
            etat_jeu_suivant = algorithme_a_star(etat_jeu)
            historique.append([num_tour, etat_avant, f"IA A* joue", "IA A*", etat_jeu_suivant])
            etat_jeu = etat_jeu_suivant
            print(f"L'IA avec A* a joué : {etat_jeu}")
            tour = 2  # Passer le tour à l'IA aléatoire
        else:
            print("\nTour de l'IA aléatoire...")
            etat_jeu_suivant = mouvement_aleatoire(etat_jeu)
            historique.append([num_tour, etat_avant, f"IA aléatoire joue", "IA Aléatoire", etat_jeu_suivant])
            etat_jeu = etat_jeu_suivant
            print(f"L'IA aléatoire a joué : {etat_jeu}")
            tour = 1  # Repasser le tour à l'IA avec A*

    # Déterminer le gagnant
    if tour == 1:
        gagnant = "IA Aléatoire"
        print("L'IA aléatoire a gagné !")
    else:
        gagnant = "IA A*"
        print("L'IA avec A* a gagné !")
    
    # Sauvegarder l'historique à la fin de la partie
    sauvegarder_historique(id_partie, historique, gagnant)


if __name__ == "__main__":
    # Demander à l'utilisateur de choisir l'état initial
    etat_initial = generer_etat_initial_aleatoire()
    
    print("Bienvenue dans le jeu de Nim contre l'IA !")
    print("L'état initial du jeu est :", etat_initial)
    
    # Demander à l'utilisateur de choisir un mode de jeu
    choix = choix_mode_de_jeu()
    
    if choix == "1":
        # Lancer la boucle de jeu contre l'IA stratégique
        boucle_de_jeu_contre_ia(etat_initial)
    elif choix == "2":
        # Lancer la boucle de jeu contre l'IA aléatoire
        boucle_de_jeu_contre_joueur_aleatoire(etat_initial)
    elif choix == "3":
        # Lancer la boucle IA contre IA aléatoire
        boucle_ia_vs_ia(etat_initial)
    else:
        print("Choix invalide. Veuillez redémarrer et choisir 1, 2 ou 3.")
