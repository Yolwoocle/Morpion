#PROJET TIC TAC TOE

import random
import copy

class Joueur:

    def __init__(self, nom, symbole): # Constructeur
        self.nom = nom
        self.symbole = symbole

    def __str__(self):
        texteJoueur = "Nom du joueur : " + str(self.nom) + "\n"
        texteJoueur += "Symbole : " + str(self.symbole) + "\n"
        return texteJoueur

class Case:

    def __init__(self, position, valeur): # Constructeur
        self.position = position
        self.valeur = valeur

    def __str__(self):
        return "|" + str(self.valeur)+ "|" # Return un affichage de la case



class Grille:
    def __init__(self): # Constructeur
        self.tableau = []
        [self.tableau.append(Case(i, None)) for i in range(9)] # Cree une liste de case vide
        self.caseDispo = []
        [self.caseDispo.append(i) for i in range(9)]
    def estVide(self, case):
        if case.valeur == None:
            return True
        return False
    def changeValCase(self, case, val):
        case.valeur = val

    def partieGagnee(self): # Chercher les combinaisons gagnantes
        for i in range(3): # Pour les lignes
            rang = i*3
            if ((self.tableau[rang].valeur == self.tableau[rang+1].valeur == self.tableau[rang+2].valeur) and (self.tableau[rang].valeur != None)):
                return True
        for i in range(3): # Pour les colonnes
            if ((self.tableau[i].valeur == self.tableau[i+3].valeur == self.tableau[i+6].valeur != None)):
                return True
        # Diagonales :
        if ((self.tableau[0].valeur == self.tableau[4].valeur == self.tableau[8].valeur) and (self.tableau[0].valeur != None)):
            return True
        if ((self.tableau[2].valeur == self.tableau[4].valeur == self.tableau[6].valeur) and (self.tableau[4].valeur != None)):
            return True
    def __str__(self):
        for j in range(3):
            for i in range(3):
                if self.tableau[j*3+i].valeur != None:
                    print("|" + str(self.tableau[j*3+i].valeur), end="")
                else:
                    print("| ", end="")
            print("|")

