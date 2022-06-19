# PyDame AI

## Projet
Un jeu de dame graphique avec un mode contre ordinateur

## Jeu de dame
Les joueurs jouent chacun à leur tour. Les blancs commencent toujours.
Le but du jeu est de capturer tous les pions adverses.
Si un joueur ne peut plus bouger, même s'il lui reste des pions, il perd la partie.
Chaque pion peut se déplacer d'une case vers l'avant en diagonale.
Un pion arrivant sur la dernière rangée et s'y arrêtant est promu en « dame ».
La dame se déplace sur une même diagonale d'autant de cases qu'elle le désire, en avant et en arrière.

### La prise par un pion

Un pion peut en prendre un autre en sautant par dessus le pion adverse pour se rendre sur la case vide située derrière celui-ci. Le pion sauté est retiré du jeu.
La prise peut également s'effectuer en arrière.
La prise est obligatoire.
Si, après avoir pris un premier pion, vous vous retrouvez de nouveau en position de prise, vous devez continuer, jusqu'à ce que cela ne soit plus possible.
Les pions doivent être enlevés à la fin de la prise et non pas un par un au fur et à mesure.


### La prise majoritaire
Lorsque plusieurs prises sont possibles, il faut toujours prendre du côté du plus grand nombre de pièces.
Cela signifie que si on peut prendre une dame ou deux pions, il faut prendre les deux pions
Dans l'exemple ci-contre, un pion blanc peut prendre un pion noir, mais l'autre pion blanc peut en prendre 3, c'est donc ce coup qui doit être joué.

### La prise par la dame
Puisque la dame a une plus grande marge de manoeuvre, elle a aussi de plus grandes possibilités pour les prises.
La dame doit prendre tout pion situé sur sa diagonale (s'il y a une case libre derrière) et doit changer de direction à chaque fois qu'une  nouvelle prise est possible.
On ne peut passer qu'une seule fois sur un même pion.
En revanche, on peut passer deux fois sur la même case.
Dans cet exemple, la dame blanche peut prendre les 4 pions noirs et pourra s'arrêter au choix sur l'une des 2 cases marquées d'une croix.
Enfin, la partie peut être déclarée nulle si aucun des deux joueurs ne peut prendre toutes les pièces adverses (par exemple 3 dames contre une).

## Ordinateur
Il y a 3 niveaux d'ordinateurs pour le jeu de dame.
L'ordinateur calcul tous les coups possibles et joue un coup en fonction de son niveau.
### Facile
L'ordinateur joue les coups au hasard.
### Moyen
L'ordinateur utilise l'alorithme minimax avec l'élagage alpha-bêta.
L'algorithme minimax (aussi appelé algorithme MinMax) est un algorithme qui s'applique à la théorie des jeux pour les jeux à deux joueurs à somme nulle (et à information complète) consistant à minimiser la perte maximum.
Cet algorithme peut être optimisé grâce à l'implémentation de la technique dite de l'élagage alpha-bêta. L'algorithme alpha bêta accélère la routine de recherche minimax en éliminant les cas qui ne seront pas utilisés. 
### Difficile
L'ordinateur peut être dans 3 états différents.
- L'ouverture
	On récupère les parties de jeu de dame de la ffjd.
	On ne conserve que les 10 premiers coups de chaque partie.
	On joue un coup correspondant à la partie actuelle.
- Le milieu de partie
	L'ordinateur utilise l'algorithme minimax avec l'élagage alpha-bêta.
- La finale
	L'ordinateur utilise l'algorithme minimax avec l'élagage alpha-bêta avec une profondeur plus élevée 

## Video

![Presentation](https://github.com/romanradice/Jeu-De-Dame/blob/main/video/presentation.gif)
