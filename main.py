#PROJET TIC TAC TOE

import random

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
    def update_pos_gagnante(self, pos_gagnantes):
        numbers_X = []
        for k in range(9):
            if self.grille.tableau[
                k].valeur == "X":  # Trouve l'emplacement des X pour mettre a jour pos_gagnantes sans les X
                numbers_X.append(k)
        for tab in pos_gagnantes:
            for bad_number in numbers_X:
                if bad_number in tab:
                    pos_gagnantes.remove(tab)
        return pos_gagnantes

    def ifWinwin(self, grille, pos_gagnantes):
        compteur = 0
        for comb in pos_gagnantes: # Pour toutes les combinaisons
            compteur = 0
            for co in comb: # On verifie si un ou plusieurs nombres
                for case_libre in grille.caseDispo:
                    if co == case_libre: # Correspondent avec les cases libre
                        pos = co
                        compteur += 1
            if compteur >= 2: # S'il y a plus d'un nombre, on ne peut pas gagner en un coup, on ne return donc aucune position
                pos = None
        return pos
    def strat_adv(self, grille, fake_pos_gagnantes):
        fake_grille = grille
        pos_gagnantes_inter = fake_pos_gagnantes
        for i in fake_pos_gagnantes:
            fake_grille = grille
            if i == grille.caseDispo[i]: # Si la case est libre
                fake_grille.changeValCase(fake_grille.caseDispo[i], "X") # On simule une grille pour regarder le tour suivant
                compteur = 0
                pos = self.ifWinwin(fake_grille, pos_gagnantes_inter)
                if pos != None:
                    compteur += 1 # On compte le nombre de fois que l'adversaire peut gagner
                    pos_gagnantes_inter.remove(pos)
                    pos = self.ifWinwin(fake_grille, pos_gagnantes_inter)
                    if pos != None:
                        compteur += 1
                if compteur == 2: # Si l'adversaire peut gagner deux fois au prochain tour
                    return i # On return la position de l'endroit ou il peut poser son symbole pour faire sa stratégie
        return None # Sinon on return rien, car pas de stratégie


    def update_fake_pos_gagnantes(self, fake_pos_gagnantes):
        numbers_O = []
        for k in range(9):
            if self.grille.tableau[k].valeur == "O":  # Trouve l'emplacement des O pour mettre a jour pos_gagnantes sans les O
                numbers_O.append(k)
        for tab in fake_pos_gagnantes:
            for bad_number in numbers_O:
                if bad_number in tab:
                    fake_pos_gagnantes.remove(tab)
        return fake_pos_gagnantes
    def IA2(self):
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
    def isEmpty(self, position, grille): # Renvoie Vrai si la case de position "position" est une case vide (regarde précisement si la position est presente le tableau grille.aCaseVide) renvoie False si non
        for valeurs in grille.caseDispo:
            if str(valeurs) == position:
                return True
        return False
    def tourJeu(self, setPos):
        self.grille.__str__()
        if setPos == None:
            pos = input(self.joueurPlaying().nom + ", Position: ")
        else:
            pos = setPos # Fonctionnement assure car setPos est issu d'un randint
            print("L'IA joue : " + str(pos))
        while not(self.isEmpty(pos,self.grille)): # securite
            pos = input("Erreur, recommencez: ")
        self.grille.tableau[int(pos)].valeur = self.list_Joueur[self.rang_joueur].symbole # Assigne le symbole du joueur a la case du tableau au rang pos
        self.grille.caseDispo.remove(int(pos)) # Retire donc la case de la liste des cases vides
        self.compteur += 1
        self.changePlayer()
    def jeuEntier(self, niveau_IA):
        if niveau_IA == 0:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                self.tourJeu(None)
            self.grille.__str__()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est terminée ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalité!")

        elif niveau_IA == 1:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)
                else:
                    self.tourJeu(str(self.grille.caseDispo[random.randint(0, len(self.grille.caseDispo)-1)])) # prend un rang aleatoire correspondant a une case vide
            self.grille.__str__()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est terminée ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalité!")

        elif niveau_IA == 2:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)

                else:
                    self.IA2()
            self.grille.__str__()
            if self.grille.partieGagnee():
                self.changePlayer()
                print("La partie est terminée ! Le vainqueur est", self.joueurPlaying().nom)
            else:
                print("Egalité!")

        elif niveau_IA == 3:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                if self.joueurPlaying() == self.list_Joueur[0]: # Si le joueur actuel est le player
                    self.tourJeu(None)
                else:
                    self.pos_gagnantes = self.update_pos_gagnante(self.pos_gagnantes)  # met donc a jour pos_gagnantes
                    if self.ifWinwin(self.grille, self.pos_gagnantes) != None:
                        self.tourJeu(self.ifWinwin(self.grille, self.pos_gagnantes))
                    else:
                        fake_pos_gagantes = self.pos_gagnantes #fake_pos_gagantes est une variable identique a pos_gagnantes, mais pour les X
                        fake_pos_gagantes = self.update_fake_pos_gagnantes(fake_pos_gagantes)
                        if self.ifWinwin(self.grille, fake_pos_gagantes) != None:
                            self.tourJeu(self.ifWinwin(self.grille, fake_pos_gagantes)) # Place notre symbole a l'endroit ou gagnerait l'ennemi si nous ne pouvions pas jouer.
                        else:
                            fake_pos_gagantes = [0, 2, 4, 6, 8]
                            fake_pos_gagantes = self.update_fake_pos_gagnantes(fake_pos_gagantes)
                            # si il peut le poser a un de ces endroits, et que prochain tour, il peut gagner sous deux formes
                            if self.strat_adv(self.grille, fake_pos_gagantes) != None:
                                pos = self.strat_adv(self.grille, fake_pos_gagantes)
                                self.tourJeu(pos)
                            else:
                                self.IA2()

