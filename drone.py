from Globals import *
import tkinter as tk
import random

class drone:
    def __init__(self,terreno,vitesse,canvas,mode) -> None:
        self.posSurTerrain = random.randint(0,len(terreno.planterrain)-1)
        self.x = terreno.planterrain[self.posSurTerrain].x
        self.y = terreno.planterrain[self.posSurTerrain].y
        self.dir = random.randint(0,1)
        self.vitesseX = 1
        self.vitesseY = 1
        self.LVLvitesse = vitesse
        self.marqHorizontal = False
        self.marqVertical = False

        self.counterelimination = 0
        self.counterdetection = 0

        self.l = terreno.l
        self.c = terreno.c
        
        self.mode = mode
        self.canvas = canvas

        if vitesse == 1:
            self.vitesseRelative = 10
        elif vitesse == 2:
            self.vitesseRelative = 20
        elif vitesse == 3:
            self.vitesseRelative = 30
        
        if self.mode:
            self.droncarre = self.canvas.create_rectangle(self.x, self.y, self.x + UNITE_MESURE, self.y + UNITE_MESURE, width = 0, fill = "red" )
    
    def coord_to_index(self):
        self.index = int((self.y*self.c+self.x)/UNITE_MESURE)


    def deplacementHorizontal(self,terreno,saisonBool):
        
        if ((-1*UNITE_MESURE >= (self.y + self.vitesseY*UNITE_MESURE) or (self.y + self.vitesseY*UNITE_MESURE) >= self.l*UNITE_MESURE) and
        ((self.x + self.vitesseX*UNITE_MESURE) >= self.c*UNITE_MESURE or (self.x + self.vitesseX*UNITE_MESURE) <= -1*UNITE_MESURE )):
            self.vitesseY *= -1
        
        if -1 < self.x + self.vitesseX*UNITE_MESURE < self.c*UNITE_MESURE:
            self.x += self.vitesseX*UNITE_MESURE

        elif (self.x + self.vitesseX*UNITE_MESURE) >= self.c*UNITE_MESURE and not self.marqHorizontal:
            self.y += self.vitesseY*UNITE_MESURE
            self.vitesseX *= -1
            self.marqHorizontal = True

        elif (self.x + self.vitesseX*UNITE_MESURE) <= -1*UNITE_MESURE and self.marqHorizontal:
            self.y += self.vitesseY*UNITE_MESURE
            self.vitesseX *= -1
            self.marqHorizontal = False

        self.coord_to_index()
        if terreno.planterrain[self.index].cirse and saisonBool:
            terreno.planterrain[self.index].detecterCirse(self.LVLvitesse, self)
            if terreno.planterrain[self.index].detection and self.mode:
                self.canvas.itemconfigure(terreno.rectangles[self.index], fill="blue")
        
        terreno.planterrain[self.index].detruireCirse(self)
        if self.mode:
            if not terreno.planterrain[self.index].cirse:
                self.canvas.itemconfigure(terreno.rectangles[self.index], fill="black")
            self.canvas.coords(self.droncarre,self.x, self.y, self.x + UNITE_MESURE, self.y + UNITE_MESURE)
        

    def deplacementVertical(self,terreno,saisonBool):

        if ((-1*UNITE_MESURE >= (self.x + self.vitesseX*UNITE_MESURE) or (self.x + self.vitesseX*UNITE_MESURE) >= self.c*UNITE_MESURE) and
        ((self.y + self.vitesseY*UNITE_MESURE) >= self.l*UNITE_MESURE or (self.y + self.vitesseY*UNITE_MESURE) <= -1*UNITE_MESURE )):
            self.vitesseX *= -1

        if -1 < self.y + self.vitesseY*UNITE_MESURE < self.l*UNITE_MESURE:
            self.y += self.vitesseY*UNITE_MESURE

        elif (self.y + self.vitesseY*UNITE_MESURE) >= self.l*UNITE_MESURE and not self.marqVertical:
            self.x += self.vitesseX*UNITE_MESURE
            self.vitesseY *= -1
            self.marqVertical = True

        elif (self.y + self.vitesseY*UNITE_MESURE) <= -1*UNITE_MESURE and self.marqVertical:
            self.x += self.vitesseX*UNITE_MESURE
            self.vitesseY *= -1
            self.marqVertical = False
        
        self.coord_to_index()
        if terreno.planterrain[self.index].cirse and saisonBool:
            terreno.planterrain[self.index].detecterCirse(self.LVLvitesse, self)
            if terreno.planterrain[self.index].detection and self.mode:
                self.canvas.itemconfigure(terreno.rectangles[self.index], fill="blue")

        terreno.planterrain[self.index].detruireCirse(self)
        if self.mode:
            if not terreno.planterrain[self.index].cirse:
                self.canvas.itemconfigure(terreno.rectangles[self.index], fill="black")
            self.canvas.coords(self.droncarre,self.x, self.y, self.x + UNITE_MESURE, self.y + UNITE_MESURE)