class Jeu:
    def __init__(self, list_Joueur): # Constructeur
        self.list_Joueur = list_Joueur
        self.grille = Grille()
        self.rang_joueur = 0
        self.compteur = 0
        self.pos_gagnantes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.fake_pos_gagantes =  [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]  # fake_pos_gagantes est une variable identique a pos_gagnantes, mais pour les X
    def update_pos_gagnantes(self, pos_gagnantes):
        numbers_X = []
        inter_tab = []
        for k in range(9):
            if self.grille.tableau[k].valeur == "X":  # Trouve l'emplacement des O pour mettre a jour fake pos_gagnantes sans les O
                numbers_X.append(k)
        if len(pos_gagnantes) > 0:
            for tab in pos_gagnantes:
                for i in tab:
                    for bad_number in numbers_X:
                        if bad_number == i:
                            inter_tab.append(tab)
        for i in inter_tab:
            if i in pos_gagnantes:
                pos_gagnantes.remove(i)
        return pos_gagnantes

    def ifWinwin(self, grille, pos_gagnantes):
        pos = None
        for comb in pos_gagnantes:  # Pour toutes les combinaisons
            compteur = 0
            for i in comb:
                for case_libre in grille.caseDispo:
                    if i == case_libre:  # Correspondent avec les cases libre
                        pos = i
                        compteur += 1
            if compteur > 1:  # S'il y a plus d'un nombre, on ne peut pas gagner en un coup, on ne return donc aucune position
                pos = None
            elif compteur == 1:
                return pos
        return pos

    def strat_adv(self, fake_pos_gagnantes):
        pos_gagnantes_inter = copy.deepcopy(fake_pos_gagnantes)
        for j in pos_gagnantes_inter:
            fake_Grille = copy.deepcopy(self.grille)
            for i in j:
                pos_gagnantes_inter = copy.deepcopy(fake_pos_gagnantes)
                if i in fake_Grille.caseDispo: # Si la case est libre
                    fake_Grille.tableau[i].valeur = "X" # On simule une grille pour regarder le tour suivant
                    fake_Grille.caseDispo.remove(i)
                    compteur = 0
                    pos_gagnantes_inter = self.update_fake_pos_gagnantes(fake_Grille, pos_gagnantes_inter)
                    fake_Grille.__str__()
                    pos = self.ifWinwin(fake_Grille, pos_gagnantes_inter)
                    if pos != None:
                        pos_gagnantes_inter.remove(j)
                        compteur += 1 # On compte le nombre de fois que l'adversaire peut gagner
                        pos = self.ifWinwin(fake_Grille, pos_gagnantes_inter)
                        if pos != None:
                            print("Strategie adverse detectee !")
                            return i # On return la position de l'endroit ou il peut poser son symbole pour faire sa strat??gie
        return None # Sinon on return rien, car pas de strat??gie


    def update_fake_pos_gagnantes(self, grille, fake_pos_gagnantes):
        numbers_O = []
        inter_tab = []
        for k in range(9):
            if grille.tableau[k].valeur == "O":  # Trouve l'emplacement des O pour mettre a jour fake pos_gagnantes sans les O
                numbers_O.append(k)
        if len(fake_pos_gagnantes) > 0: # [2, 3, 8]
            for tab in fake_pos_gagnantes:
                for i in tab:
                    for bad_number in numbers_O:
                        if bad_number == i:
                            inter_tab.append(tab)
        for i in inter_tab:
            fake_pos_gagnantes.remove(i)
        return fake_pos_gagnantes
    def IA2(self):
        if self.compteur == 1 and self.grille.tableau[4].valeur == None:
            self.tourJeu(str(4))
            return None
        have_played = False
        self.pos_gagnantes = self.update_pos_gagnantes(self.pos_gagnantes)  # met donc a jour pos_gagnantes
        for i in range(9):
            if self.grille.tableau[i].valeur == "O":  # Si on trouve un symbole O dans la grille
                for j in range(i + 1, 9):
                    if self.grille.tableau[j].valeur == "O":  # On regarde si d'autres symboles O sont dans la grille
                        for ltl_tab in self.pos_gagnantes:
                            if i in ltl_tab and j in ltl_tab:  # Si les deux symboles peuvent former une comb gagnante
                                for p in ltl_tab:
                                    if p != i and p != j:
                                        pos = p
                                        have_played = True

                if have_played != True:
                    for ltl_tab in self.pos_gagnantes:
                        if i in ltl_tab:
                            for p in ltl_tab:
                                if p != i:
                                    pos = p
                            have_played = True

        if have_played != True:
            pos = self.grille.caseDispo[random.randint(0, len(self.grille.caseDispo) - 1)]
        self.tourJeu(str(pos))

    def joueurPlaying(self):
        return self.list_Joueur[self.rang_joueur]
    def changePlayer(self):
        if self.rang_joueur == 0:
            self.rang_joueur = 1
        else:
            self.rang_joueur = 0
    def isEmpty(self, position, grille): # Renvoie Vrai si la case de position "position" est une case vide (regarde pr??cisement si la position est presente le tableau grille.aCaseVide) renvoie False si non
        for valeurs in grille.caseDispo:
            if str(valeurs) == position:
                return True
        return False
    def tourJeu(self, setPos):
        if setPos == None:
            pos = input(self.joueurPlaying().nom + ", Position: ")
        else:
            pos = setPos # Fonctionnement assure car setPos est issu d'un randint
            print("L'IA joue:", str(pos))
        while not(self.isEmpty(pos,self.grille)): # securite
            pos = input("Erreur, recommencez: ")
        self.grille.tableau[int(pos)].valeur = self.list_Joueur[self.rang_joueur].symbole # Assigne le symbole du joueur a la case du tableau au rang pos
        self.grille.caseDispo.remove(int(pos)) # Retire donc la case de la liste des cases vides
        self.compteur += 1
        self.changePlayer()
        self.grille.__str__()
    def jeuEntier(self, niveau_IA):
        if niveau_IA == 0:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                self.tourJeu(None)
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est termin??e ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalit??!")

        elif niveau_IA == 1:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)
                else:
                    self.IA2()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est termin??e ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalit??!")

        elif niveau_IA == 2:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)
                else:
                    self.pos_gagnantes = self.update_pos_gagnantes(self.pos_gagnantes)
                    if self.ifWinwin(self.grille, self.pos_gagnantes) != None:  # Gagne si c'est possible
                        self.tourJeu(str(self.ifWinwin(self.grille, self.pos_gagnantes)))
                    else:
                        self.fake_pos_gagantes = self.update_fake_pos_gagnantes(self.grille, self.fake_pos_gagantes)
                        if self.ifWinwin(self.grille, self.fake_pos_gagantes) != None:  # Empeche l'adversaire de gagner
                            self.tourJeu(str(self.ifWinwin(self.grille, self.fake_pos_gagantes)))
                        else:
                            self.IA2()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est termin??e ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalit??!")

        elif niveau_IA == 3:
            self.compteur = 0
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)
                else:
                    self.pos_gagnantes = self.update_pos_gagnantes(self.pos_gagnantes)
                    if self.ifWinwin(self.grille, self.pos_gagnantes) != None: # Gagne si c'est possible
                        print("J'ai gagne !")
                        self.tourJeu(str(self.ifWinwin(self.grille, self.pos_gagnantes)))
                    else:
                        self.fake_pos_gagantes = self.update_fake_pos_gagnantes(self.grille, self.fake_pos_gagantes)
                        if self.ifWinwin(self.grille, self.fake_pos_gagantes) != None: # Empeche l'adversaire de gagner
                            print("Je pare l'adversaire !")
                            self.tourJeu(str(self.ifWinwin(self.grille, self.fake_pos_gagantes)))
                        else:
                            fake_pos_gagantes = self.update_fake_pos_gagnantes(self.grille, self.fake_pos_gagantes)
                            # si il peut le poser a un de ces endroits, et que prochain tour, il peut gagner sous deux formes
                            if self.compteur >= 3 != None and self.strat_adv(fake_pos_gagantes):
                                pos = self.strat_adv(fake_pos_gagantes)
                                technic = [0, 2, 6, 8]
                                if pos in technic:
                                    self.pos_gagnantes = [[1, 4, 7], [3, 4, 5]]
                                    self.IA2()
                                    self.pos_gagnantes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],[2, 5, 8], [0, 4, 8], [2, 4, 6]]
                                    self.pos_gagnantes = self.update_pos_gagnantes(self.pos_gagnantes)
                                else:
                                    self.tourJeu(str(pos))
                            else:
                                print("Je lance une tentative de victoire !")
                                if self.compteur <= 2:
                                    technic = [0, 2, 6, 8]
                                    for i in technic:
                                        if i in self.grille.caseDispo:
                                            pos = i
                                    self.tourJeu(str(pos))
                                else:
                                    self.IA2()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est termin??e ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalit??!")
