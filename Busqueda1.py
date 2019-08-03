# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:20:36 2019

@author: diego
"""

import Tablero
import random

import pygame
import sys
from pygame.locals import *  # Surge error, es normal
#from Tablero import Tablero
from Graficar import Graficar

##Clases ///////////////////////////////////////

class Mapa:
    def __init__(self, archivo="mapa3.txt"):
        self.mapa = leerMapa(archivo)
        
    def camino(self, nodo):
        if (nodo.tipo == "Camino"):
            posAgente = buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = buscarPos(6, self.mapa)
            if self.mapa[nodo.pos[0]][nodo.pos[1]] != 7:
                self.mapa[nodo.pos[0]][nodo.pos[1]] = 6
        
        if (nodo.tipo == "Bomba"):
            self.mapa[nodo.pos[0]][nodo.pos[1]] = 7
            for i in range(len(nodo.inmediatos)):
                if (self.mapa[nodo.inmediatos[i][0]][nodo.inmediatos[i][1]] == 2):
                    self.mapa[nodo.inmediatos[i][0]][nodo.inmediatos[i][1]] = 8

        if (nodo.tipo == "Estallar"):
            padre = nodo.padre
            estallar = []
            bom = None
            while (padre != None):
                if (padre.tipo == "Bomba"):
                    estallar = padre.inmediatos
                    bom = padre.pos
                    break
                else:
                    padre = padre.padre

            for i in range(len(estallar)):
                if (estallar[i] == globals()["metaOculta"]):
                    self.mapa[estallar[i][0]][estallar[i][1]] = 4
                else:
                    if(self.mapa[estallar[i][0]][estallar[i][1]] != 1):
                        self.mapa[estallar[i][0]][estallar[i][1]] = 0
            self.mapa[bom[0]][bom[1]] = 0
        
        posAgente = buscarPos(5, self.mapa)
        while(posAgente != 0):
            self.mapa[posAgente[0]][posAgente[1]] = 0
            posAgente = buscarPos(5, self.mapa)
        for i in range(len(nodo.posEnemigos)):
            self.mapa[nodo.posEnemigos[i][0]][nodo.posEnemigos[i][1]] = 5

        return self.mapa

		
class Nodo:
    def __init__(self, tipo=None, pos=[0, 0], padre=None, inmediatos=[], mapa = []):
        self.mapaFinal = []
        self.puerta = False
        self.bomba = False
        self.contBom = 0
        self.tipo = tipo
        self.pos = pos
        self.mapa = []
        self.padre = padre
        self.inmediatos = inmediatos
        self.muerte = False
        self.posFinal = []
        self.posEnemigos = []
 
        if self.padre == None:
            self.g = 0
            self.mapa = mapa
            self.posFinal = posEncontrada(self.mapa)
            self.posEnemigos = enlistarLadrillos(self.mapa, 5)
            self.posEnemigos[0].append("Derecha")
            self.posEnemigos[1].append("Izquierda")
            self.posEnemigos[2].append("Abajo")
            print(self.posFinal)
            
        else:
            self.g = self.padre.g + 1
            self.posFinal = self.padre.posFinal
            #self.actualizarMatriz()

        self.h = distancia(self.pos, self.posFinal)
        self.f = self.g + self.h
        print(self.tipo, self.pos , self.posFinal, globals()["metaOculta"], " , ", self.f)
        



    def actualizarMatriz(self):
        if (self.tipo == "Camino"):
            posAgente = buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = buscarPos(6, self.mapa)
            if self.mapa[self.pos[0]][self.pos[1]] != 7:
                self.mapa[self.pos[0]][self.pos[1]] = 6
        
        if (self.tipo == "Bomba"):
            posAgente = buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = buscarPos(6, self.mapa)
            self.mapa[self.pos[0]][self.pos[1]] = 7
            posiciones = []
            for i in range(len(self.inmediatos)):
                if (self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] == 2):
                    self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] = 8

                for j in range(len(globals()["listaLadrillos"])):
                    if(self.inmediatos[i] == globals()["listaLadrillos"][j]):
                        posiciones.append(j)

            tamaño = len(globals()["listaLadrillos"])
            for i in range(len(posiciones)):
                del(globals()["listaLadrillos"][posiciones[i]])
                print(len(globals()["listaLadrillos"]), tamaño)
                print("a")

            final = posEncontrada(self.mapa)
            if(final != 0):
                self.posFinal = final
        
        if (self.tipo == "Estallar"):
            padre = self.padre
            estallar = []
            bom = None
            while (padre != None):
                if (padre.tipo == "Bomba"):
                    estallar = padre.inmediatos
                    bom = padre.pos
                    break
                else:
                    padre = padre.padre

            posiciones = []        
            for i in range(len(estallar)):
                if(estallar[i] == self.pos):
                    self.muerte = True
                if (estallar[i] == globals()["metaOculta"]):
                    self.mapa[estallar[i][0]][estallar[i][1]] = 4
                    self.puerta = True
                    self.posFinal = posEncontrada(self.mapa)
                else:
                    if(self.mapa[estallar[i][0]][estallar[i][1]] != 1):
                        self.mapa[estallar[i][0]][estallar[i][1]] = 0
                
                for j in range(len(self.posEnemigos)):
                    if (estallar[i] == self.posEnemigos[j]):
                        posiciones.append(j)

            for i in range(len(posiciones)):
                del(self.posEnemigos[posiciones[i]])
                print("a")

            self.mapa[bom[0]][bom[1]] = 0
        
        posAgente = buscarPos(5, self.mapa)
        while(posAgente != 0):
            if posAgente == self.pos:
                self.muerte = True
            self.mapa[posAgente[0]][posAgente[1]] = 0
            posAgente = buscarPos(5, self.mapa)
        for i in range(len(self.posEnemigos)):
            self.mapa[self.posEnemigos[i][0]][self.posEnemigos[i][1]] = 5


    def mostrarValores(self):
        mensajePapa = None
        if self.padre != None:
            mensajePapa =  (self.padre.pos, self.padre.h , self.padre.g)
        print(self.bomba, self.contBom, self.tipo, self.pos, self.posFinal, mensajePapa, 
                self.inmediatos, self.h, self.g, self.f, self.muerte, self.puerta)
        #print(self.tipo,"\n", self.mapa)
        
class AAsterisco:
    def __init__(self, mapa):
        self.mapa = mapa
        self.contador = 0
        
        # Nodos de inicio y fin.
        pos_inicial = buscarPos(6, mapa)
        self.inicio = Nodo("Camino", pos_inicial, None, [],  mapa)
        #self.inicio.mostrarValores()
        #self.fin = Nodo("Camino",pos_final)
        #self.fin.mostrarValores()
 
        # Crea las listas abierta y cerrada.
        self.abierta = []
        self.cerrada = []
        self.temp = []
 
        # Añade el nodo inicial a la lista cerrada.
        self.cerrada.append(self.inicio)
        #print(self.inicio.mapa)
   
        # Añade vecinos a la lista abierta
        self.abierta += self.vecinos(self.inicio)
 
        # Buscar mientras meta no este en la lista cerrada.
        while self.meta():
            self.contador += 1
            if(self.abierta == []):
                self.abierta = llenarLista(self.temp, self.abierta)
            self.buscar()
            """if(self.contador <= 3):
                self.buscar()
            else:
                punto = self.abierta[0]
                for i in range(1, len(self.abierta)):
                    if (punto.f > self.abierta[i].f):
                           punto = self.abierta[i]
                self.abierta = vaciarLista(self.abierta)
                punto.posFinal = punto.pos
                self.abierta.append(punto)
                break"""
 
        self.caminata = self.camino()
 
    # Devuelve una lista con los nodos vecinos transitables.
    def vecinos(self, nodo):
        
        nodo.contBom -= 1
        mapa = self.nuevoMapa(nodo.mapa)
        listaEnemigos = self.nuevosEnemigos(nodo.posEnemigos, mapa)
        for i in range(len(listaEnemigos)):
            mapa[listaEnemigos[i][0]][listaEnemigos[i][1]] = 5
            print([listaEnemigos[i][0], listaEnemigos[i][1]], nodo.pos)
            if(listaEnemigos[i][0] == nodo.pos[0] and listaEnemigos[i][1] == nodo.pos[1]):
                nodo.muerte = True
                

        vecinos   = []
        nuevopadre = nodo


        abajo_pos     = [nuevopadre.pos[0]+1 , nuevopadre.pos[1]]
        arriba_pos    = [nuevopadre.pos[0]-1 , nuevopadre.pos[1]]
        izquierda_pos = [nuevopadre.pos[0] , nuevopadre.pos[1]-1]
        derecha_pos   = [nuevopadre.pos[0] , nuevopadre.pos[1]+1]
        nodoAspirante = []
        
        abajo = mapa[abajo_pos[0]][abajo_pos[1]]
        arriba = mapa[arriba_pos[0]][arriba_pos[1]]
        izquierda = mapa[izquierda_pos[0]][izquierda_pos[1]]
        derecha = mapa[derecha_pos[0]][derecha_pos[1]]
        

        #print(self.peligroMorir(nuevopadre))
        if(nuevopadre.muerte == False and self.peligroMorir(nuevopadre) and nodo.bomba == True):
            nodoAspirante = Nodo("Camino", [nuevopadre.pos[0], nuevopadre.pos[1]], nuevopadre, [] , nuevopadre.mapa)
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta 
            nodoAspirante.f += 10  
            nodoAspirante.mapa = mapa
            nodoAspirante.posEnemigos = listaEnemigos
            nodoAspirante.actualizarMatriz()
            vecinos.append(nodoAspirante)
        

        if ((nodo.contBom < 0) and (nodo.bomba == True)):
            nodoAspirante = Nodo("Estallar",nodo.pos,nodo,[],nodo.mapa)
            nodoAspirante.bomba = False
            nodoAspirante.contBom = 0
            nodoAspirante.mapa = nodo.mapa
            nodoAspirante.posEnemigos = nodo.posEnemigos
            nodoAspirante.actualizarMatriz()
            #nodoAspirante.posEncontrada()
            #nodoAspirante.mostrarValores()
            self.cerrada.append(nodoAspirante)
            nuevopadre = self.cerrada[-1]
            #self.abierta = vaciarLista(self.abierta)

            mapa = self.nuevoMapa(nuevopadre.mapa)
            listaEnemigos = self.nuevosEnemigos(nuevopadre.posEnemigos, mapa)
            for i in range(len(listaEnemigos)):
                mapa[listaEnemigos[i][0]][listaEnemigos[i][1]] = 5
                print([listaEnemigos[i][0], listaEnemigos[i][1]], nodo.pos)
                if(listaEnemigos[i][0] == nodo.pos[0] and listaEnemigos[i][1] == nodo.pos[1]):
                    nodo.muerte = True

            abajo_pos     = [nuevopadre.pos[0]+1 , nuevopadre.pos[1]]
            arriba_pos    = [nuevopadre.pos[0]-1 , nuevopadre.pos[1]]
            izquierda_pos = [nuevopadre.pos[0] , nuevopadre.pos[1]-1]
            derecha_pos   = [nuevopadre.pos[0] , nuevopadre.pos[1]+1]
            nodoAspirante = []

            abajo = mapa[abajo_pos[0]][abajo_pos[1]]
            arriba = mapa[arriba_pos[0]][arriba_pos[1]]
            izquierda = mapa[izquierda_pos[0]][izquierda_pos[1]]
            derecha = mapa[derecha_pos[0]][derecha_pos[1]]
        
        if ((arriba == 2 or abajo == 2 or izquierda == 2 or derecha == 2) or (arriba == 5 or abajo == 5 or izquierda == 5 or derecha == 5)) and (nodo.bomba == False) and (nodo.puerta == False):
            inmediatos = []
            inmediatos.append(nodo.pos)
            inmediatos.append(arriba_pos)
            inmediatos.append(abajo_pos)
            inmediatos.append(izquierda_pos)
            inmediatos.append(derecha_pos)
            activarBomba = Nodo("Bomba",[nodo.pos[0], nodo.pos[1]],nodo,inmediatos, nodo.mapa)
            activarBomba.bomba = True
            activarBomba.contBom = 2
            activarBomba.mapa = nodo.mapa
            activarBomba.posEnemigos = nodo.posEnemigos
            activarBomba.actualizarMatriz()
            #activarBomba.mostrarValores()
            #activarBomba.posEncontrada()
            #print(activarBomba.mapa)
            self.cerrada.append(activarBomba)
            nuevopadre = self.cerrada[-1]
            
            mapa = self.nuevoMapa(nuevopadre.mapa)
            listaEnemigos = self.nuevosEnemigos(nuevopadre.posEnemigos, mapa)
            for i in range(len(listaEnemigos)):
                mapa[listaEnemigos[i][0]][listaEnemigos[i][1]] = 5
                print([listaEnemigos[i][0], listaEnemigos[i][1]], nodo.pos)
                if(listaEnemigos[i][0] == nodo.pos[0] and listaEnemigos[i][1] == nodo.pos[1]):
                    nodo.muerte = True
            
            abajo = self.mapa[abajo_pos[0]][abajo_pos[1]]
            arriba = self.mapa[arriba_pos[0]][arriba_pos[1]]
            izquierda = self.mapa[izquierda_pos[0]][izquierda_pos[1]]
            derecha = self.mapa[derecha_pos[0]][derecha_pos[1]]
            #self.fin.pos = globals()["pos_f"]
            encerrado = False
            if(arriba != 5 and abajo != 5 and derecha != 5 and izquierda != 5):
                self.temp = llenarLista(self.abierta, self.temp)
                self.abierta = vaciarLista(self.abierta)

        
            abajo_pos     = [nuevopadre.pos[0]+1 , nuevopadre.pos[1]]
            arriba_pos    = [nuevopadre.pos[0]-1 , nuevopadre.pos[1]]
            izquierda_pos = [nuevopadre.pos[0] , nuevopadre.pos[1]-1]
            derecha_pos   = [nuevopadre.pos[0] , nuevopadre.pos[1]+1]
            nodoAspirante = []
            
            abajo = mapa[abajo_pos[0]][abajo_pos[1]]
            arriba = mapa[arriba_pos[0]][arriba_pos[1]]
            izquierda = mapa[izquierda_pos[0]][izquierda_pos[1]]
            derecha = mapa[derecha_pos[0]][derecha_pos[1]]

            
        ### Posiciones vacias
        if  (abajo == 0 or abajo == 4) and abajo != 5:
            if (nuevopadre.muerte == False):
                nodoAspirante = Nodo("Camino",[abajo_pos[0], abajo_pos[1]], nuevopadre, [], nuevopadre.mapa)
                nodoAspirante.bomba = nuevopadre.bomba
                nodoAspirante.contBom = nuevopadre.contBom
                nodoAspirante.puerta = nuevopadre.puerta
                nodoAspirante.mapa = mapa
                nodoAspirante.posEnemigos = listaEnemigos
                nodoAspirante.actualizarMatriz()
                #nodoAspirante.mostrarValores()
                vecinos.append(nodoAspirante)   
                
        if  (arriba == 0 or arriba == 4) and arriba != 5 :
            if (nuevopadre.muerte == False) :
                nodoAspirante = Nodo("Camino",[arriba_pos[0], arriba_pos[1]], nuevopadre, [], nuevopadre.mapa) 
                nodoAspirante.bomba = nuevopadre.bomba
                nodoAspirante.contBom = nuevopadre.contBom
                nodoAspirante.puerta = nuevopadre.puerta
                nodoAspirante.mapa = mapa
                nodoAspirante.posEnemigos = listaEnemigos
                nodoAspirante.actualizarMatriz()
                #nodoAspirante.mostrarValores()
                vecinos.append(nodoAspirante)  
                
        if (izquierda == 0 or izquierda == 4) and izquierda != 5 :
            if (nuevopadre.muerte == False) :
                nodoAspirante = Nodo("Camino",[izquierda_pos[0], izquierda_pos[1]], nuevopadre, [], nuevopadre.mapa)  
                nodoAspirante.bomba = nuevopadre.bomba
                nodoAspirante.contBom = nuevopadre.contBom
                nodoAspirante.puerta = nuevopadre.puerta
                nodoAspirante.mapa = mapa
                nodoAspirante.posEnemigos = listaEnemigos
                nodoAspirante.actualizarMatriz()
                #nodoAspirante.mostrarValores()
                vecinos.append(nodoAspirante) 
                
        if  (derecha == 0 or derecha == 4) and derecha != 5 :
            if (nuevopadre.muerte == False):
                nodoAspirante = Nodo("Camino",[derecha_pos[0], derecha_pos[1]], nuevopadre, [], nuevopadre.mapa)
                nodoAspirante.bomba = nuevopadre.bomba
                nodoAspirante.contBom = nuevopadre.contBom
                nodoAspirante.puerta = nuevopadre.puerta
                nodoAspirante.mapa = mapa
                nodoAspirante.posEnemigos = listaEnemigos
                nodoAspirante.actualizarMatriz()
                #nodoAspirante.mostrarValores()
                vecinos.append(nodoAspirante) 
        
        return vecinos
 
    def nuevosEnemigos(self, lista, mapa):
        for i in range(len(lista)):
            posicion = False
            listaFinal = []
            if(lista[i][2] == "Derecha"):
                if(mapa[lista[i][0]][lista[i][1]+1] == 0) or (mapa[lista[i][0]][lista[i][1]+1] == 4) or (mapa[lista[i][0]][lista[i][1]+1] == 6):
                    listaFinal.append([lista[i][0], lista[i][1]+1, "Derecha"])
                    posicion = True
                    continue
                else:
                    lista[i][2] = "Izquierda"

            if(lista[i][2] == "Izquierda"):
                if(mapa[lista[i][0]][lista[i][1]-1] == 0) or (mapa[lista[i][0]][lista[i][1]-1] == 4) or (mapa[lista[i][0]][lista[i][1]-1] == 6):
                    listaFinal.append([lista[i][0], lista[i][1]-1, "Izquierda"])
                    posicion = True
                    continue
                else:
                    lista[i][2] = "Arriba"
            
            if(lista[i][2] == "Arriba"):
                if(mapa[lista[i][0]-1][lista[i][1]] == 0) or (mapa[lista[i][0]-1][lista[i][1]] == 4) or (mapa[lista[i][0]-1][lista[i][1]] == 6):
                    listaFinal.append([lista[i][0]-1, lista[i][1], "Arriba"])
                    posicion = True
                    continue
                else:
                    lista[i][2] = "Abajo"

            if(lista[i][2] == "Abajo"):     
                if(mapa[lista[i][0]+1][lista[i][1]] == 0) or (mapa[lista[i][0]+1][lista[i][1]] == 4) or (mapa[lista[i][0]+1][lista[i][1]] == 6):
                    listaFinal.append([lista[i][0]+1, lista[i][1], "Abajo"])
                    posicion = True
                    continue
                else:
                    lista[i][2] = "Derecha"
        
            if (posicion == False):
                listaFinal.append(lista[i])
        
        return listaFinal

    def nuevoMapa(self, mapa):
        mapaFinal = []
        for i in range(len(mapa)):
            mapaFinal.append(mapa[i])

        posAgente = buscarPos(5, mapaFinal)
        while(posAgente != 0):
            mapaFinal[posAgente[0]][posAgente[1]] = 0
            posAgente = buscarPos(5, mapaFinal)
        
        return mapaFinal

    # Pasa el elemento de f menor de la lista abierta a la cerrada.    
    def f_menor(self):
        a = self.abierta[0]
        n = 0
        for i in range(1, len(self.abierta)):
            if self.abierta[i].f < a.f:
                a = self.abierta[i]
                n = i
        self.cerrada.append(self.abierta[n])
        del self.abierta[n]
        #while(len(self.abierta) > 0):
         #   self.abierta.pop()
        
        
   
 
    # Comprueba si un nodo está en una lista.
    def en_lista(self, nodo, lista):
        for i in range(len(lista)):
            if nodo.pos == lista[i].pos:
                return 1
        return 0
 
    # Gestiona los vecinos del nodo seleccionado.
    def ruta(self):
        for i in range(len(self.nodos)):
            #if self.en_lista(self.nodos[i], self.cerrada):
             #   continue
            if not self.en_lista(self.nodos[i], self.abierta):
                self.abierta.append(self.nodos[i])
                #print(self.abierta[-1].pos)
            else:
                if self.select.f < self.nodos[i].f:
                    for j in range(len(self.abierta)):
                        if self.nodos[i].pos == self.abierta[j].pos:
                            del self.abierta[j]
                            self.abierta.append(self.nodos[i])
                            break     
 
    # Analiza el último elemento de la lista cerrada.
    def buscar(self):
        self.f_menor()
        self.select = self.cerrada[-1]
        self.nodos = self.vecinos(self.select)  
        self.ruta()
 
    # Comprueba si el meta meta está en la lista abierta.
    def meta(self):
        for i in range(len(self.abierta)):
            if (self.abierta[i].pos == globals()["metaOculta"]) and (self.abierta[i].puerta == True):
                return 0
        return 1
    
    def peligroMorir(self, nodo):
        padre = nodo.padre
        pos = nodo.pos
        ladrillos = []
        while (padre != None):
            if (padre.tipo == "Bomba"):
                ladrillos = padre.inmediatos
                break
            else:
                padre = padre.padre
        
        for i in range(len(ladrillos)):
            if(ladrillos[i] == pos):
                return 0
                    
        return 1     
    # Retorna una lista con las posiciones del camino a seguir.
    def camino(self):
        for i in range(len(self.abierta)):
            if (self.abierta[i].pos == globals()["metaOculta"]):
                meta = self.abierta[i]
                print(meta.mapa)

        camino = []
        while meta.padre != None:
            camino.append(meta)
            #print(meta.mapa, "\n")
            #print(meta.tipo, meta.pos, "Puerta ->", meta.puerta, meta.posFinal)
            meta = meta.padre
            #print("c", len(camino))
        camino.append(meta)
        camino.reverse()
        return camino

    
    
    
##//////////////////////////////////////////////



#Funciones /////////////////////////////////////

def vaciarLista(lista):
    while(len(lista) > 0):
        lista.pop()
        
    return lista

def llenarLista(lista1, listaVacia):
    for i in range(len(lista1)):
        listaVacia.append(lista1[i])

    return listaVacia
  
def distancia(a, b):
   # print(a, "\n", b)
    dis = abs(a[0] - b[0]) + abs(a[1] - b[1]) #Valor absoluto.      
    return dis

def buscarPos(x, mapa):
    for f in range(len(mapa)):
        for c in range(len(mapa[0])):
            if mapa[f][c] == x:
                return [f, c]
    return 0
    
    
# Quita el ultimo caracter de una lista.
def quitarUltimo(lista):
    for i in range(len(lista)):
        lista[i] = lista[i][:-1]
    return lista
 
# Covierte una cadena en una lista.
def listarCadena(cadena, i):
    lista = []
    for j in range(len(cadena)):
        if cadena[j] == "0":
            lista.append(0)
        if cadena[j] == "1":
            lista.append(1)
        if cadena[j] == "2":
            lista.append(2)
        if cadena[j] == "3":
            lista.append(3)
        if cadena[j] == "4":
            lista.append(4)
        if cadena[j] == "5":
            lista.append(5)
        if cadena[j] == "6":
            lista.append(6)
        if cadena[j] == "7":
            lista.append(7)
        if cadena[j] == "8":
            lista.append(8)
            
    return lista

def enlistarLadrillos(mapa, num):
    lista = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == num:
                lista.append([i,j])
    #print(listaLadrillos)
    return lista

def posEncontrada(mapa):
    posFinal = buscarPos(4, mapa)
    if(posFinal == 0) and (len(globals()["listaLadrillos"]) != 0):
        posFinal = globals()["listaLadrillos"][0]
        del globals()["listaLadrillos"][0]
        #print(globals()["listaLadrillos"])
    return posFinal
 
# Lee un archivo de texto y lo convierte en una lista.
def leerMapa(archivo):
    mapa1 = open(archivo, "r")
    mapa1 = mapa1.readlines()
    mapa1 = quitarUltimo(mapa1)
    for i in range(len(mapa1)):
        mapa1[i] = listarCadena(mapa1[i], i)
    return mapa1

def generarMeta(lista):
    pos = random.randint(0 , len(lista))
    return lista[pos-1]

##////////////////////////////////////////////////////
    
   
def main():
    opcion = int(input("Ingrese"))
    if opcion == 1:
        tablerito = Tablero.Tablero()
        tablerito.GenLadrillos()
        globals()["metaOculta"] = tablerito.GenMeta()
        print(globals()["metaOculta"])
        mapaEnd = Mapa("aleatoria.txt")
        globals()["listaLadrillos"] = enlistarLadrillos(mapaEnd.mapa, 2)
        dibujarMapa = Mapa("aleatoria.txt")
        print("a")
    else:
        mapaEnd = Mapa()
        globals()["listaLadrillos"] = enlistarLadrillos(mapaEnd.mapa,2)
        globals()["metaOculta"] = generarMeta(globals()["listaLadrillos"])
        dibujarMapa = Mapa()
        print("a")

    """for i in range(len(mapaEnd.mapa)):
        for j in range(len(mapaEnd.mapa[0])):
            if(mapaEnd.mapa[i][j] == 2):
                globals()["metaOculta"] = [9,14]
    print(globals()["metaOculta"])"""
    ##print(mapaEnd)     
    A = AAsterisco(mapaEnd.mapa)
    print(mapaEnd.mapa)

    for i in range(len(A.caminata)):
        print(A.caminata[i].tipo, A.caminata[i].pos, "Puerta ->", A.caminata[i].puerta, A.caminata[i].posFinal, " , ", A.caminata[i].f, " , ",A.caminata[i].posEnemigos )
        #print(mapaEnd.camino(A.caminata[i]))

    """for i in range(len(A.caminata)):
        print(dibujarMapa.camino(A.caminata[i]), "\n", i)"""
    
    #matrices = Busqueda1.principal()#[matrizeje1, matrizeje2, matrizeje3, matrizeje4, matrizeje5]

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
        [len(mapaEnd.mapa[0])*40, len(mapaEnd.mapa)*28])
    pygame.display.set_caption("Bomberman game")

    # Variable auxiliar para controlar el tiempo de graficado del tablero:
    aux_tiempo = 3000
    c = True

    while c:


        Tiempo = pygame.time.get_ticks()
        # print(Tiempo)

        if aux_tiempo == Tiempo:
            ventana.fill(pygame.Color("#4ca404"))
            grafica.GraficarTablero(ventana, dibujarMapa.camino(A.caminata[aux]))
            #dibujarMapa.camino(A.caminata[aux])
            aux_tiempo += 1000
            aux += 1
            print(len(A.caminata), aux)
            if aux == len(A.caminata)+1:
                break

        #if Tiempo == 20000:
        #   c = False

        for evento in pygame.event.get():
            if evento.type == QUIT:  # Surge error, es normal
                pygame.quit()  # Surge error, es normal
                sys.exit()

        pygame.display.update()

            
            #print(i)  
            #listaDeMatrices.append(mapaEnd.camino(A.caminata[i]))
            #print(A.caminata[i].tipo, A.caminata[i].pos, "Puerta ->", A.caminata[i].puerta, A.caminata[i].posFinal)
            #print(A.camino[i])



main()
