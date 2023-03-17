from Globals import *
import tkinter  as tk
import random
from carreTerrain import carreTerrain

class terreno:
    '''
    Le but ici c'est de créer une ensemble d'objet de la classe "carreTerrain", cet ensemble de carré donne 
    le terrain lui-même. "planterrain" c'est la liste qui contient les objets carrés.
    '''
    def __init__(self,canvas, l, c, mode, espace = UNITE_MESURE) -> None:
        self.l = l
        self.c = c
        self.espace = espace
        self.planterrain = []
        self.rectangles = []
        self.canvas = canvas

        self.mode = mode

        self.plantesAcc = 0

        for j in range(l):
            for i in range(c):
                self.planterrain.append(carreTerrain(i*espace, j*espace, self.l, self.c))
                if self.mode:
                    self.rectangles.append(self.canvas.create_rectangle(i*espace, j*espace, (i*espace)+espace, (j*espace)+espace, width = 0, fill = "black" ))

    def premierPlante(self):
        '''
        Plante la prémier plante dans le terrain de manière aléatoire.
        '''
        pos = random.randint(0,len(self.planterrain)-1)
        self.planterrain[pos].planterCirse()
        if self.planterrain[pos].cirse:
            self.plantesAcc += 1
        if self.mode:
            self.canvas.itemconfigure(self.rectangles[pos], fill="white")
    
    def cirsevegetative(self,saisonBool):
        '''
        Analyse si la cirse elle existe dans le carré en question. Si oui, donc on verifie le nombre de jours 
        qu'elle est déjà présent (pas le nombre total, juste les cycles de 3 jours). 
        Si le nombre est égal à 3, donc la cirse doit faire une propagation vegetative
        et retourner le temps à 0. Sinon, on ajoute 1 jour au cycle de 3 jours.

        Si la saison est hiver ou été la reproduction vegetative aura lieu chaque 40 jours !!!!
        '''
        if saisonBool:
            marqueurTemporal = 3
        else:
            marqueurTemporal = 40
            
        for carre in self.planterrain:
            if carre.cirse:
                if carre.tc3 == marqueurTemporal:
                    elegibles = [x for x in carre.atour1 if not self.planterrain[x].cirse]
                    if elegibles:
                        pos = random.randint(0, len(elegibles)-1)
                        self.planterrain[elegibles[pos]].planterCirse()
                        if self.planterrain[elegibles[pos]].cirse:
                            self.plantesAcc += 1
                        if self.mode:
                            self.canvas.itemconfigure(self.rectangles[elegibles[pos]], fill="green")
                    carre.tc3 = 0
                else:
                    carre.tc3 += 1
        

    
    def cirseaerienne(self):
        '''
        Pareil à la fonction derrière, mais pour la reproduction aerienne. (Chaque 5 jours)
        '''
        for carre in self.planterrain:
            if carre.cirse:
                if carre.tc5 == 5:
                    elegibles = [x for x in carre.atour5 if not self.planterrain[x].cirse]
                    if elegibles:
                        pos = random.randint(0, len(elegibles)-1)
                        self.planterrain[elegibles[pos]].planterCirse()
                        if self.planterrain[elegibles[pos]].cirse:
                            self.plantesAcc += 1
                        if self.mode:
                            self.canvas.itemconfigure(self.rectangles[elegibles[pos]], fill="green")
                    carre.tc5 = 0
                else:
                    carre.tc5 += 1
    
    def parcelleSaine(self):
        '''
        Compte le nombre de carrés infecté par les cirses. renvoie une valeur booléenne pour indiquer 
        si la simulation est arrêtée ou non. 
        UNE PARCELLE EST CONSIDÉRÉE ENVAHIE SI LES VÉGÉTAUX OCCUPENT PLUS DE 95% DE SA SUPERFICIE TOTALE.
        '''
        counter = 0
        for carre in self.planterrain:
            if carre.cirse:
                counter +=1
        if counter >= 0.95 * len(self.planterrain):
            return False
        else:
            return True

    def reproduction(self,saisonBool):
        '''exécute les fonctions de reproduction végétative et aérienne. 
        Pas de reproduction aérienne quand c'est l'hiver ou l'automne
        '''
        self.cirsevegetative(saisonBool)
        if saisonBool:
            self.cirseaerienne()