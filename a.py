def convertir(T):
    taille = len(T)
    convertion = 0
    for i in range(taille):
        convertion = convertion + T[i]*(2**(taille-i-1))
    return convertion

def rendu(somme):
    n1 = 0
    n2 = 0
    n3 = 0
    while somme != 0:
        if somme >= 5:
            n1 += 1
            somme -= 5
        elif somme >= 2 and somme < 5:
            n2 += 1
            somme -= 2
        else:
            n3 += 1
            somme -= 1
    return n1, n2, n3

print(rendu(18))