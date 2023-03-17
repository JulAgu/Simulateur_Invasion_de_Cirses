from Globals import *

class countersTerrain:
    '''Cette classe est chargée de compter le nombre de plantes vivantes et détectées dans chaque cycle de simulation quotidien.
    '''
    def __init__(self) -> None:
        self.cirsesvivantes = 0
        self.cirsesdetectes = 0
    
    def counter(self,terrain):
        for i in terrain.planterrain:
            if i.cirse:
                self.cirsesvivantes += 1
            if i.detection:
                self.cirsesdetectes += 1
    
    def counterReset(self):
        self.cirsesvivantes = 0
        self.cirsesdetectes = 0
    