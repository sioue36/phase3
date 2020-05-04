import quoridor as quo
import pyglet
import time
import api


class QuoridorX (quo.Quoridor):
    
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)
    
    def afficher(self):
        if self.automatique:
            self.window = pyglet.window.Window(width=500, height=500, caption='Quoridor automatique (Attendez que la partie se termine)')
            @self.window.event
            def on_draw():
                nom_des_joueurs = pyglet.text.Label('Blanc : {}       Noir : {}'.format(self.grille['joueurs'][0]['nom'], self.grille['joueurs'][1]['nom']),
                                    x=self.window.width/2, y=self.window.height-5,
                                    anchor_x='center', anchor_y='top')
                murs_a_placer = pyglet.text.Label('Murs : {}        Murs : {}'.format(self.grille['joueurs'][0]['murs'], self.grille['joueurs'][1]['murs']),
                                    x=self.window.width/2, y=self.window.height-25,
                                    anchor_x='center', anchor_y='top')
                self.window.clear()
                nom_des_joueurs.draw()
                murs_a_placer.draw()
                draw_quadrillé()
                placeJoueurs(self.grille)
                placeMursHorizontaux(self.grille)
                placeMursVerticaux(self.grille)
                COUP = self.jouer_coup(1)
                self.grille = api.jouer_coup(self.id, COUP[0], COUP[1])

            def allo(dt):
                draw_quadrillé()

            pyglet.clock.schedule_interval(allo , 1)
            pyglet.app.run()
        else:
            self.window = pyglet.window.Window(width=500, height=500, caption='Quoridor (Fermez la fenêtre pour entrer votre prochain coup)')
            @self.window.event
            def on_draw():
                nom_des_joueurs = pyglet.text.Label('Blanc : {}       Noir : {}'.format(self.grille['joueurs'][0]['nom'], self.grille['joueurs'][1]['nom']),
                                    x=self.window.width/2, y=self.window.height-5,
                                    anchor_x='center', anchor_y='top')
                murs_a_placer = pyglet.text.Label('Murs : {}        Murs : {}'.format(self.grille['joueurs'][0]['murs'], self.grille['joueurs'][1]['murs']),
                                    x=self.window.width/2, y=self.window.height-25,
                                    anchor_x='center', anchor_y='top')
                self.window.clear()
                nom_des_joueurs.draw()
                murs_a_placer.draw()
                draw_quadrillé()
                placeJoueurs(self.grille)
                placeMursHorizontaux(self.grille)
                placeMursVerticaux(self.grille)
            pyglet.app.run()


def draw_rectangle(largeur, hauteur, x, y):
            pyglet.graphics.draw(8, pyglet.gl.GL_LINES, ('v2i', (x, y, x, y+hauteur, x, y+hauteur, x+largeur, y+hauteur,  x+largeur, y+hauteur, x+largeur, y, x+largeur, y, x, y)))

def draw_quadrillé():
        draw_rectangle(396, 396, 50, 50)
        for i in range(4):
            draw_rectangle(44, 396, i*88+94, 50)
        for i in range(4):
            draw_rectangle(396, 44, 50, i*88+94)

def placeMursVerticaux(grille):
    for mur in grille['murs']['verticaux']:
        draw_rectangle(10, 88, 45+(mur[0]-1)*44 , 50+(mur[1]-1)*44)

def placeMursHorizontaux(grille):
    for mur in grille['murs']['horizontaux']:
        draw_rectangle(88, 10, 50+(mur[0]-1)*44 , 45+(mur[1]-1)*44)

def placeJoueurs(grille):
    #joueur 1
    x = 50 + 17 + (grille['joueurs'][0]['pos'][0]-1)*44   #en x
    y = 50 + 17 + (grille['joueurs'][0]['pos'][1]-1)*44 #en y
    draw_rectangle(10, 10, x, y)
    #joueur 2
    x = 50 + 17 + (grille['joueurs'][1]['pos'][0]-1)*44   #en x
    y = 50 + 17 + (grille['joueurs'][1]['pos'][1]-1)*44 #en y
    draw_rectangle(10, 10, x, y)
    draw_rectangle(8, 8, x+1, y+1)
    draw_rectangle(6, 6, x+2, y+2)
    draw_rectangle(4, 4, x+3, y+3)
    draw_rectangle(2, 2, x+4, y+4)
