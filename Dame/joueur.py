from plateau import Plateau


class Joueur:
    def __init__(self, jeu, joueur) -> None:
        self.jeu = jeu
        self.joueur = joueur
        
        self.mouvements = []
        self.pions_manges = []

        self.coup_ob = []
        self.coup_norm = []

    def pions_jouable(self):
        pions_jouables = []
        for coup in self.coups_ob + self.coups_norm:
            if coup[0][0] not in pions_jouables:
                pions_jouables.append(coup[0][0])
        return pions_jouables

    def coups_possibles(self):
        self.coups_ob = self.jeu.coups_obligatoires(self.joueur)
        self.coups_norm = [] if self.coups_ob else self.jeu.coups_normaux(self.joueur)
    
    def prochain_case_possible(self, coordonnees_pion_a_jouer: list):
        prochaine_case_possible = []
        if self.coups_ob:
            liste_coups_possible_pion = [coup for coup in self.coups_ob if coup[0][0] == coordonnees_pion_a_jouer]
            mouvements_possibles = [(coup[0][1], coup[1][0]) for coup in liste_coups_possible_pion]
            for mouvement in mouvements_possibles:
                if mouvement[0] not in prochaine_case_possible:
                    prochaine_case_possible.append(mouvement[0])
        elif self.coups_norm:
            liste_coups_possible_pion = [coup for coup in self.coups_norm if coup[0][0] == coordonnees_pion_a_jouer]
            prochaine_case_possible = [elem for elem in liste_coups_possible_pion[0][0][1]]
        return prochaine_case_possible
    
    def pions_mangeable(self, prochaine_case_possible: list, coordonnees_pion_a_jouer: list, coordonnees_pion_deplacement: list):
        if self.coups_ob:
            liste_coups_possible_pion = [coup for coup in self.coups_ob if coup[0][0] == coordonnees_pion_a_jouer]
            mouvements_possibles = [(coup[0][1], coup[1][0]) for coup in liste_coups_possible_pion]
            return mouvements_possibles[prochaine_case_possible.index(coordonnees_pion_deplacement)][1]


    def demander_case(self, case_possible: list):
        try:
            coordonnees_case = input("saisir les coordonnees de la case a jouer :").split(" ")
            coordonnees_case = [int(coordonnees_case[0]), int(coordonnees_case[1])]  
        except Exception:
            pass
        while coordonnees_case not in case_possible:
            try:
                print("coordonnées invalide")
                coordonnees_case = input("saisir les coordonnees de la case a jouer :").split(" ")
                coordonnees_case = [int(coordonnees_case[0]), int(coordonnees_case[1])]
            except Exception:
                pass
        return coordonnees_case


    def jouer_coup_obliatoire(self, coordonnees_pion_a_jouer: list, coordonnees_pion_deplacement: list, pion_mange: list):
        self.pions_manges.append(pion_mange)
        self.jeu.deplacement_pion(coordonnees_pion_a_jouer[0], coordonnees_pion_a_jouer[1], coordonnees_pion_deplacement[0], coordonnees_pion_deplacement[1])
        self.mouvements.append(coordonnees_pion_a_jouer)
        if len(self.coups_ob[0][0]) > 2:
            coups_ob = []
            for i in range(len(self.coups_ob)):
                if self.coups_ob[i][0][0] == coordonnees_pion_a_jouer:
                    coups_ob.append([self.coups_ob[i][0][1:],self.coups_ob[i][1][1:]])
            self.coups_ob = coups_ob
        else:
            self.coups_ob = []
            self.mouvements.append(coordonnees_pion_deplacement)
            return False
        return True


    def jouer_coup_normal(self, coordonnees_pion_a_jouer: list, coordonnees_pion_deplacement: list):
        self.mouvements = [coordonnees_pion_a_jouer, coordonnees_pion_deplacement]
        self.jeu.deplacement_pion(coordonnees_pion_a_jouer[0], coordonnees_pion_a_jouer[1], coordonnees_pion_deplacement[0], coordonnees_pion_deplacement[1])

    def fin_du_tour(self):
        for pion in self.pions_manges:
            self.jeu.manger_pion(pion[0], pion[1])
        if self.pions_manges:
            coup = [self.mouvements, self.pions_manges]
        else:
            coup = self.mouvements
        self.mouvements = []
        self.pions_manges = []
        return coup