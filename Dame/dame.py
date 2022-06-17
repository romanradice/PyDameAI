import copy
from pion import Pion
from variable import COEFFICIENTS

def coordonne_valide(y, x) -> bool:
    """
		renvoie True si 0 <= x < 10 et 0 <= y < 10, False sinon
	"""
    return 0 <= x < 10 and 0 <= y < 10

def partie_fini(plateau):
    score_b = 0
    score_n = 0
    for i in range(len(plateau)):
        for j in range(len(plateau)):
            if plateau[i][j] > 0 :
                score_b += plateau[i][j]
            elif plateau[i][j] < 0:
                score_n += plateau[i][j]
    return score_n == 0 or score_b == 0

def score_plateau(plateau):
    score = 0
    for i in range(len(plateau)):
        for j in range(len(plateau)):
            score += plateau[i][j]
    return score

def recuperer_pions(plateau: list):
    pions = []
    for i in range(len(plateau)):
        for j in range(len(plateau)):
            couleur = plateau[i][j]
            if couleur:
                pions.append([i, j, couleur])
    return pions

def pions_par_couleur(pions, couleur):
        pions_couleur = []
        for pion in pions:
            if pion[2] == couleur or pion[2] == couleur * 10:
                pions_couleur.append(pion)
        return pions_couleur

def joue_coup_obligatoire(plateau: list, pions: list, mouvement: list):
    position_debut = mouvement[0][0]
    position_fin = mouvement[0][-1]
    plateau[position_fin[0]][position_fin[1]] = plateau[position_debut[0]][position_debut[1]]
    plateau[position_debut[0]][position_debut[1]] = 0
    if isinstance(pions[0], (list)): 
        for i in range(len(pions)):
            if pions[i][:2] == position_debut:
                pions[i] = position_fin+[pions[i][2]]
    else:
        if pions[:2] == position_debut:
            pions = position_fin+[pions[2]]
    for i in range(len(mouvement[1])):
        mort_y, mort_x  = mouvement[1][i]
        pions.remove([mort_y, mort_x, plateau[mort_y][mort_x]])
        plateau[mort_y][mort_x] = 0
    return plateau, pions

def joue_coup_normaux(plateau: list, pions: list, mouvement: list):
    if len(pions) >= 2: 
        for i in range(len(pions)):
            if pions[i][:2] == mouvement[0]:
                pions[i] = mouvement[1]+[pions[i][2]]
    else:
        if pions[:2] == mouvement[0]:
            pions[i] = mouvement[1]+[pions[2]]
    plateau[mouvement[1][0]][mouvement[1][1]] = plateau[mouvement[0][0]][mouvement[0][1]]
    plateau[mouvement[0][0]][mouvement[0][1]] = 0
    return plateau, pions

def coups_normaux_liste_pions(plateau: list, pions: list[list[int, int, int]], couleur: int):
    coups_normaux = []
    for pion in pions:
        dame = True if pion[2] == 10 or pion[2] == -10 else False
        coup = dame_mouvement_normal(plateau, [pion[0], pion[1]]) if dame \
            else pion_mouvement_normal(plateau, [pion[0], pion[1]], pion[2])
        if coup:
            coups_normaux.append([coup])
    return coups_normaux

def coups_normaux_pions(plateau: list, pions: list[Pion], couleur: int):
    """
	renvoie la liste des coups possibles d'un pion
	plateau : list, liste de tout les pions; couleur : int, couleur du pion
	"""
    coups_normaux = []
    for pion in pions:
        coup = dame_mouvement_normal(plateau, [pion.position_y, pion.position_x]) if pion.dame \
            else pion_mouvement_normal(plateau, [pion.position_y, pion.position_x], pion.couleur)
        if coup:
            coups_normaux.append([coup])
    return coups_normaux

def coups_obligatoires_list_pions(plateau: list, pions: list[list[int, int, int]], couleur: int) -> list:
    coups_obligatoires = []
    nb_coups_max = 1
    for pion in pions:
        plateau[pion[0]][pion[1]] = 0
        dame = True if pion[2] == 10 or pion[2] == -10 else False
        coups = dame_mange_rec(plateau, [pion[0], pion[1]], pion[2], sauvegarde=[[[], []]]) if dame \
            else pion_mange_rec(plateau, [pion[0], pion[1]], pion[2], sauvegarde=[[[], []]])
        plateau[pion[0]][pion[1]] = pion[2] 
        for coup in coups:
            if len(coup[0]) > nb_coups_max:
                coups_obligatoires = [coup]
                nb_coups_max = len(coup[0])
            elif len(coup[0]) == nb_coups_max:
                coups_obligatoires.append(coup)
    return coups_obligatoires

def coups_obligatoires_pions(plateau: list, pions: list[Pion], couleur: int) -> list:
    """
	renvoie la liste des coups obligatoires du pion
	"""
    coups_obligatoires = []
    nb_coups_max = 1
    for pion in pions:
        couleur = pion.couleur
        plateau[pion.position_y][pion.position_x] = 0
        coups = dame_mange_rec(plateau, [pion.position_y, pion.position_x], couleur, sauvegarde=[[[], []]]) if pion.dame \
            else pion_mange_rec(plateau, [pion.position_y, pion.position_x], couleur, sauvegarde=[[[], []]])
        plateau[pion.position_y][pion.position_x] = couleur   
        for coup in coups:
            if len(coup[0]) > nb_coups_max:
                coups_obligatoires = [coup]
                nb_coups_max = len(coup[0])
            elif len(coup[0]) == nb_coups_max:
                coups_obligatoires.append(coup)
    return coups_obligatoires

