class Pion():
    def __init__(self, position_x, position_y, dame, couleur, est_vivant):
        """
			- Constructeur de la classe Pion
			- position_x : int, position_y : int sont les positions x et y du pion sur le plateau, dame : bool dame si True, pion si False, couleur : int blanc si 1, noir si -1, est_vivant : bool pion vivant si True mort sinon	
		"""
        self.position_x = position_x
        self.position_y = position_y
        self.dame = dame
        self.couleur = couleur * 10 if self.dame else couleur
        self.est_vivant = est_vivant

    def deplacement(self, pos_arrivee_y, pos_arrivee_x):
        """
			- Methode pour deplacer l'instance de la classe pion
			- pos_arrivee_y : int, pos_arrivee_y : int sont les positions d'arrivee x et y du pion
		"""
        self.position_x = pos_arrivee_x
        self.position_y = pos_arrivee_y

    def devient_dame(self):
        """
			- Methode pour transformer un pion en dame
			- pas d'arguments
		"""
        if not self.dame:
            self.dame = True
            self.couleur = self.couleur * 10

    def mort(self):
        """
			- Methode pour supprimer un pion
			- pas d'arguments
		"""
        self.est_vivant = False
        self.couleur = 0


def creation_pion(x, y, couleur, dame=False):
    """
	- Cree un pion au positions x : int et y : int de la couleur couleur : int
	- renvoie l'objet pion
	"""  
    pion = Pion(x, y, dame, couleur, True)
    return pion