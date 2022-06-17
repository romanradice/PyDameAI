from joueur import Joueur
from utils import numero_coup_partie_en_cours, recuperer_plateau_sauvegarde, creation_pion_avec_plateau, coup_vers_manoury, sauvegarder_plateau, recuperer_manoury, sauvegarder_type_joueur, recuperer_sauvegarde
from plateau import Plateau
from ai import AI
from dame import partie_fini

import variable

import random
import copy


plateau = [ [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
            [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] ]



class Jeu:
    def __init__(self, bot: bool, difficulte="moyen"):
        self.bot = bot
        self.difficulte = difficulte

        self.plateau_sauvegarde = []
        self.mouvements = []
        self.mouvements_manoury = []
        self.joueurs = []

        self.fin = False
        self.initialisation_plateau()
        self.initialisation_joueur()
    
    def sauvegarder(self):
        self.plateau_sauvegarde.append(self.plateau.recuperer_plateau())
        num_coup = str(self.tour)+"a" if self.joueur == 1 else str(self.tour)+"b"
        sauvegarder_plateau(num_coup, self.plateau.recuperer_plateau(), self.mouvements_manoury)

    def sauvegarde_manoury(self, mouvement: list):
        if self.joueur == 1:
            self.mouvements_manoury.append([coup_vers_manoury(mouvement)])
        else:
            self.mouvements_manoury[-1].append(coup_vers_manoury(mouvement))

    def initialisation_plateau(self):
        self.tour = 1
        self.joueur = 1
        numero = numero_coup_partie_en_cours()
        if numero == (0, 0):
            pions = creation_pion_avec_plateau(plateau)
            self.plateau = Plateau(pions)
        else:
            self.tour,self.joueur = numero
            self.plateau = recuperer_plateau_sauvegarde(variable.fichier_en_lecture)
            self.mouvements_manoury = recuperer_manoury(variable.fichier_en_lecture)

    def initialisation_joueur(self):
        tour = random.choice([-1,1])
        if numero_coup_partie_en_cours() == (0, 0):
            self.j1 = AI(self.plateau.recuperer_plateau(), tour, self.difficulte) if self.bot else Joueur(self.plateau, tour)
            self.j2 = Joueur(self.plateau, -tour)
            self.joueurs = [self.j1, self.j2] if tour == 1 else [self.j2, self.j1]
            if not self.bot:
                sauvegarder_type_joueur("joueur", "joueur")
            else:
                j1 = "joueur" if tour == -1 else "bot"
                j2 = "joueur" if tour == 1 else "bot"
                sauvegarder_type_joueur(j1, j2)
        else:
            partie = recuperer_sauvegarde(variable.fichier_en_lecture)
            if partie["j1"] == "bot" :
                self.j1 = AI(self.plateau.recuperer_plateau(), 1, self.difficulte)
                self.j2 = Joueur(self.plateau, -1)
                self.joueurs = [self.j1, self.j2]
            elif partie["j2"] == "bot":
                self.j1 = AI(self.plateau.recuperer_plateau(), -1, self.difficulte)
                self.j2 = Joueur(self.plateau, 1)
                self.joueurs = [self.j2, self.j1]
            else:
                self.j1 = Joueur(self.plateau, -1)
                self.j2 = Joueur(self.plateau, 1)
                self.joueurs = [self.j2, self.j1]


    def fin_tour(self):
        if self.joueur == -1:
            self.tour += 1
        self.joueur = -self.joueur

    
    def jouer_coup_bot_console(self):
        if self.mouvements_manoury:
            self.j1.placer_manoury(self.mouvements_manoury)
        self.j1.placer_plateau(copy.deepcopy(self.plateau.recuperer_plateau()))
        mouvement = self.j1.best_move()
        # coup ob
        if len(mouvement):
            if isinstance(mouvement[0][0], list):
                self.plateau.deplacement_pion(mouvement[0][0][0], mouvement[0][0][1], mouvement[0][-1][0], mouvement[0][-1][1])
                for pion_mange in mouvement[1]:
                    self.plateau.manger_pion(pion_mange[0], pion_mange[1])
            # coup norm
            elif isinstance(mouvement[0][0], int):
                self.plateau.deplacement_pion(mouvement[0][0], mouvement[0][1], mouvement[1][0], mouvement[1][1])

            self.mouvements.append(mouvement)
            self.sauvegarde_manoury(mouvement)
        else:
            self.fin = True
            print("vous avez perdu")
            print("Le joueur", -self.j1.joueur, "a gagné")

    def jouer_coup_joueur_console(self, joueur: Joueur):
        joueur.coups_possibles()
        pions_jouables = joueur.pions_jouable()
        self.plateau.afficher()
        if pions_jouables and (joueur.coups_ob or joueur.coups_norm):
            print("c'est au tour du joueur", joueur.joueur, "de jouer")
            print("les pions qui peuvent bouger sont:",pions_jouables)
            coordonnees_pion_a_jouer = joueur.demander_case(pions_jouables)
            case_possible = joueur.prochain_case_possible(coordonnees_pion_a_jouer)
            if joueur.coups_ob:
                print("vous pouvez aller vers les cases", case_possible)
                coordonnees_pion_deplacement = joueur.demander_case(case_possible)
                pion_mange = joueur.pions_mangeable(case_possible, coordonnees_pion_a_jouer, coordonnees_pion_deplacement)
                peut_rejouer = joueur.jouer_coup_obliatoire(coordonnees_pion_a_jouer, coordonnees_pion_deplacement, pion_mange)
                while peut_rejouer:
                    coordonnees_pion_a_jouer = coordonnees_pion_deplacement
                    case_possible = joueur.prochain_case_possible(coordonnees_pion_a_jouer)
                    print("vous pouvez manger et vous déplacer vers les cases", case_possible)
                    coordonnees_pion_deplacement = joueur.demander_case(case_possible)
                    pion_mange = joueur.pions_mangeable(case_possible, coordonnees_pion_a_jouer, coordonnees_pion_deplacement)
                    print(pion_mange)
                    peut_rejouer = joueur.jouer_coup_obliatoire(coordonnees_pion_a_jouer, coordonnees_pion_deplacement, pion_mange)
            else:
                print("vous pouvez vous déplacer vers les cases", case_possible)
                coordonnees_pion_deplacement = joueur.demander_case(case_possible)
                joueur.jouer_coup_normal(coordonnees_pion_a_jouer, coordonnees_pion_deplacement)
            mouvement = joueur.fin_du_tour()
            self.mouvements.append(mouvement)
            self.sauvegarde_manoury(mouvement)
        else:
            self.fin = True
            print("vous avez perdu")
            print("Le joueur", -joueur.joueur, "a gagné")
    
    def tour_bot_jouer(self):
        joueur = self.joueurs[0] if self.joueur == 1 else self.joueurs[1]
        return self.bot and joueur == self.j1

    def jouer_console(self):
        while not self.fin:
            joueur = self.recuperer_joueur()
            print(self.joueur)
            if self.tour_bot_jouer():
                self.jouer_coup_bot_console()
                self.plateau.afficher()
            else:
                self.jouer_coup_joueur_console(joueur)
            self.sauvegarder()
            self.fin_tour()

            if partie_fini(self.plateau.recuperer_plateau()):
                self.fin = True
                print("Le joueur", -joueur.joueur, "a gagné")
            print("----------------------------------------------------------------------------------------------------")

    def recuperer_joueur(self):
        return self.joueurs[0] if self.joueur == 1 else self.joueurs[1]
