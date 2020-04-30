import networkx as nx


class QuoridorError(Exception):
    ''' 
    Exception pour les erreurs de la classe Quoridor
    '''
    pass


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Attributes:
        état (dict): état du jeu tenu à jour.

    Examples:
        >>> q.Quoridor()
    """

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. 
                
                Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].

            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].

        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """
        if not hasattr(joueurs, '__iter__'):
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")
        if len(joueurs) != 2:
            raise QuoridorError(
                "L'itérable de joueurs en contient un nombre différent de deux.")
        self.grille = {
            "joueurs": [{"nom": None, "murs": None, "pos": None}, {"nom": None, "murs": None, "pos": None}],
            "murs": {"horizontaux": [], "verticaux": []}
        }
        for i in range(2):
            if isinstance(joueurs[i], str):
                self.grille['joueurs'][i]['nom'] = joueurs[i]
                self.grille['joueurs'][i]['murs'] = 10
                if i == 0:
                    self.grille['joueurs'][i]['pos'] = (5, 1)
                else:
                    self.grille['joueurs'][i]['pos'] = (5, 9)
            else:
                self.grille['joueurs'][i]['nom'] = joueurs[i]['nom']
                self.grille['joueurs'][i]['murs'] = joueurs[i]['murs']
                if joueurs[i]['murs'] > 10 or joueurs[i]['murs'] < 0:
                    raise QuoridorError(
                        "Le nombre de murs qu'un joueur peut placer est plus grand que 10, ou négatif.")
                self.grille['joueurs'][i]['pos'] = tuple(joueurs[i]['pos'])
                if joueurs[i]['pos'][0] < 1 or joueurs[i]['pos'][0] > 9 or joueurs[i]['pos'][1] < 1 or joueurs[i]['pos'][1] > 9:
                    raise QuoridorError(
                        "La position d'un joueur est invalide.")
        if murs != None:
            if type(murs) is not dict:
                raise QuoridorError(
                    "L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
            self.grille['murs']['horizontaux'] = murs['horizontaux']
            self.grille['murs']['verticaux'] = murs['verticaux']
            raising = False
            murpareil = []
            for i in range(len(self.grille['murs']['horizontaux'])):
                self.grille['murs']['horizontaux'][i] = tuple(
                    self.grille['murs']['horizontaux'][i])
                if self.grille['murs']['horizontaux'][i] in murpareil:
                    raising = True
                murpareil.append(self.grille['murs']['horizontaux'][i])
                if self.grille['murs']['horizontaux'][i][0] == 9 or self.grille['murs']['horizontaux'][i][1] == 1:
                    raising = True
                if (self.grille['murs']['horizontaux'][i][0] + 1, self.grille['murs']['horizontaux'][i][1] - 1) in self.grille['murs']['verticaux']:
                    raising = True
                if (self.grille['murs']['horizontaux'][i][0] - 1, self.grille['murs']['horizontaux'][i][1]) in self.grille['murs']['horizontaux'] or (self.grille['murs']['horizontaux'][i][0] + 1, self.grille['murs']['horizontaux'][i][1]) in self.grille['murs']['horizontaux']:
                    raising = True
            murpareil = []
            for i in range(len(self.grille['murs']['verticaux'])):
                self.grille['murs']['verticaux'][i] = tuple(
                    self.grille['murs']['verticaux'][i])
                if self.grille['murs']['verticaux'][i] in murpareil:
                    raising = True
                murpareil.append(self.grille['murs']['verticaux'][i])
                if self.grille['murs']['verticaux'][i][0] == 1 or self.grille['murs']['verticaux'][i][1] == 9:
                    raising = True
                if (self.grille['murs']['verticaux'][i][0] - 1, self.grille['murs']['verticaux'][i][1] + 1) in self.grille['murs']['horizontaux']:
                    raising = True
                if (self.grille['murs']['verticaux'][i][0], self.grille['murs']['verticaux'][i][1] - 1) in self.grille['murs']['verticaux'] or (self.grille['murs']['verticaux'][i][0], self.grille['murs']['verticaux'][i][1] + 1) in self.grille['murs']['verticaux']:
                    raising = True
            if raising:
                raise QuoridorError("La position d'un mur est invalide.")
            graphe = construire_graphe([self.grille['joueurs'][0]['pos'], self.grille['joueurs']
                                        [1]['pos']], self.grille['murs']['horizontaux'], self.grille['murs']['verticaux'])
            if not nx.has_path(graphe, self.grille['joueurs'][0]['pos'], 'B1'):
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.grille['joueurs'][1]['pos'], 'B2'):
                raise QuoridorError("La position d'un mur est invalide.")
        if self.grille['joueurs'][0]['murs'] + self.grille['joueurs'][1]['murs'] + len(self.grille['murs']['horizontaux']) + len(self.grille['murs']['verticaux']) != 20:
            raise QuoridorError(
                "Le total des murs placés et plaçables n'est pas égal à 20.")

    def afficher(self):
        '''
        Présente le tableau de jeu.
        '''
        def placemurver(chaine, xy):
            '''
            Ajoute un mur vertical à la position xy dans la grille.
            '''
            z = (xy[0] - 1)*4 + (10 - xy[1])*80 - 39
            chaine = chaine[:z - 80] + '|' + chaine[z - 79: z - 40] + \
                '|' + chaine[z - 39: z] + '|' + chaine[z + 1:]
            return chaine

        def placemurhor(chaine, xy):
            '''
            Ajoute un mur horizontal à la position xy dans la grille.
            '''
            z = (xy[0])*4 + (10 - xy[1])*80
            chaine = chaine[:z - 2] + '-------' + chaine[z + 5:]
            return chaine

        def placepion(chaine, nb, x, y):
            '''
            Ajoute un pion 'nb' à la position (x, y) dans la grille.
            '''
            z = (x - 1)*4 + (10 - y)*80 - 37
            chaine = chaine[:z] + str(nb) + chaine[z + 1:]
            return chaine

        chaine = '   -----------------------------------'
        chaine += '\n' + '9' + ' | .   .   .   .   .   .   .   .   . |'
        for i in range(8, 0, -1):
            chaine += '\n' + '  |                                   |'
            chaine += '\n' + str(i) + ' | .   .   .   .   .   .   .   .   . |'
        chaine += '\n' + '--|-----------------------------------' + \
            '\n' + '  | 1   2   3   4   5   6   7   8   9'
        joueur_x = self.grille['joueurs'][0]['pos'][0]
        joueur_y = self.grille['joueurs'][0]['pos'][1]
        cpu_x = self.grille['joueurs'][1]['pos'][0]
        cpu_y = self.grille['joueurs'][1]['pos'][1]
        chaine = placepion(chaine, 1, joueur_x, joueur_y)
        chaine = placepion(chaine, 2, cpu_x, cpu_y)
        for i in self.grille['murs']['horizontaux']:
            chaine = placemurhor(chaine, i)
        for i in self.grille['murs']['verticaux']:
            chaine = placemurver(chaine, i)
        print('Légende: 1=' + self.grille['joueurs'][0]['nom'] + ', 2=' + self.grille['joueurs'][1]['nom'] + '\n' + chaine)

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent."""
        return self.afficher_damier_ascii(self.grille)

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): Le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        if joueur != 1 and joueur != 2:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        if position[0] < 1 or position[0] > 9 or position[1] < 1 or position[1] > 9:
            raise QuoridorError(
                'La position est invalide (en dehors du damier).')
        graphe = construire_graphe([self.grille['joueurs'][0]['pos'], self.grille['joueurs']
                                    [1]['pos']], self.grille['murs']['horizontaux'], self.grille['murs']['verticaux'])
        if position not in list(graphe.successors(self.grille['joueurs'][joueur - 1]['pos'])):
            raise QuoridorError(
                "La position est invalide pour l'état actuel du jeu.")
        self.grille['joueurs'][joueur - 1]['pos'] = position

    def état_partie(self):
        """Produire l'état actuel de la partie.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                Notez que les positions doivent être sous forme de tuple (x, y) uniquement.

        Examples:

            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ],
                'murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }

            où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
            au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
            associée à sa position sur le damier. Une position est représentée par un tuple
            de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

            Les murs actuellement placés sur le damier sont énumérés dans deux listes de
            positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
            est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
            situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
            mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        return self.grille

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.
            
        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        if self.partie_terminée():
            raise QuoridorError('La partie est déjà terminée.')
        if joueur != 1 and joueur != 2:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        graphe = construire_graphe([self.grille['joueurs'][0]['pos'], self.grille['joueurs']
                                    [1]['pos']], self.grille['murs']['horizontaux'], self.grille['murs']['verticaux'])
        if joueur == 1:
            next_pos = nx.shortest_path(
                graphe, tuple(self.grille['joueurs'][0]['pos']), 'B1')[1]
        else:
            next_pos = nx.shortest_path(
                graphe, tuple(self.grille['joueurs'][1]['pos']), 'B2')[1]
        self.grille['joueurs'][joueur - 1]['pos'] = next_pos
        return ('D', next_pos)

    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if list(self.grille['joueurs'][0]['pos'])[1] == 9:
            return True
        if list(self.grille['joueurs'][1]['pos'])[1] == 1:
            return True
        return False

    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        if orientation == 'vertical':
            orientation = 'verticaux'
            if position[0] == 1 or position[1] == 9:
                raise QuoridorError(
                    'La position est invalide pour cette orientation.')
        if orientation == 'horizontal':
            orientation = 'horizontaux'
            if position[0] == 9 or position[1] == 1:
                raise QuoridorError(
                    'La position est invalide pour cette orientation.')
        if joueur != 1 and joueur != 2:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        if self.grille['joueurs'][joueur - 1]['murs'] == 0:
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")
        self.grille['joueurs'][joueur - 1]['murs'] -= 1
        self.grille['murs'][orientation].append(position)
        test_for_QuoridorError = Quoridor(
            self.grille["joueurs"], self.grille["murs"])


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.

    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.

    Args:
        joueurs (List[Tuple]): une liste des positions (x,y) des joueurs.
        murs_horizontaux (List[Tuple]): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (List[Tuple]): une liste des positions (x,y) des murs verticaux.

    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
