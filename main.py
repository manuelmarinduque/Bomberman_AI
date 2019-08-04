import Busqueda1
import pygame
import sys
from pygame.locals import *  # Surge error, es normal
from Tablero import Tablero
from Graficar import Graficar
#import Busqueda1

# Función sólamente de prueba, permite graficar 5 matrices y generar el vídeo envíado al grupo:

mapeo = Busqueda1.listaFinal()
dibujarTablero = Busqueda1.Mapa(mapeo[1])
matrices = dibujarTablero.mapa


# variable para controlar el iterador de matrices:
aux = 0

# Objeto Tablero para generar el tablero de juego
#tablero = Tablero()
#matriz_juego = matrices[0]#tablero.GenLadrillos()

# Objeto Graficar() para poder graficar el tablero de juego
grafica = Graficar()

# A partir de aquí se genera la ventana de Pygame hasta el final del ciclo while:

pygame.init()  # Surge error, es normal

# Se le da una dimensión a la ventana acorde al las dimensiones de la matriz_juego:
ventana = pygame.display.set_mode(
    [len(matrices[0])*40, len(matrices)*28])
pygame.display.set_caption("Bomberman game")

# Variable auxiliar para controlar el tiempo de graficado del tablero:
aux_tiempo = 500
c = True

while c:

    Tiempo = pygame.time.get_ticks()
    # print(Tiempo)

    if aux_tiempo == Tiempo:
        ventana.fill(pygame.Color("#4ca404"))
        grafica.GraficarTablero(ventana, dibujarTablero.camino(mapeo[0][aux]))
        aux_tiempo += 500
        aux += 1
        if aux == len(mapeo[0])+1:
            break

    #if Tiempo == 20000:
     #   c = False

    for evento in pygame.event.get():
        if evento.type == QUIT:  # Surge error, es normal
            pygame.quit()  # Surge error, es normal
            sys.exit()

    pygame.display.update()
