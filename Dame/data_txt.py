from definition import DATA_DIR
import os.path


fichiers_txt = ["checkers.txt"]
def nettoyer_fichier(fichiers: list):
    ouverture = True
    fichier_propre = []
    for fichier_txt in fichiers:
        with open(os.path.join(DATA_DIR, fichier_txt), "r") as fichier:
            lignes = fichier.readlines()
            for ligne in lignes:
                ligne = ligne.replace("\n", "")
                if not ouverture and "[Result" in ligne:
                    ouverture = True
                elif ouverture and ligne and ligne[0] != "[" and ligne[0] != "\n":
                    try:
                        index = ligne.index("11.")
                        fichier_propre.append(ligne[:index]+"\n")
                        ouverture = False
                    except ValueError:
                        fichier_propre.append(ligne)
    with open(os.path.join(DATA_DIR, "checkers"+".txt"), "w") as fichier:
        fichier.writelines(fichier_propre)


def recuperer_ouverture():
    parties_coups = []
    for fichier_txt in fichiers_txt:
        with open(os.path.join(DATA_DIR, fichier_txt), "r") as fichier:
            lignes = fichier.readlines()
        for ligne in lignes:
            coups = []
            for i in range(1, 10):
                index_debut = ligne.index(str(i)+".")
                index_fin = ligne.index(str(i+1)+".")
                coup = ligne[index_debut+3:index_fin-1].split(" ")
                coups.append(coup)
            parties_coups.append(coups)
    return parties_coups


def recherche_ouverture(debut_partie=[]):
    ouvertures_valide = []
    ouvertures = recuperer_ouverture()
    for ouverture in ouvertures:
        est_valide = True
        if len(ouverture) < len(debut_partie):
            continue
        for i in range(len(debut_partie)):
            for j in range(len(debut_partie[i])):
                if debut_partie[i][j] != ouverture[i][j]: 
                    est_valide = False
        if est_valide:
            ouvertures_valide.append(ouverture)
    return ouvertures_valide

# fichiers_n = ["cannes-2020-serie1.txt", "cannes-2020-serie2.txt", "Chartres2014_nationale.txt", "chptFrance_2012.txt", "online.txt", "parthenay2014.txt"]
# nettoyer_fichier(fichiers_n)
