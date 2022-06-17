import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showerror


from PIL import Image
from PIL import ImageTk

from definition import ASSET_DIR, DATA_DIR
import os.path

from variable import COULEUR_BLANC, COULEUR_NOIR, TAILLE_CASE, TAILLE_PLATEAU, NOMBRE_CASE_PLATEAU, TAILLE_FENETRE, COULEUR_PION_BLANC_1, COULEUR_PION_BLANC_2, COULEUR_PION_NOIR_1, COULEUR_PION_NOIR_2, fichier_en_lecture
import variable

from utils import recuperer_sauvegarde
from jeu import Jeu as Jeu_plateau
from dame import partie_fini
from data_json import set_data_path_json, get_data_json, set_data_json

import time
import copy

class MenuBar(tk.Menu):
    def __init__(self, root, app):
        tk.Menu.__init__(self, root)
        self.app = app

        self.menu_fichier = tk.Menu(self, tearoff=0)
        self.menu_fichier.add_command(label="Nouvelle partie", command=self.nouvelle_partie)
        self.menu_fichier.add_command(label="Sauvegarder", command=self.sauvegarder_fichier)
        self.menu_fichier.add_command(label="Ouvrir fichier", command=self.ouvrir_fichier)
        self.menu_fichier.add_command(label="Quitter", command=self.quitter)
        self.add_cascade(label="Fichier", menu=self.menu_fichier)

    def nouvelle_partie(self):
        set_data_json(variable.fichier_en_lecture, {})
        self.app.jeu.actualisation(self.app.bot, self.app.difficulte)
        

    def ouvrir_fichier(self):
        fichier = tk.filedialog.askopenfilename(initialdir = DATA_DIR, title = "Ouvrir fichier",filetypes = [("Json File", "*.json")])
        variable.fichier_en_lecture = fichier.split('/')[-1]
        self.app.jeu.actualisation(self.app.bot, self.app.difficulte)

    def sauvegarder_fichier(self):
        fichier = tk.filedialog.asksaveasfilename(initialdir = DATA_DIR, title = "Sauvegarder vers",filetypes = [("Json File", "*.json")]) + ".json"
        set_data_path_json(fichier, get_data_json(variable.fichier_en_lecture))
    
    def quitter(self):
        self.app.root.destroy()