"""
Bon bon bon...
On veut faire une IA parfaite
J'ai essay?? de laisser venir les idees mais je n'y suis pas parvenue
Il faut donc faire un schema, une fiche technique !
La voici :

Idee generale:
- Si c'est mon tour et que je peux gagner, je gagne.
- Si l'adversaire tente une combinaison en un coup, je la parre
- Si l'adversaire tente une strategie sur deux tours (piege), je menace de gagner, menant ainsi au nul
- Si l'adversaire ne tente rien, je fais une strategie

Eh bien alors, comment on fait ??a ?
On va faire 4 fonctions (un pour chaque if) pour simplifier la lecture finale, ca simplifiera aussi la creation de l'algorithme.

Detaillons maintenant chaque point un par un:

Si c'est mon tour et que je peux gagner, je gagne:
- Je regarde si je peux gagner
- Si c'est le cas, je place le "O" au point qui manque
- Si c'est pas le cas, je passe a la suite

Si l'adversaire tente une combinaison en un coup, je la parre:
- Je regarde si, sans que je joue, l'adversaire peut gagner
- Si c'est bien le cas, je place mon point la ou il aurait gagn??
- Sinon je passe a la suite

Si l'adversaire tente une strategie sur deux tours (piege), je menace de gagner, menant ainsi au nul ou la victoire [Meilleure strategie qu'on peut faire dans le jeu]:
- Je regarde si, sans que je joue, l'adversaire peut jouer un coup qui, au prochain tour encore, lui offrira une victoire quoi qu'il arrive (une double menace de victoire 
qui s'av??re donc imparrable)
- Si c'est le cas, je regarde si je peux le menacer de faire une combinaison gagnante qu'il peut parrer (ou pas), mais que cette combinaison ne l'incite pas  a jouer ou il devrait jouer
    - Si c'est le cas, je le menace
    - Sinon, je pare a l avance l'une de ses deux futures combinaisons
- Si c'est pas, je continue

Si l'adversaire ne tente rien, je fais une strategie:
- Si rien de ce qui est avant n'arrive, alors je tente de faire une petite combinaison de trois, sans chercher a aller plus loin, car le second joueur ne dispose pas d'assez de tour
pour tenter une double strategie.
- Je place donc un "O" de facon a pouvoir former une combinaison gagnante tout comme l'IA de niveau 2, s'il me pare, j'en tente une autre (a condition toujours que ce qui pr??c??de 
n'est pas valid??


Au travail !
"""


multijoueur = input("Souhaitez-vous une partie multijoueur ? (O/N) : ")
while not(multijoueur == "O" or multijoueur == "N"):
    multijoueur = input("Erreur, recomencez (O/N) : ")

if multijoueur == "O":
    player1_name = input("Entrez le pseudo du joueur 1 de symbole X : ")
    player2_name = input("Entrez le pseudo du joueur 2 de symbole O : ")
    niveau_IA = 0
else:
    print("--> IA de niveau 1 : Pose son symbole de fa??on a gagner sans se soucier du jeu adverse.")
    print("--> IA de niveau 2 : Bloque l'adversaire et tente de gagner.")
    print("--> IA de niveau 3 : Anticipe la strategie adverse, la bloque, et si le gain est ?? port??e, gagne.")
    niveau_IA = input("Choisissez le niveau de l'IA (1 / 2 / 3) : ")
    while not(niveau_IA == "1" or niveau_IA == "2" or niveau_IA == "3"): # Securite
        niveau_IA = input("Erreur, recommencez (1 / 2 / 3) : ")
    niveau_IA = int(niveau_IA) # Evite les erreurs entre str et int
    player1_name = input("Entrez votre pseudo : ")
    player2_name = "IA-" + str(niveau_IA)

retry = "O"
L = [Joueur(player1_name,"X"), Joueur(player2_name, "O")]
while retry == "O":
    game = Jeu(L)
    game.jeuEntier(niveau_IA)
    retry = input("Voulez-vous recommencer ? (O/N) :")
    while not(retry != "O" or retry != "N"):
        retry = input("Erreur, recommencez (O/N) : ")
print("\n Merci d'avoir jou?? !")