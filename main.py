import pygame
import sys
from pygame.locals import *  # Surge error, es normal
from Tablero import Tablero
from Graficar import Graficar
#import Busqueda1

# Función sólamente de prueba, permite graficar 5 matrices y generar el vídeo envíado al grupo:

matrizeje1 = [[1, 1, 1, 1, 1, 1, 1], [1, 6, 0, 0, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje2 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 6, 0, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje3 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 6, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje4 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 6, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje5 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 6, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje6 = [[1, 1, 1, 1, 1, 1, 1], [1, 6, 0, 0, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje7 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 6, 0, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje8 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 6, 0, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje9 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 6, 0, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]
matrizeje10 = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 6, 1], [1, 0, 1, 2, 1, 0, 1], [
    1, 0, 2, 2, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 2, 0, 0, 2, 2, 1], [1, 1, 1, 1, 1, 1, 1]]


matrices = [matrizeje1, matrizeje2, matrizeje3, matrizeje4, matrizeje5,
            matrizeje6, matrizeje7, matrizeje8, matrizeje9, matrizeje10,
            matrizeje1, matrizeje2, matrizeje3, matrizeje4, matrizeje5,
            matrizeje6, matrizeje7, matrizeje8, matrizeje9, matrizeje10]

# variable para controlar el iterador de matrices:
aux = 0

# Objeto Tablero para generar el tablero de juego
#tablero = Tablero()
matriz_juego = matrices[0]#tablero.GenLadrillos()

# Objeto Graficar() para poder graficar el tablero de juego
grafica = Graficar()

# A partir de aquí se genera la ventana de Pygame hasta el final del ciclo while:

pygame.init()  # Surge error, es normal

# Se le da una dimensión a la ventana acorde al las dimensiones de la matriz_juego:
ventana = pygame.display.set_mode(
    [len(matriz_juego[0])*40, len(matriz_juego)*28])
pygame.display.set_caption("Bomberman game")

# Variable auxiliar para controlar el tiempo de graficado del tablero:
aux_tiempo = 5000
c = True

while c:

    Tiempo = pygame.time.get_ticks()
    # print(Tiempo)

    if aux_tiempo == Tiempo:
        ventana.fill(pygame.Color("#4ca404"))
        grafica.GraficarTablero(ventana, matrices[aux])
        aux_tiempo += 1000
        aux += 1
        if aux == len(matrices)+1:
            break

    #if Tiempo == 20000:
     #   c = False

    for evento in pygame.event.get():
        if evento.type == QUIT:  # Surge error, es normal
            pygame.quit()  # Surge error, es normal
            sys.exit()

    pygame.display.update()