def pion_mange_rec(plateau: list, coordonnees: list, couleur: int, sauvegarde=[[[], []]]) -> list:
    """
	mange les pions selon les coups obligatoires, pour un pion
	"""
    deja_mange = [] if not sauvegarde[-1] else sauvegarde[-1][1]
    sauvegarde[-1][0].append(coordonnees)
    coups_possibles = pion_mouvement_manger(plateau, coordonnees, couleur, deja_mange)
    if not coups_possibles:
        return []
    else:
        s = sauvegarde.pop()
        for piece, coup in coups_possibles:
            sauvegarde.append(copy.deepcopy(s))
            sauvegarde[-1][1].append(piece)
            pion_mange_rec(plateau ,coup, couleur, sauvegarde)
        return sauvegarde

def dame_mange_rec(plateau: list, coordonnees: list, couleur: int, sauvegarde=[[[], []]]) -> list:
    """
	mange les pions selon les coups obligatoires, pour une dame
	"""
    deja_mange = [] if not sauvegarde[-1] else sauvegarde[-1][1]
    sauvegarde[-1][0].append(coordonnees)
    coups_possibles = dame_mouvement_manger(plateau, coordonnees, couleur, deja_mange)
    if not coups_possibles:
        return []
    else:
        s = sauvegarde.pop()
        for piece, coup in coups_possibles:
            sauvegarde.append(copy.deepcopy(s))
            sauvegarde[-1][1].append(piece)
            dame_mange_rec(plateau, coup, couleur, sauvegarde)
        return sauvegarde
##

def pion_mouvement_normal(plateau: list, coordonnees: list, couleur: int) -> list:
    mouvements = [coordonnees, []]
    direction = COEFFICIENTS[2:] if couleur > 0 else COEFFICIENTS[:2]
    for c in direction:
        y, x = c
        if coordonne_valide(coordonnees[0] + y, coordonnees[1] + x) and plateau[coordonnees[0] + y][coordonnees[1] + x] == 0:
            mouvements[1].append([coordonnees[0] + y, coordonnees[1] + x])
    return mouvements if mouvements[1] else []

def dame_mouvement_normal(plateau: list, coordonnees: list) -> list:
    mouvements = [coordonnees, []]
    for c in COEFFICIENTS:
        y, x = c
        i = 1
        while coordonne_valide(coordonnees[0] + y * i, coordonnees[1] + x * i) and plateau[coordonnees[0] + y * i][coordonnees[1] + x * i] == 0:
            mouvements[1].append([coordonnees[0] + y * i, coordonnees[1] + x * i])
            i = i + 1
    return mouvements if mouvements[1] else []


def pion_mouvement_manger(plateau: list, coordonnees: list, couleur: int, deja_mange=[]) -> list:
    mouvements = []
    for c in COEFFICIENTS:
        x, y = c
        if coordonne_valide(coordonnees[0] + 2 * y, coordonnees[1] + 2 * x) and (plateau[coordonnees[0] + y][coordonnees[1] + x] == -couleur or plateau[coordonnees[0] + y][coordonnees[1] + x] == -couleur * 10) and [coordonnees[0] + y, coordonnees[1] + x] not in deja_mange:
            if plateau[coordonnees[0] + 2 * y][coordonnees[1] + 2 * x] == 0:
                mouvements.append([[coordonnees[0] + y, coordonnees[1] + x], [coordonnees[0] + 2 * y, coordonnees[1] + 2 * x]])
    return mouvements


def dame_mouvement_manger(plateau: list, coordonnees: list, couleur: int, deja_mange=[]) -> list:
    mouvements = []
    for c in COEFFICIENTS:
        x, y = c
        i, j = 1, 1
        while coordonne_valide(coordonnees[0] + y * (i + 1), coordonnees[1] + x * (i + 1)) and plateau[coordonnees[0] + y * i][
            coordonnees[1] + x * i] == 0:
            i += 1
        if coordonne_valide(coordonnees[0] + y * (i + 1), coordonnees[1] + x * (i + 1)) and [coordonnees[0] + y * i, coordonnees[
                                                                                                            1] + x * i] not in deja_mange and (
                plateau[coordonnees[0] + y * i][coordonnees[1] + x * i] == -couleur or plateau[coordonnees[0] + y * i][
            coordonnees[1] + x * i] == -couleur // 10):
            while coordonne_valide(coordonnees[0] + y * i + y * j, coordonnees[1] + x * i + x * j) and \
                    plateau[coordonnees[0] + y * i + y * j][coordonnees[1] + x * i + x * j] == 0:
                mouvements.append(
                    [[coordonnees[0] + y * i, coordonnees[1] + x * i], [coordonnees[0] + y * i + j * y, coordonnees[1] + x * i + j * x]])
                j += 1
    return mouvements
