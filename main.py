# -*- coding: utf-8 -*-
'''
Module permettant de jouer au jeu Quoridor contre un server.
'''

import time
import argparse
from api import initialiser_partie, jouer_coup
import quoridor
import quoridorx


def analyser_commande():
    '''
    Permet d'analyser la commande de l'utilisateur.
    '''
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 3')
    parser.add_argument(dest='idul', help='IDUL du joueur.')
    parser.add_argument('-a', '--automatique', dest='automatique', action='store_true',
                        help='Activer le mode automatique.')
    parser.add_argument('-x', '--graphique', dest='graphique', action='store_true',
                        help='Activer le mode graphique.')
    return parser.parse_args()


if __name__ == "__main__":
    ARGS = analyser_commande()
    ID_PARTIE = initialiser_partie(ARGS.idul)[0]
    GRILLE = initialiser_partie(ARGS.idul)[1]
    if ARGS.graphique:
        PARTIE = quoridorx.QuoridorX(GRILLE['joueurs'], GRILLE['murs'])
        PARTIE.automatique = ARGS.automatique
        PARTIE.id = ID_PARTIE
    else:
        PARTIE = quoridor.Quoridor(GRILLE['joueurs'], GRILLE['murs'])
    WIN = False
    while not WIN:
        PARTIE.afficher()
        if not ARGS.automatique:
            TYPE_COUP = input(
                "\nQuel type de coup voulez vous effectuer ?\n'D' pour déplacer le jeton,\
                \n'MH' pour placer un mur horizontal,\n'MV' pour placer un mur vertical.\nType: ")
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
            PARTIE.grille = jouer_coup(ID_PARTIE, TYPE_COUP, POSITION)
        else:
            time.sleep(0.35)
            COUP = PARTIE.jouer_coup(1)
            PARTIE.grille = jouer_coup(ID_PARTIE, COUP[0], COUP[1])
        WIN = PARTIE.partie_terminée()
