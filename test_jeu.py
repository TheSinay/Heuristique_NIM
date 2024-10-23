# fichier: test_jeu.py

import unittest
from jeu import afficher_etat,generer_mouvements,appliquer_mouvement,heuristique,etat_final,cout_mouvement,algorithme_a_star,boucle_de_jeu_contre_ia
from unittest.mock import patch


class TestNim(unittest.TestCase):
    def test_afficher_etat(self):
        # Capture de la sortie standard pour tester l'affichage
        from io import StringIO
        import sys
        output = StringIO()
        sys.stdout = output

        etat_jeu = [3, 4, 5]
        afficher_etat(etat_jeu)
        expected_output = "Tas 1: 3 objets\nTas 2: 4 objets\nTas 3: 5 objets\n"
        self.assertEqual(output.getvalue(), expected_output)

        sys.stdout = sys.__stdout__

    def test_generer_mouvements(self):
        etat_jeu = [5, 3, 2]
        mouvements = generer_mouvements(etat_jeu)
    
    # Les mouvements attendus pour cet état, avec la règle de max 3 objets retirés
        expected_mouvements = [
        # Retirer des objets du tas 1 (valeur 5, mais max 3 objets peuvent être retirés)
        [4, 3, 2], [3, 3, 2], [2, 3, 2],  # Retirer 1, 2, ou 3 objets du tas 1
        
        # Retirer des objets du tas 2 (valeur 3, donc tous les objets peuvent être retirés)
        [5, 2, 2], [5, 1, 2], [5, 0, 2],  # Retirer 1, 2, ou 3 objets du tas 2
        
        # Retirer des objets du tas 3 (valeur 2, donc max 2 objets peuvent être retirés)
        [5, 3, 1], [5, 3, 0]  # Retirer 1 ou 2 objets du tas 3
        ]
    
        self.assertEqual(mouvements, expected_mouvements)
        
    def test_mouvement_valide(self):
        etat_jeu = [3, 4, 5]
        resultat = appliquer_mouvement(etat_jeu, 1, 3)  # Retirer 3 objets du tas 2
        self.assertEqual(resultat, [3, 1, 5])

    def test_index_invalide(self):
        etat_jeu = [3, 4, 5]
        resultat = appliquer_mouvement(etat_jeu, 3, 1)  # Tas inexistant
        self.assertIsNone(resultat)

    def test_nombre_objets_superieur(self):
        etat_jeu = [3, 4, 5]
        resultat = appliquer_mouvement(etat_jeu, 0, 5)  # Plus d'objets que dans le tas
        self.assertIsNone(resultat)

    def test_nombre_objets_negatif(self):
        etat_jeu = [3, 4, 5]
        resultat = appliquer_mouvement(etat_jeu, 1, -1)  # Retirer un nombre négatif d'objets
        self.assertIsNone(resultat)
    def test_heuristique(self):
        self.assertEqual(heuristique([3, 4, 5]), 12)  # Somme des objets
        self.assertEqual(heuristique([1, 0, 2]), 3)
        self.assertEqual(heuristique([0, 0, 0]), 0)
        
    def test_etat_final(self):
        # Cas où l'état est final (tous les tas sont vides)
        self.assertTrue(etat_final([0, 0, 0]))

        # Cas où l'état n'est pas final (certains tas ne sont pas vides)
        self.assertFalse(etat_final([1, 0, 0]))
        self.assertFalse(etat_final([0, 2, 0]))
        self.assertFalse(etat_final([3, 4, 5]))

    # Test pour la fonction cout_mouvement
    def test_cout_mouvement(self):
        # Quel que soit l'état courant et l'état suivant, le coût doit être toujours de 1
        self.assertEqual(cout_mouvement([3, 4, 5], [3, 4, 4]), 1)
        self.assertEqual(cout_mouvement([1, 0, 0], [0, 0, 0]), 1)
        self.assertEqual(cout_mouvement([0, 1, 0], [0, 0, 0]), 1)
        self.assertEqual(cout_mouvement([3, 3, 3], [2, 3, 3]), 1)
        
    def test_a_star(self):
        etat_initial = [3, 4, 5]
        chemin = algorithme_a_star(etat_initial)
        # Vérifier que le chemin se termine par l'état final (tous les tas vides)
        self.assertEqual(chemin[-1], [0, 0, 0])
        
    def test_a_star_gestion_etats(self):
        etat_initial = [3, 4, 5]
        chemin = algorithme_a_star(etat_initial)
        # Vérifier que le chemin se termine par l'état final (tous les tas vides)
        self.assertEqual(chemin[-1], [0, 0, 0])

    def test_a_star_deja_visite(self):
        # Tester un état simple où certains mouvements peuvent générer des états déjà visités
        etat_initial = [1, 1, 2]
        chemin = algorithme_a_star(etat_initial)
        # Vérifier que l'algorithme trouve le chemin optimal
        self.assertEqual(chemin[-1], [0, 0, 0])
        
    def test_reconstruction_chemin(self):
        etat_initial = [3, 4, 5]
        chemin = algorithme_a_star(etat_initial)
        # Vérifier que le chemin se termine par l'état final (tous les tas vides)
        self.assertEqual(chemin[-1], [0, 0, 0])

        # Vérifier que le premier état du chemin est bien l'état initial
        self.assertEqual(chemin[0], etat_initial)

    def test_chemin_simple(self):
        etat_initial = [1, 1, 1]
        chemin = algorithme_a_star(etat_initial)
        self.assertEqual(chemin[-1], [0, 0, 0])  # Doit terminer par l'état final
    
  
   
        
if __name__ == '__main__':
    unittest.main()