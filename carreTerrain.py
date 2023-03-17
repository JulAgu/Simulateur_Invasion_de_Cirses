from Globals import *
import random


class carreTerrain():
    '''Definition d'une classe  représentant chaque unité de terrain. 
    Cette classe va faire la comptage des circes autour des rayons specifiés. jusqu'à une 
    unité pour la propagation vegetative et cinq carré de rayon pour la propagation aerienne.
    Les attributes de la classe gardent l'information potitionelle du chaque unité, ansi que
    '''
    def __init__(self,x,y,l,c,cirse = False, detection = False) -> None:

        '''
        Définitions des attributes de la classe. La liste "atour1", par example, gardera les indices des carrés qui sont à coté
        du objet carré et qui après seront ou pas eligible à recevoir une plante de cirse conçu pour la propagation vegetative.
        '''
        self.x = x
        self.y = y
        self.coordcarre = [x,y]
        self.cirse = cirse
        self.detection = detection
        referenceX = int(self.x/UNITE_MESURE)
        referenceY = int(self.y/UNITE_MESURE)
        self.atour1 = []
        self.atour1_cord = []
        self.atour5 = []
        self.atour5_cord = []

        #En calculant atour1:
        for i in range(referenceX - 1, referenceX + 2):
            for j in range(referenceY - 1, referenceY + 2):
                if (l > j >= 0 and c > i >= 0 
                        and not (i == referenceX and j == referenceY)):
                    self.atour1.append(j*c+i)
                    self.atour1_cord.append([i*UNITE_MESURE,j*UNITE_MESURE])

        #En calculant atour5:
        for i in range(referenceX - 5, referenceX + 6):
            for j in range(referenceY - 5, referenceY + 6):
                if (l > j >= 0 and c > i >= 0 
                        and not (i == referenceX and j == referenceY)):
                    self.atour5.append(j*c+i)
                    self.atour5_cord.append([i*UNITE_MESURE,j*UNITE_MESURE])
    
    def planterCirse(self):
        '''
        La fonction pour planter une cirse. Elle met la presence de cirse dans l'objet carré comme vrai
        et met en place des compteurs de temps pour 3 jours (reproduction vegetative), 5 jour (reproduction aerienne)
        et le nombre total de jours que la cirse est présent dans le carré en question. 
        '''
        self.cirse = True
        self.tc3 = 0
        self.tc5 = 0
        self.tcirse = 0
    
    def detecterCirse(self,vitesseDron,dron):
        '''
        Donne la probabilité de detecter la cirse, en accordance avec la vitesse du drone. Donne aussi un compteur 
        du nombre total de cirse detecté par les drones. Si le cirse est détectée, les attributs mappés sont modifiés. 
        '''
        prob = random.randint(0,100)
        if vitesseDron == 1:
            if prob <= 80:
                self.detection = True
                dron.counterdetection +=1
        
        if vitesseDron == 2:
            if prob <= 70:
                self.detection = True
                dron.counterdetection +=1
        
        if vitesseDron == 3:
            if prob <= 55:
                self.detection = True
                dron.counterdetection +=1
    
    def detruireCirse(self,dron):
        '''
        Calcule la probabilité de qu'une cirse soit éliminé par l'herbicide une fois qu'elle a été identifié par le drone. 
        Si le cirse est détruit, les attributs mappés sont modifiés.
        '''
        prob = random.randint(0,100)
        if self.detection == True and prob <= 65:
            self.cirse = False
            self.detection = False
            dron.counterelimination +=1