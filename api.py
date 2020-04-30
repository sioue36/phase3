# -*- coding: utf-8 -*-
'''
Les fonctions pour communiquer avec le serveur.
'''

import requests


URL = "https://python.gel.ulaval.ca/quoridor/api"


def lister_parties(idul):
    '''
    Retourne la liste des 20 dernières parties de l'idul passé en argument.
    '''
    rep = requests.get(URL + '/lister/', params={'idul': idul})
    if rep.status_code == 200:
        if 'message' in rep.json():
            raise RuntimeError(rep.json()['message'])
        return rep.json()['parties']
    print(f"Le GET sur {URL + '/lister/'} a produit le code d'erreur {rep.status_code}.")


def initialiser_partie(idul):
    '''
    Retourne un tuple (id de la partie, état de la partie).
    '''
    rep = requests.post(URL + '/initialiser/', data={'idul': idul})
    if rep.status_code == 200:
        if 'message' in rep.json():
            raise RuntimeError(rep.json()['message'])
        return (rep.json()['id'], rep.json()['état'])
    print(f"Le GET sur {URL + '/initialiser/'} a produit le code d'erreur {rep.status_code}.")


def jouer_coup(id_partie, type_coup, position):
    '''
    Prend en argument l'identifiant de la partie, le type de coup et la position puis 
    retourne l'état de la partie après que le serveur aie joué son coup.
    '''
    rep = requests.post(URL + '/jouer/', data={'id': id_partie, 'type': type_coup, 'pos': position})
    if rep.status_code == 200:
        if 'message' in rep.json():
            raise RuntimeError(rep.json()['message'])
        if 'gagnant' in rep.json():
            raise StopIteration(rep.json()['gagnant'])
        return rep.json()["état"]
    print(f"Le GET sur {URL + '/jouer/'} a produit le code d'erreur {rep.status_code}.")
