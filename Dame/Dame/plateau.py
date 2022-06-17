from pion import Pion
from dame import coups_obligatoires_pions, coups_normaux_pions
from variable import PLATEAU
import copy

class Plateau:
    def __init__(self, pions: list[Pion]):
        """
			- Constructeur de la classe Plateau
			- pions : list
		"""
        self.pions = pions
        self.plateau = list()
        self.actualiser_plateau()

    def reinitialiser_plateau(self):
        """
			Methode pour reinitialiser le plateau, remettre les valeurs du tableau a 0
		"""
        self.plateau = [[0] * PLATEAU for i in range(PLATEAU)]

    def actualiser_plateau(self):
        """
			Methode pour actualiser le plateau, actualise les positions des pions
		"""
        self.reinitialiser_plateau()
        for pion in self.pions:
            y_pos, x_pos = pion.position_y, pion.position_x
            self.plateau[y_pos][x_pos] = pion.couleur

    def recuperer_plateau(self):
        """
			retourne l'instance du plateau
		"""
        return self.plateau

    def afficher(self):
        """
			Affiche le plateau dans la console
		"""
        for i in range(PLATEAU):
            for j in range(PLATEAU):
                print(self.plateau[i][j], "\t", end="")
            print("\t")
            print()

    def score(self):
        """
			renvoie le score du joueur da la couleur
		"""
        score = 0
        for pion in self.pions:
            score += pion.couleur
        return score
    
    def recuperer_pion(self, position_y, position_x) -> Pion:
        """
			Renvoie l'instance du pion possedant les coordonnees rentrees
			position_y : int, position_x : int, les potitions x et y du pion que l'on veut recuperer
		"""
        for pion in self.pions:
            if pion.position_x == position_x and pion.position_y == position_y:
                return pion

    def pions_existe(self, position_y, position_x, couleur) -> bool:
        for pion in self.pions:
            if pion.position_x == position_x and pion.position_y == position_y and pion.couleur == couleur:
                return True
        return False
    
    def manger_pion(self, position_y, position_x):
        pion = self.recuperer_pion(position_y, position_x)
        pion.mort()
        self.plateau[position_y][position_x] = 0
        self.pions.remove(pion)
    
    def deplacement_pion(self, position_y, position_x, position_arrivee_y, position_arrivee_x):
        pion = self.recuperer_pion(position_y, position_x)
        pion.deplacement(position_arrivee_y, position_arrivee_x)
        if (pion.couleur == -1 and pion.position_y == 9) or (pion.couleur == 1 and pion.position_y == 0):
            pion.devient_dame()
        self.plateau[position_y][position_x] = 0
        self.plateau[position_arrivee_y][position_arrivee_x] = pion.couleur
        
    def coups_normaux(self, couleur: int):
        pions = self.recuperer_pions_par_couleur(couleur)
        pions = [pion for pion in pions if pion.est_vivant]
        plateau = self.recuperer_plateau()
        return coups_normaux_pions(plateau, pions, couleur)

    def coups_obligatoires(self, couleur: int) -> list:
        pions = self.recuperer_pions_par_couleur(couleur)
        pions = [pion for pion in pions if pion.est_vivant]
        plateau = self.recuperer_plateau()
        return coups_obligatoires_pions(plateau, pions, couleur)

    def recuperer_pions_par_couleur(self, couleur: int):
        pions = [pion for pion in self.pions if pion.couleur == couleur or pion.couleur == couleur * 10]
        return pions
    
    def partie_fini(self, couleur):
        pions = self.recuperer_pions_par_couleur(couleur)
        for pion in pions:
            if pion.est_vivant:
                return False
        return True

