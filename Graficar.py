import pygame


class Graficar:

    def __init__(self):
        self.pared = pygame.image.load("Images/lad.png")
        self.ladrillo = pygame.image.load("Images/din.png")
        self.puerta = pygame.image.load("Images/pta.png")
        self.monstruo = pygame.image.load("Images/mon1.png")
        self.agente = pygame.image.load("Images/mun.png")
        self.bomba = pygame.image.load("Images/bom.png")

    def GraficarTablero(self, ventana, matriz):
        for n, i in enumerate(matriz):
            posy = n*28
            for k, j in enumerate(i):
                posx = k*40
                if j == 1:  # Pared
                    ventana.blit(self.pared, (posx, posy))
                if j == 2:  # Ladrillo
                    ventana.blit(self.ladrillo, (posx, posy))
                if j == 4:  # Puerta
                    ventana.blit(self.puerta, (posx, posy))
                if j == 5:  # Monstruo
                    ventana.blit(self.monstruo, (posx, posy))
                if j == 6:  # Agente
                    ventana.blit(self.agente, (posx, posy))
                if j == 7:  # Bomba
                    ventana.blit(self.bomba, (posx, posy))
