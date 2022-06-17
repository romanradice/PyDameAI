from plateau import Plateau
from pion import Pion, creation_pion
from data_json import add_data_json, set_data_json, get_data_json

import random
import variable

def sauvegarder_plateau(num_coup, plateau, manoury):
    tour = {num_coup: {"plateau": plateau, "manoury": manoury}}
    add_data_json(variable.fichier_en_lecture, tour)

def sauvegarder_type_joueur(j1, j2):
    tour = {"j1": j1, "j2": j2}
    add_data_json(variable.fichier_en_lecture, tour)

def supprimer_plateau_sauvegarde(fichier):
    set_data_json(fichier, {})

def recuperer_sauvegarde(fichier):
    return get_data_json(fichier)

def recuperer_manoury(fichier):
    partie = get_data_json(fichier)
    if partie:
        dernier_plateau_index = "0a"
        for clee in partie.keys():
            if clee == "j1" or clee == "j2":
                continue
            dernier_plateau_index = clee if int(clee[:-1]) >= int(dernier_plateau_index[:-1]) else dernier_plateau_index
        return partie[dernier_plateau_index]["manoury"]

def recuperer_plateau_sauvegarde(fichier) -> Plateau:
    partie = get_data_json(fichier)
    if partie:
        dernier_plateau_index = "0a"
        for clee in partie.keys():
            if clee == "j1" or clee == "j2":
                continue
            dernier_plateau_index = clee if int(clee[:-1]) >= int(dernier_plateau_index[:-1]) else dernier_plateau_index
        plateau_list = partie[dernier_plateau_index]["plateau"]
        pions = creation_pion_avec_plateau(plateau_list)
        return Plateau(pions)

def numero_coup_partie_en_cours() -> tuple:
    partie = get_data_json(variable.fichier_en_lecture)
    if partie:
        dernier_plateau_index = "0a"
        for clee in partie.keys():
            if clee == "j1" or clee == "j2":
                continue
            dernier_plateau_index = clee if int(clee[:-1]) >= int(dernier_plateau_index[:-1]) else dernier_plateau_index
        tour = int(dernier_plateau_index[:-1])
        if tour == 0:
            return (0, 0)
        joueur = -1
        if "b" in dernier_plateau_index:
            tour += 1
            joueur = 1
        return (tour, joueur)
    else:
        return (0, 0)

def manoury_vers_coordonnes(valeur: int):
    valeur = int(valeur)
    return [(valeur - 1) // 5, 2 * ((valeur - 1) % 5) + (((valeur - 1) // 5) + 1) % 2]

def coordonnes_vers_manoury(y: int, x: int):
    return (y * 5 + x // 2) + 1

def recuperer_coup_manory():
    manory = []
    partie = get_data_json(variable.fichier_en_lecture)
    if partie:
        for clee,valeur in partie.items():
            if clee == "j1" or clee == "j2":
                continue
            if clee[-1] == "a":
                manory.append([])
            manory[-1].append(valeur["manoury"])
    return manory

def coup_vers_manoury(mouvement: list):
    manoury = ""
    if isinstance(mouvement[0][0], list):
        manoury = str(coordonnes_vers_manoury(mouvement[0][0][0], mouvement[0][0][1])) + "x" + str(coordonnes_vers_manoury(mouvement[0][-1][0], mouvement[0][-1][1]))
    else:
        manoury = str(coordonnes_vers_manoury(mouvement[0][0], mouvement[0][1])) + "-" + str(coordonnes_vers_manoury(mouvement[1][0], mouvement[1][1]))
    return manoury

def creation_pion_avec_plateau(plateau: list) -> list:
    taille_plateau = len(plateau)
    pions = []
    for y in range(taille_plateau):
        for x in range(taille_plateau):
            couleur = plateau[y][x]
            if couleur:
                if couleur % 10 == 0:
                    pion = creation_pion(x,y,couleur//10,True)
                else:
                    pion = creation_pion(x,y,couleur,False)
                pions.append(pion)
    return pions