class App(ttk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
    
        self.menu_accueil = MenuAccueil(self)
        self.menu_difficultes = MenuDifficultes(self)
        self.jeu = Jeu(self)

        self.bot = False
        self.difficulte = "moyen"
       
        self.frames = {"menu accueil": self.menu_accueil, "menu difficultes": self.menu_difficultes, "jeu": self.jeu}
        self.display_frame = self.frames["menu accueil"]
        self.display_frame.pack(fill="both", expand=True)

    def change_frame(self, name: str, bot=False, difficulte="moyen"):
        self.display_frame.pack_forget()
        self.display_frame = self.frames[name]
        self.display_frame.pack(fill="both", expand=True)
        if name == "jeu":
            self.bot = bot
            self.difficulte = difficulte
            self.display_frame.actualisation(bot, difficulte)
            

        
class MenuAccueil(ttk.Frame):
    def __init__(self, root: App):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.initialisation()
    
    def initialisation(self):
        self.label_menu_name = ttk.Label(self, text="Mode de Jeu")
        self.label_menu_name.pack(fill="x", side="top")

        self.boutton_joueur_contre_joueur = ttk.Button(self, text="joueur contre joueur", command=lambda:self.root.change_frame("jeu"))
        self.boutton_joueur_contre_joueur.pack(fill="x")
        self.boutton_joueur_contre_ordi = ttk.Button(self, text="joueur contre ordinateur", command=lambda:self.root.change_frame("menu difficultes"))
        self.boutton_joueur_contre_ordi.pack(fill="x")

class MenuDifficultes(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.initialisation()
    
    def initialisation(self):
        self.label_menu_name = ttk.Label(self, text="Difficultés ordinateur")
        self.label_menu_name.pack(fill="x", side="top")
        self.boutton_niveau_facile = ttk.Button(self, text="facile", command=lambda:self.root.change_frame("jeu", True, "facile"))
        self.boutton_niveau_facile.pack(fill="x", padx=(150,150), pady=(2,0))
        self.boutton_niveau_moyen = ttk.Button(self, text="moyen", command=lambda:self.root.change_frame("jeu", True, "moyen"))
        self.boutton_niveau_moyen.pack(fill="x", padx=(150,150), pady=(2,0))
        self.boutton_niveau_difficile = ttk.Button(self, text="difficile", command=lambda:self.root.change_frame("jeu", True, "difficile"))
        self.boutton_niveau_difficile.pack(fill="x", padx=(150,150), pady=(2,0))

        self.boutton_retour = ttk.Button(self, text="Retour", command=lambda:self.root.change_frame("menu accueil"))
        self.boutton_retour.pack(side="bottom")


class Jeu(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.initialisation()
        

    def actualisation(self, bot, difficulte):
        self.fin = False
        self.gagnant = 0
        self.dernier_plateau = True
        self.nb_tour = 1
        self.jeu = Jeu_plateau(bot, difficulte)
        self.joueur = None
        self.pion_selectionne = None
        self.pions_selectionnable = []
        self.case_jouable = []
        self.canvas_plateau.creation_plateau()
        self.frame_righbar.frame_historique.reinitialiser_historique()
        self.initialisation_historique()
        self.frame_righbar.frame_historique.recuperer_dernier()
        self.canvas_plateau.creation_pions(self.jeu.plateau.recuperer_plateau())
        self.frame_righbar.label_timer.reinitialisation()
        score = self.jeu.plateau.score()
        self.frame_righbar.label_score.changer(score)

        self.debut_tour()
        
        

    def initialisation(self):
        self.canvas_plateau = Plateau(self)
        self.canvas_plateau.pack(side="left", fill="both")

        self.frame_righbar = RightBar(self)
        self.frame_righbar.pack(side="right")
    
    def initialisation_historique(self):
        partie = recuperer_sauvegarde(variable.fichier_en_lecture)
        if partie:
            i = 0
            for clee, valeur in partie.items():
                if clee == "j1" or clee == "j2":
                    continue
                manoury = valeur["manoury"][-1][-1] 
                joueur = 1 if i % 2 == 0 else -1
                self.frame_righbar.frame_historique.ajouter(manoury, joueur, valeur["plateau"])
                i += 1

    def debut_tour(self):
        tour_bot = self.jeu.tour_bot_jouer()
        self.joueur = self.jeu.recuperer_joueur()
        if partie_fini(self.jeu.plateau.recuperer_plateau()):
            self.fin = True
            self.gagnant = -self.joueur.joueur
        if self.fin:
            self.canvas_plateau.partie_fini_canvas(self.gagnant)
        else:
            self.effacer_pion_jouable()
            self.pions_selectionnable = []
            self.effacer_pion_selectionner()
            self.pion_selectionne = None
            self.effacer_case_jouable()
            self.case_jouable = []
            if tour_bot:
                self.jouer_bot()
            else:
                self.joueur.coups_possibles()
                self.pions_selectionnable = self.joueur.pions_jouable()
                if not self.pions_selectionnable:
                    self.canvas_plateau.partie_fini_canvas(-self.joueur.joueur)
                else:
                    self.colorier_pion_jouable()


    def colorier_pion_jouable(self):
        for pion in self.pions_selectionnable:
            self.canvas_plateau.creation_case_colore_canvas(pion[1], pion[0], "red")

    def effacer_pion_jouable(self):
        for pion in self.pions_selectionnable:
            self.canvas_plateau.creation_case_canvas(pion[1], pion[0], COULEUR_NOIR)
            valeur = self.jeu.plateau.recuperer_plateau()[pion[0]][pion[1]]
            self.canvas_plateau.creation_pion(pion[1], pion[0], valeur)
    
    def colorier_case_jouable(self):
        for case in self.case_jouable:
            self.canvas_plateau.creation_point_couleur_canvas(case[1], case[0], "green")

    def effacer_case_jouable(self):
        for case in self.case_jouable:
            self.canvas_plateau.creation_case_canvas(case[1], case[0], COULEUR_NOIR)
            valeur = self.jeu.plateau.recuperer_plateau()[case[0]][case[1]]
            self.canvas_plateau.creation_pion(case[1], case[0], valeur)

    def colorier_pion_selectionner(self):
        if self.pion_selectionne:
            self.canvas_plateau.creation_case_colore_canvas(self.pion_selectionne[0], self.pion_selectionne[1], "grey")

    def effacer_pion_selectionner(self):
        if self.pion_selectionne:
            self.canvas_plateau.creation_case_canvas(self.pion_selectionne[0], self.pion_selectionne[1], COULEUR_NOIR)
            valeur = self.jeu.plateau.recuperer_plateau()[self.pion_selectionne[1]][self.pion_selectionne[0]]
            self.canvas_plateau.creation_pion(self.pion_selectionne[0], self.pion_selectionne[1], valeur)
            if [self.pion_selectionne[1], self.pion_selectionne[0]] in self.pions_selectionnable:
                self.canvas_plateau.creation_case_colore_canvas(self.pion_selectionne[0], self.pion_selectionne[1], "red")


    def fin_tour(self):
        self.jeu.sauvegarder()
        self.jeu.fin_tour()
        
        # add historique with plateau save
        self.frame_righbar.frame_historique.ajouter(self.jeu.mouvements_manoury[-1][-1], self.joueur.joueur, copy.deepcopy(self.jeu.plateau.recuperer_plateau()))
        self.frame_righbar.frame_historique.recuperer_dernier()

        self.frame_righbar.label_timer.reinitialisation()
        score = self.jeu.plateau.score()
        self.frame_righbar.label_score.changer(score)
        self.debut_tour()

    def jouer_bot(self):
        if self.jeu.mouvements_manoury:
            self.joueur.placer_manoury(self.jeu.mouvements_manoury)
        self.joueur.placer_plateau(copy.deepcopy(self.jeu.plateau.recuperer_plateau()))
        mouvement = self.joueur.best_move()
        # coup ob
        if mouvement:
            if isinstance(mouvement[0][0], list):
                coordonnees_pion_a_jouer = mouvement[0][0]
                for coup in mouvement[0][1:]:
                    # self.after(1000)
                    self.jeu.plateau.deplacement_pion(coordonnees_pion_a_jouer[0], coordonnees_pion_a_jouer[1], coup[0], coup[1])
                    valeur = self.jeu.plateau.recuperer_plateau()[coup[0]][coup[1]]
                    self.canvas_plateau.mouvement_pion(coordonnees_pion_a_jouer[1], coordonnees_pion_a_jouer[0], coup[1], coup[0], valeur)
                    coordonnees_pion_a_jouer = coup
                    
                for pion_mange in mouvement[1]:
                    self.jeu.plateau.manger_pion(pion_mange[0], pion_mange[1])
                    self.canvas_plateau.manger_pion(pion_mange[1], pion_mange[0])
            # coup norm
            elif isinstance(mouvement[0][0], int):
                self.jeu.plateau.deplacement_pion(mouvement[0][0], mouvement[0][1], mouvement[1][0], mouvement[1][1])
                valeur = self.jeu.plateau.recuperer_plateau()[mouvement[1][0]][mouvement[1][1]]
                self.canvas_plateau.mouvement_pion(mouvement[0][1], mouvement[0][0], mouvement[1][1], mouvement[1][0], valeur)
            self.jeu.sauvegarde_manoury(mouvement)
            self.fin_tour()
        else:
            self.fin = True
            self.gagnant = -self.joueur.joueur
            self.fin_tour()

    def jouer_joueur(self, x: int, y: int):
        if not self.dernier_plateau:
            return

        for pion in self.pions_selectionnable:
            if pion == [y, x]:
                self.effacer_pion_selectionner()
                self.pion_selectionne = [x, y]
                self.colorier_pion_selectionner()
                self.effacer_case_jouable()
                self.case_jouable = self.joueur.prochain_case_possible([y, x])
                self.colorier_case_jouable()
            
        for case in self.case_jouable:
            if case == [y, x]:
                coordonnees_pion_a_jouer = [self.pion_selectionne[1], self.pion_selectionne[0]]
                coordonnees_pion_deplacement = [y, x]
                if self.joueur.coups_ob:
                    self.effacer_pion_selectionner()
                    self.effacer_case_jouable()
                    pion_mange = self.joueur.pions_mangeable(self.case_jouable, coordonnees_pion_a_jouer, coordonnees_pion_deplacement)
                    peut_rejouer = self.joueur.jouer_coup_obliatoire(coordonnees_pion_a_jouer, coordonnees_pion_deplacement, pion_mange)
                    valeur = self.jeu.plateau.recuperer_plateau()[y][x]
                    self.canvas_plateau.mouvement_pion(self.pion_selectionne[0], self.pion_selectionne[1], x, y, valeur)
                    if peut_rejouer:
                        self.pion_selectionne = [x, y]
                        self.colorier_pion_selectionner()
                        self.case_jouable = self.joueur.prochain_case_possible([y, x])
                        self.colorier_case_jouable()
                        self.effacer_pion_jouable()
                        self.pions_selectionnable = [[x, y]]
                    else:
                        mouvement = self.joueur.fin_du_tour()
                        self.jeu.sauvegarde_manoury(mouvement)
                        for pion_mange in mouvement[1]:
                            self.canvas_plateau.manger_pion(pion_mange[1], pion_mange[0])
                        self.fin_tour()
                elif self.joueur.coups_norm:
                    self.joueur.jouer_coup_normal(coordonnees_pion_a_jouer, coordonnees_pion_deplacement)
                    valeur = self.jeu.plateau.recuperer_plateau()[y][x]
                    self.canvas_plateau.mouvement_pion(self.pion_selectionne[0], self.pion_selectionne[1], x, y, valeur=valeur)
                    self.pion_selectionne = [x, y]
                    mouvement = self.joueur.fin_du_tour()
                    self.jeu.sauvegarde_manoury(mouvement)
                    self.fin_tour()
                    
    


class Plateau(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=TAILLE_PLATEAU[0], height=TAILLE_PLATEAU[1])
        self.root = root
        self.initialisation()

        self.bind("<Button-1>", self.clicked)

    def clicked(self, event):
        x, y = self.coordonnees_case_plateau(event.x, event.y)
        self.root.jouer_joueur(x, y)

    def initialisation(self):
        self.creation_plateau()
    
    def coordonnees_case_plateau(self, x, y):
        return x // TAILLE_CASE, y // TAILLE_CASE

    def couleur_case(self, x: int, y: int):
        return COULEUR_BLANC if ((NOMBRE_CASE_PLATEAU+1)*y+x) % 2 == 0 else COULEUR_NOIR
    
    def couleur_pion(self, valeur: int):
        if valeur > 0:
            return COULEUR_PION_BLANC_1, COULEUR_PION_BLANC_2
        elif valeur < 0:
            return COULEUR_PION_NOIR_1, COULEUR_PION_NOIR_2

    def creation_plateau(self):
        for i in range(NOMBRE_CASE_PLATEAU):
            for j in range(NOMBRE_CASE_PLATEAU):
                couleur = self.couleur_case(j, i)
                self.creation_case_canvas(j, i, couleur)

    def creation_pion(self, x: int, y: int, valeur: int):
        if valeur != 0:
            couleur1, couleur2 = self.couleur_pion(valeur)
            valeur = abs(valeur)
            if valeur == 1:
                self.creation_pion_canvas(x, y, couleur1, couleur2)
            elif valeur == 10:
                self.creation_dame_canvas(x, y, couleur1, couleur2)


    def creation_pions(self, plateau: list):
        taille = len(plateau)
        for i in range(taille):
            for j in range(taille):
                valeur = plateau[i][j]
                if not valeur:
                    continue
                self.creation_pion(j, i, valeur)
                

    def coordonnes_case_canvas(self, x: int, y: int):
        return (x * TAILLE_CASE, y * TAILLE_CASE)

    def creation_case_canvas(self, x: int, y: int, couleur):
        coord_x, coord_y = self.coordonnes_case_canvas(x, y)
        self.create_rectangle(coord_x, coord_y, coord_x + TAILLE_CASE, coord_y + TAILLE_CASE, fill=couleur, outline=couleur)
    
    def creation_pion_canvas(self, x: int, y: int, couleur1, couleur2):
        # ROND
        coord_x, coord_y = self.coordonnes_case_canvas(x, y)
        self.create_oval(coord_x + 8, coord_y + 8, coord_x + TAILLE_CASE - 8, coord_y + TAILLE_CASE - 8, fill=couleur1, outline=couleur1)
        self.create_oval(coord_x + 20, coord_y + 20, coord_x + TAILLE_CASE - 20, coord_y + TAILLE_CASE - 20, width = 3, outline = couleur2)

    def creation_dame_canvas(self, x: int, y: int, couleur1, couleur2):
        # ETOILE
        coord_x, coord_y = self.coordonnes_case_canvas(x, y)
        self.create_oval(coord_x + 8, coord_y + 8, coord_x + TAILLE_CASE - 8, coord_y + TAILLE_CASE - 8, fill=couleur1, outline=couleur1)
        self.create_polygon(coord_x + 14, coord_y+TAILLE_CASE//2, coord_x+TAILLE_CASE//2, coord_y + 14, coord_x+TAILLE_CASE - 14, coord_y+TAILLE_CASE//2, coord_x+TAILLE_CASE//2, coord_y+TAILLE_CASE - 14, width = 3, fill=couleur2)
    
    def creation_case_colore_canvas(self, x: int, y: int, couleur):
        coord_x, coord_y = self.coordonnes_case_canvas(x, y)
        self.create_rectangle(coord_x + 1, coord_y + 1, coord_x + TAILLE_CASE - 1, coord_y + TAILLE_CASE - 1, width= 3, outline=couleur)

    def creation_point_couleur_canvas(self, x: int, y: int, couleur):
        coord_x, coord_y = self.coordonnes_case_canvas(x, y)
        self.create_oval(coord_x + 20, coord_y + 20, coord_x + TAILLE_CASE - 20, coord_y + TAILLE_CASE - 20, width = 0, fill = couleur)

    def mouvement_pion(self, x: int, y: int, nouveau_x: int, nouveau_y: int, valeur: int):
        couleur_case = self.couleur_case(x, y)
        self.creation_case_canvas(x, y, couleur_case)
        self.creation_pion(nouveau_x, nouveau_y, valeur=valeur)
    
    def manger_pion(self, x: int, y: int):
        couleur_case = self.couleur_case(x, y)
        self.creation_case_canvas(x, y, couleur_case)

    def partie_fini_canvas(self, couleur):
        txt = "Le joueur BLANC a gagné" if couleur == 1 else "Le joueur NOIR a gagné"
        self.create_text(TAILLE_PLATEAU[0] // 2, TAILLE_PLATEAU[1] // 2, text=txt, fill="red", font=('Helvetica 26 bold'))

class RightBar(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root, width=TAILLE_FENETRE[0] - TAILLE_PLATEAU[0], height=TAILLE_FENETRE[1] - TAILLE_PLATEAU[1])
        self.root = root
        self.initialisation()

    def initialisation(self):
        self.label_score = ScoreLabel(self)
        self.label_score.pack(side="top", fill="x")
        self.frame_historique = HistoriqueFrame(self)
        self.frame_historique.pack(side="top", fill="both", expand=True)
        self.label_timer = TimerLabel(self)
        self.label_timer.pack(side="top", fill="x")

class TimerLabel(ttk.Label):
    def __init__(self, root):
        ttk.Label.__init__(self, root)
        self.configure(font=("Courier", 36))
        self.root = root
        self.compteur = 0
        self.afficher()
        self.after(1000, self.ajouter)

    def reinitialisation(self):
        self.compteur = 0
        self.afficher()
    
    def ajouter(self):
        self.compteur += 1
        self.afficher()
        self.after(1000, self.ajouter)
    
    def afficher(self):
        self.config(text=str(self.compteur))

class ScoreLabel(ttk.Label):
    def __init__(self, root):
        ttk.Label.__init__(self, root)
        self.configure(font=("Courier", 36))
        self.root = root
        self.changer(0)
    
    def changer(self, score: str):
        self['text'] = score


class HistoriqueFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root, width=TAILLE_FENETRE[0]-TAILLE_PLATEAU[0]-100, height=TAILLE_FENETRE[1]-180)
        self.root = root
        self.numero = 2
        self.indicateur = 0
        self.indicateur_joueur = 1
        self.ligne_historique = []
        self.initialisation()

    def initialisation(self):
        self.canvas = tk.Canvas(self, width=200)
        self.canvas.grid(row=0, column=0, columnspan=4, sticky="nw")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=5, rowspan=5, sticky="ns")
        self.frame_historique_ligne_conteneur = ttk.Frame(self.canvas)
        self.frame_historique_ligne_conteneur.pack(fill="both", expand=True)
        self.frame_historique_ligne_conteneur.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame_historique_ligne_conteneur, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        self.img_fleche_path = os.path.join(ASSET_DIR, "right-arrow.png")
        self.img_double_fleche_path = os.path.join(ASSET_DIR, "right-double-arrow.png")

        self.img_premier = Image.open(self.img_double_fleche_path)
        self.img_premier = self.img_premier.resize((20, 20), Image.ANTIALIAS)
        self.img_premier = self.img_premier.rotate(180)
        self.photo_premier= ImageTk.PhotoImage(self.img_premier)
        self.boutton_premier_coup = ttk.Button(self, image=self.photo_premier, command=lambda:self.changer_plateau(self.recuperer_premier()))
        self.boutton_premier_coup.grid(row=1, column=0)

        self.img_avant = Image.open(self.img_fleche_path)
        self.img_avant = self.img_avant.resize((20, 20), Image.ANTIALIAS)
        self.img_avant = self.img_avant.rotate(180)
        self.photo_avant = ImageTk.PhotoImage(self.img_avant)
        self.boutton_coup_avant = ttk.Button(self, image=self.photo_avant, command=lambda:self.changer_plateau(self.recuperer_precedant()))
        self.boutton_coup_avant.grid(row=1, column=1)

        self.img_apres = Image.open(self.img_fleche_path)
        self.img_apres = self.img_apres.resize((20, 20), Image.ANTIALIAS)
        self.photo_apres = ImageTk.PhotoImage(self.img_apres)
        self.boutton_coup_apres = ttk.Button(self, image=self.photo_apres, command=lambda:self.changer_plateau(self.recuperer_suivant()))
        self.boutton_coup_apres.grid(row=1, column=2)

        self.img_dernier = Image.open(self.img_double_fleche_path)
        self.img_dernier = self.img_dernier.resize((20, 20), Image.ANTIALIAS)
        self.photo_dernier= ImageTk.PhotoImage(self.img_dernier)
        self.boutton_dernier_coup = ttk.Button(self, image=self.photo_dernier, command=lambda:self.changer_plateau(self.recuperer_dernier()))
        self.boutton_dernier_coup.grid(row=1, column=3)
    
    def ajouter(self, manoury, joueur, plateau):
        if joueur == 1:
            ligne_historique = HistoriqueLigneFrame(self.frame_historique_ligne_conteneur, self, self.numero // 2)
            ligne_historique.coup_premier_joueur(manoury, plateau)
            ligne_historique.pack(side="top")
            self.ligne_historique.append(ligne_historique)
        else:
            ligne_historique = self.ligne_historique[-1]
            ligne_historique.coup_deuxieme_joueur(manoury, plateau)
        self.numero += 1

    def changer_plateau(self, plateau):
        self.root.root.canvas_plateau.creation_plateau()
        if self.root.root.dernier_plateau:
            self.root.root.canvas_plateau.creation_pions(plateau)
            self.root.root.debut_tour()
        else:
            self.root.root.canvas_plateau.creation_pions(plateau)


    def recuperer_plateau_indicateur(self):
        return self.ligne_historique[self.indicateur].plateau_j1 if self.indicateur_joueur == 1 else self.ligne_historique[self.indicateur].plateau_j2

    def recuperer_precedant(self):
        if self.indicateur_joueur == 1:
            self.indicateur = max(0, self.indicateur - 1)
        if self.indicateur == 0 and self.indicateur_joueur == 1:
            pass
        else:
            self.indicateur_joueur = -self.indicateur_joueur     
        plateau = self.recuperer_plateau_indicateur()
        if plateau != self.dernier_plateau():
            self.root.root.dernier_plateau = False
        else:
            self.root.root.dernier_plateau = True
        return plateau
        
    def recuperer_suivant(self):
        if self.indicateur_joueur == -1:
            self.indicateur = min(len(self.ligne_historique), self.indicateur + 1)
        if self.indicateur == len(self.ligne_historique) - 1:
            if self.ligne_historique[self.indicateur].plateau_j2 is not None:
                self.indicateur_joueur = -1
            else:
                self.indicateur_joueur = 1
        else:
            self.indicateur_joueur = -self.indicateur_joueur  
        plateau = self.recuperer_plateau_indicateur()
        if plateau != self.dernier_plateau():
            self.root.root.dernier_plateau = False
        else:
            self.root.root.dernier_plateau = True
        return plateau

    def recuperer_premier(self):
        self.indicateur = 0
        self.indicateur_joueur = 1
        plateau = self.recuperer_plateau_indicateur()
        if plateau != self.dernier_plateau():
            self.root.root.dernier_plateau = False
        else:
            self.root.root.dernier_plateau = True
        return plateau

    def recuperer_dernier(self):
        self.indicateur = len(self.ligne_historique) - 1
        if self.indicateur != -1:
            if self.ligne_historique[self.indicateur].plateau_j2 is not None:
                self.indicateur_joueur = -1
            else:
                self.indicateur_joueur = 1    
            self.root.root.dernier_plateau = True
            return self.recuperer_plateau_indicateur()
        else:
            return []
    
    def dernier_plateau(self):
        indicateur = len(self.ligne_historique) - 1
        if indicateur != -1:
            if self.ligne_historique[indicateur].plateau_j2 is not None:
                indicateur_joueur = -1
            else:
                indicateur_joueur = 1    
            return self.ligne_historique[indicateur].plateau_j1 if indicateur_joueur == 1 else self.ligne_historique[indicateur].plateau_j2
        else:
            return []

    def reinitialiser_historique(self):
        for ligne in self.ligne_historique:
            ligne.pack_forget()
        self.ligne_historique = []
        self.numero = 2



class HistoriqueLigneFrame(ttk.Frame):
    def __init__(self, root, historique_frame, numero):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.historique_frame = historique_frame
        self.numero = numero
        self.plateau_j1 = None
        self.plateau_j2 = None

        self.initialisation()

    def initialisation(self):
        self.label_numero_tour = ttk.Label(self, text=str(self.numero)+'.')
        self.label_numero_tour.pack(side="left")
        self.boutton_coup_premier_joueur = ttk.Button(self)
        self.boutton_coup_premier_joueur.pack(side="left", fill="x")
        self.boutton_coup_deuxieme_joueur = ttk.Button(self)
        self.boutton_coup_deuxieme_joueur.pack(side="left", fill="x")
    
    def coup_premier_joueur(self, coup_manory, plateau):
        self.boutton_coup_premier_joueur['text'] = coup_manory
        self.boutton_coup_premier_joueur.configure(command=lambda:self.clicked(plateau, 1))
        self.plateau_j1 = plateau
    
    def coup_deuxieme_joueur(self, coup_manory, plateau):
        self.boutton_coup_deuxieme_joueur['text'] = coup_manory
        self.boutton_coup_deuxieme_joueur.configure(command=lambda:self.clicked(plateau, -1))
        self.plateau_j2 = plateau
    
    def clicked(self, plateau, joueur):
        if self.historique_frame.dernier_plateau() != plateau:
            self.historique_frame.root.root.dernier_plateau = False
        else:
            self.historique_frame.root.root.dernier_plateau = True
        self.historique_frame.indicateur = self.numero-1
        self.historique_frame.indicateur_joueur = joueur
        self.historique_frame.changer_plateau(plateau)
        
root = tk.Tk()
root.geometry(str(TAILLE_FENETRE[0])+"x"+str(TAILLE_FENETRE[1]))
root.resizable(False, False)
root.title("JEU DE DAME")
interface = App(root)
interface.pack(fill="both", expand=True)
menubar = MenuBar(root, interface)
root.config(menu=menubar)
root.mainloop()