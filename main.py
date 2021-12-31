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
        while not(self.isEmpty(pos,self.grille)): # securite
            pos = input("Erreur, recommencez: ")
        self.grille.tableau[int(pos)].valeur = self.list_Joueur[self.rang_joueur].symbole # Assigne le symbole du joueur a la case du tableau au rang pos
        self.grille.caseDispo.remove(int(pos)) # Retire donc la case de la liste des cases vides
        self.compteur += 1
        self.changePlayer()
    def jeuEntier(self, niveau_IA):
        if niveau_IA == 0:
            while not(self.grille.partieGagnee()) and (len(self.grille.caseDispo) != 0): # Boucle du jeu
                self.tourJeu()
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
                    print(self.grille.caseDispo)
                    print(len(self.grille.caseDispo)-1)
                    self.tourJeu(self.grille.caseDispo[random.randint(0, len(self.grille.caseDispo)-1)]) # prend un rang aleatoire correspondant a une case vide

            self.grille.__str__()

multijoueur = input("Souhaitez-vous une partie multijoueur ? (O/N) : ")
while not(multijoueur == "O" or multijoueur == "N"):
    multijoueur = input("Erreur, recomencez (O/N) : ")

if multijoueur == "O":
    player1_name = input("Entrez le pseudo du joueur 1 de symbole X : ")
    player2_name = input("Entrez le pseudo du joueur 2 de symbole O : ")
    niveau_IA = 0
else:
    niveau_IA = input("Choisissez le niveau de l'IA (1) : ")
    while not(niveau_IA == "1"): # Securite
        niveau_IA = input("Erreur, recommencez (1) : ")
    niveau_IA = int(niveau_IA) # Evite les erreurs entre str et int
    player1_name = input("Entrez votre pseudo : ")
    player2_name = "IA " + str(niveau_IA)



L = [Joueur(player1_name,"X"), Joueur(player2_name, "O")]
game = Jeu(L)
game.jeuEntier(niveau_IA)