"""
Bon bon bon...
On veut faire une IA parfaite
J'ai essayé de laisser venir les idees mais je n'y suis pas parvenue
Il faut donc faire un schema, une fiche technique !
La voici :

Idee generale:
- Si c'est mon tour et que je peux gagner, je gagne.
- Si l'adversaire tente une combinaison en un coup, je la parre
- Si l'adversaire tente une strategie sur deux tours (piege), je menace de gagner, menant ainsi au nul
- Si l'adversaire ne tente rien, je fais une strategie

Eh bien alors, comment on fait ça ?
On va faire 4 fonctions (un pour chaque if) pour simplifier la lecture finale, ca simplifiera aussi la creation de l'algorithme.

Detaillons maintenant chaque point un par un:

Si c'est mon tour et que je peux gagner, je gagne:
- Je regarde si je peux gagner
- Si c'est le cas, je place le "O" au point qui manque
- Si c'est pas le cas, je passe a la suite

Si l'adversaire tente une combinaison en un coup, je la parre:
- Je regarde si, sans que je joue, l'adversaire peut gagner
- Si c'est bien le cas, je place mon point la ou il aurait gagné
- Sinon je passe a la suite

Si l'adversaire tente une strategie sur deux tours (piege), je menace de gagner, menant ainsi au nul ou la victoire [Meilleure strategie qu'on peut faire dans le jeu]:
- Je regarde si, sans que je joue, l'adversaire peut jouer un coup qui, au prochain tour encore, lui offrira une victoire quoi qu'il arrive (une double menace de victoire 
qui s'avère donc imparrable)
- Si c'est le cas, je regarde si je peux le menacer de faire une combinaison gagnante qu'il peut parrer (ou pas), mais que cette combinaison ne l'incite pas  a jouer ou il devrait jouer
    - Si c'est le cas, je le menace
    - Sinon, je pare a l avance l'une de ses deux futures combinaisons
- Si c'est pas, je continue

Si l'adversaire ne tente rien, je fais une strategie:
- Si rien de ce qui est avant n'arrive, alors je tente de faire une petite combinaison de trois, sans chercher a aller plus loin, car le second joueur ne dispose pas d'assez de tour
pour tenter une double strategie.
- Je place donc un "O" de facon a pouvoir former une combinaison gagnante tout comme l'IA de niveau 2, s'il me pare, j'en tente une autre (a condition toujours que ce qui précède 
n'est pas validé


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
    print("--> IA de niveau 1 : Pose son symbole de façon aléatoire.")
    print("--> IA de niveau 2 : Cherche à tout prix à faire une combinaison gagnante.")
    print("--> IA de niveau 3 : IA impossible à vaincre...")
    niveau_IA = input("Choisissez le niveau de l'IA (1 / 2) : ")
    while not(niveau_IA == "1" or niveau_IA == "2"): # Securite
        niveau_IA = input("Erreur, recommencez (1 / 2) : ")
    niveau_IA = int(niveau_IA) # Evite les erreurs entre str et int
    player1_name = input("Entrez votre pseudo : ")
    player2_name = "IA-" + str(niveau_IA)
    def jeuEntier(self):
        while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
            self.tourJeu()
        self.grille.__str__()
        if self.grille.partieGagnee():
            self.changePlayer()
            player = str(self.joueurPlaying().nom)
            print("La partie est terminée ! Le vainqueur est ", player, " !")
        else:
            print("Egalité!")


multijoueur = input("Souhaitez-vous une partie multijoueur ? (O/N) : ")
while not(multijoueur == "O" or multijoueur == "N"):
    multijoueur = input("Erreur, recomencez (O/N) : ")

if multijoueur == "O":
    player1_name = input("Entrez le pseudo du joueur 1 de symbole X : ")
    player2_name = input("Entrez le pseudo du joueur 2 de symbole O : ")
    niveau_IA = 0
else:
    print("--> IA de niveau 1 : Pose son symbole de façon aléatoire.")
    print("--> IA de niveau 2 : Cherche à tout prix à faire une combinaison gagnante.")
    print("--> IA de niveau 3 : IA impossible à vaincre...")
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
print("\n Merci d'avoir joué !")