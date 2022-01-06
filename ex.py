def recherche(caractere, mot):
    compteur = 0
    for i in mot:
        if caractere == i:
            compteur +=1
    return compteur
print(recherche("l", "literallement"))