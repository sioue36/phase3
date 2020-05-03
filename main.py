# -*- coding: utf-8 -*-
'''
Module permettant de jouer au jeu Quoridor contre un server.
'''

import argparse
from api import initialiser_partie, jouer_coup
import quoridor
import quoridorx
import time


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

import random
if __name__ == "__main__":
#initialise la grille de départ
    ARGS = analyser_commande()
    ID_PARTIE = initialiser_partie(ARGS.idul)[0]
    GRILLE = initialiser_partie(ARGS.idul)[1]
#GRAPHIQUE  
    if ARGS.graphique:
        partie = quoridorx.QuoridorX(GRILLE['joueurs'], GRILLE['murs'])
        partie.automatique = ARGS.automatique
        partie.id = ID_PARTIE
#NON-GRAPHIQUE
    else:
        partie = quoridor.Quoridor(GRILLE['joueurs'], GRILLE['murs'])

    WIN = False
    while not WIN:
        partie.afficher()

        #si le jeu est manuel
        if not ARGS.automatique:
            #type de coup
            TYPE_COUP = input(
                "\nQuel type de coup voulez vous effectuer ?\n'D' pour déplacer le jeton,\n'MH' pour placer un mur horizontal,\n'MV' pour placer un mur vertical.\nType: ")
            TYPE_COUP = TYPE_COUP.upper()
            if TYPE_COUP == '':
                TYPE_COUP = 'D'
            #la prochaine position
            ISINT = False
            while not ISINT:
                try:
                    POS_X = int(input("Coordonnée en 'x'? "))
                    POS_Y = int(input("Coordonnée en 'y'? "))
                    ISINT = True
                except ValueError:
                    print('La valeur entrée est invalide.')
            POSITION = (POS_X, POS_Y)
            #coup serveur
            partie.grille = jouer_coup(ID_PARTIE, TYPE_COUP, POSITION)

        #si le jeu est automatique
        else:
            time.sleep(0.35)
            COUP = partie.jouer_coup(1)
            partie.grille = jouer_coup(ID_PARTIE, COUP[0], COUP[1])

        WIN = partie.partie_terminée()