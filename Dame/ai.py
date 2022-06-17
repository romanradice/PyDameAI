from plateau import Plateau
from dame import recuperer_pions, coups_obligatoires_list_pions, coups_normaux_liste_pions, joue_coup_obligatoire, joue_coup_normaux, partie_fini, pions_par_couleur, score_plateau
from utils import coup_vers_manoury, manoury_vers_coordonnes
from data_txt import recherche_ouverture
import copy
import random
class AI():
    def __init__(self, plateau: list, tour: int, difficulte):
        self.plateau = plateau
        self.pions = recuperer_pions(plateau)
        self.profondeur = 6
        self.joueur = tour
        self.nb_tour = 0
        self.state = "ouverture"
        self.difficulte = difficulte
        self.mouvement = []
        self.mouvements_manoury = []

    def best_move(self):
        """
			renvoie la liste des meilleurs mouvement
		"""
        if self.difficulte == "facile":
            self.mouvement = self.coup_aleatoire(self.plateau, self.pions)
        elif self.difficulte == "moyen":
            self.minimax(self.plateau, self.pions, self.profondeur, -200, 200, self.joueur)
        elif self.difficulte == "difficile":
            if self.state == "ouverture":
                self.mouvement = self.coup_ouverture(self.mouvements_manoury)
            if self.state == "milieu":
                self.minimax(self.plateau, self.pions, self.profondeur, -200, 200, self.joueur)
            if self.state == "finale":
                self.minimax(self.plateau, self.pions, self.profondeur + 3, -200, 200, self.joueur)
            if self.state == "ouverture" and self.nb_tour >= 10:
                self.state == "milieu"
            if (self.state == "ouverture" or self.state == "milieu") and len(pions_par_couleur(self.pions, 1)) <= 5 or len(pions_par_couleur(self.pions, -1)) <= 5:
                self.state == "finale"

        self.nb_tour += 1
        return self.mouvement

    def placer_plateau(self, plateau: list):
        self.plateau = plateau
        self.pions = recuperer_pions(plateau)

    def placer_manoury(self, manoury: list):
        self.mouvements_manoury = manoury

    def jouer_coups_possibles(self, plateau: list, pions: list, tour: int):
        jeu = []
        pions_couleur = pions_par_couleur(pions, tour)
        coups_obligatoires = coups_obligatoires_list_pions(plateau, pions_couleur, tour)
        
        if coups_obligatoires:   
            for coup in coups_obligatoires:
                n_plateau, n_pions = joue_coup_obligatoire(copy.deepcopy(plateau), copy.deepcopy(pions), coup)
                jeu.append([n_plateau, n_pions, coup])
        else:
            coups_normaux = coups_normaux_liste_pions(plateau, pions_couleur, tour)
            if coups_normaux:
                for coup in coups_normaux:
                    for case_possible in coup[0][1]:
                        n_plateau, n_pions = joue_coup_normaux(copy.deepcopy(plateau), copy.deepcopy(pions), [coup[0][0], case_possible])
                        jeu.append([n_plateau, n_pions, [coup[0][0], case_possible]])
        return jeu

    def minimax(self, plateau, pions, depht, alpha, beta, tour):
        if depht == 0 or partie_fini(plateau):
            return score_plateau(plateau)
        jeu = self.jouer_coups_possibles(plateau, pions, tour)
        if tour == 1:
            max_evaluation = -200
            for n_plateau, n_pions, coup in jeu:
                evaluation = self.minimax(n_plateau, n_pions, depht - 1 , alpha, beta, -tour)
                if max_evaluation < evaluation:
                    if (self.profondeur == depht and self.state != "finale") or (self.profondeur == depht+3 and self.state == "finale"):
                        self.mouvement = coup
                    max_evaluation = evaluation
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = 200
            for n_plateau, n_pions, coup in jeu:
                evaluation = self.minimax(n_plateau, n_pions, depht - 1 , alpha, beta, -tour)
                if min_evaluation > evaluation:
                    if (self.profondeur == depht and self.state != "finale") or (self.profondeur == depht+3 and self.state == "finale"):
                        self.mouvement = coup
                    min_evaluation = evaluation
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_evaluation

    def coup_aleatoire(self, plateau, pions):
        pions_couleur = pions_par_couleur(pions, self.joueur)
        coups_obligatoires = coups_obligatoires_list_pions(plateau, pions_couleur, self.joueur)
        if coups_obligatoires:
            return random.choice(coups_obligatoires)
        else:
            coups_normaux = coups_normaux_liste_pions(plateau, pions_couleur, self.joueur)
            if coups_normaux:
                coups = random.choice(coups_normaux)
                return [coups[0][0], random.choice(coups[0][1])]
        return []


    def coup_ouverture(self, debut_coup):
        coups = recherche_ouverture(debut_coup)
        if coups:
            print(len(coups), "ouvertures")
            coup = random.choice(coups)
            if self.joueur == 1:
                prochain_coup = coup[len(debut_coup)][0]
            else:
                prochain_coup = coup[len(debut_coup)-1][1]
            if "x" in prochain_coup:
                manoury = prochain_coup.split("x")
                pions_couleur = pions_par_couleur(self.pions, self.joueur)
                coups_possibles = coups_obligatoires_list_pions(self.plateau, pions_couleur, self.joueur)
                for coup in coups_possibles:
                    if coup[0][0] == manoury_vers_coordonnes(manoury[0]) and coup[0][-1] == manoury_vers_coordonnes(manoury[1]):
                        return coup
            elif "-" in prochain_coup:
                manoury = prochain_coup.split("-")
                pions_couleur = pions_par_couleur(self.pions, self.joueur)
                coups_normaux = coups_normaux_liste_pions(self.plateau, pions_couleur, self.joueur)
                for coup_normal in coups_normaux:
                    for coup in coup_normal[0][1]:
                        if coup_normal[0][0] == manoury_vers_coordonnes(manoury[0]) and coup == manoury_vers_coordonnes(manoury[1]):
                            return [coup_normal[0][0], coup]
        else:
            self.state = "milieu"
            return []

