# -*- coding: utf-8 -*-
'''
Module permettant de jouer au jeu Quoridor contre un server.
'''


from api import lister_parties, initialiser_partie, jouer_coup
from quoridor import afficher_damier_ascii, analyser_commande


if __name__ == "__main__":

    ARGS = analyser_commande()
    ID_PARTIE = initialiser_partie(ARGS.idul)[0]
    GRILLE = initialiser_partie(ARGS.idul)[1]

    if ARGS.lister:
        print(lister_parties(ARGS.idul))

    WIN = False

    while not WIN:

        afficher_damier_ascii(GRILLE)

        TYPE_COUP = input(
            "Quel type de coup voulez vous effectuer ?\n 'D' pour déplacer le jeton,\n'MH' pour placer un mur horizontal,\n'MV' pour placer un mur vertical.\nType: ")
        TYPE_COUP = TYPE_COUP.upper()
        if TYPE_COUP == '':
            TYPE_COUP = 'D'

        ISINT = False
        while not ISINT:
            try:
                POS_X = int(input("Coordonnée en 'x'? "))
                POS_Y = int(input("Coordonnée en 'y'? "))
                ISINT = True
            except ValueError:
                print('La valeur entrée est invalide.')
        POSITION = (POS_X, POS_Y)

        GRILLE = jouer_coup(ID_PARTIE, TYPE_COUP, POSITION)
