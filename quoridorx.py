import quoridor as quo
import pyglet_graphique as pyg

class QuoridorX (quo.Quoridor):
    
    def __init__(self, joueurs, murs=None, param_supplémentaire=None):
        super().__init__(joueurs, murs)
        self.affichage = param_supplémentaire
    
    def afficher(self):
        pyg.ouvrir_fenetre(self.grille)

lol = QuoridorX(['sim', {'nom':'jul', 'murs':5, 'pos':(5,9)}], murs={'horizontaux':[(3,3), (5,3), (5,4)], 'verticaux':[(4,3), (4,5)]})
lol.afficher()