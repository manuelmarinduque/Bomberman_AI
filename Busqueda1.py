# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:20:36 2019

@author: diego
"""

import Tablero

##Clases ///////////////////////////////////////

class Mapa:
    def __init__(self, archivo="mapa3.txt"):
        self.mapa = leerMapa(archivo)
        

		
class Nodo:
    def __init__(self, tipo=None, pos=[0, 0], padre=None, inmediatos=[], mapa = []):
        self.mapaFinal = []
        self.puerta = False
        self.bomba = False
        self.contBom = 0
        self.tipo = tipo
        self.pos = pos
        self.mapa = mapa
        self.padre = padre
        self.inmediatos = inmediatos
        self.muerte = False
        self.posFinal = []
 
        if self.padre == None:
            self.g = 0
            self.mapa = mapa
            self.posFinal = posEncontrada(self.mapa)
            print(self.posFinal)
            
        else:
            self.g = self.padre.g + 1
            self.retornarMapa()
            self.posFinal = self.padre.posFinal
            self.actualizarMatriz()
            print(self.tipo, self.pos , self.posFinal, globals()["metaOculta"])


        self.h = distancia(self.pos, self.posFinal)
        self.f = self.g + self.h
        
    def actualizarMatriz(self):
        if (self.tipo == "Camino"):
            posAgente = buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = buscarPos(6, self.mapa)
            if self.mapa[self.pos[0]][self.pos[1]] != 7:
                self.mapa[self.pos[0]][self.pos[1]] = 6
        
        if (self.tipo == "Bomba"):
            self.mapa[self.pos[0]][self.pos[1]] = 7
            for i in range(len(self.inmediatos)):
                if (self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] == 2):
                    self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] = 8
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
            self.mapa[bom[0]][bom[1]] = 0
            


    def mostrarValores(self):
        mensajePapa = None
        if self.padre != None:
            mensajePapa =  (self.padre.pos, self.padre.h , self.padre.g)
        print(self.bomba, self.contBom, self.tipo, self.pos, self.posFinal, mensajePapa, 
                self.inmediatos, self.h, self.g, self.f, self.muerte, self.puerta)
        #print(self.tipo,"\n", self.mapa)
        
    def retornarMapa(self):
        for i in range(len(self.mapa)):
            self.mapaFinal.append(self.mapa[i])

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
 
        # Añade el nodo inicial a la lista cerrada.
        self.cerrada.append(self.inicio)
        #print(self.inicio.mapa)
   
        # Añade vecinos a la lista abierta
        self.abierta += self.vecinos(self.inicio)
 
        # Buscar mientras meta no este en la lista cerrada.
        while self.meta():
            self.contador += 1
            self.buscar()
            """if(self.contador <= 4000):
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
        vecinos   = []
        nuevopadre = nodo
        abajo_pos     = [nodo.pos[0]+1 , nodo.pos[1]]
        arriba_pos    = [nodo.pos[0]-1 , nodo.pos[1]]
        izquierda_pos = [nodo.pos[0] , nodo.pos[1]-1]
        derecha_pos   = [nodo.pos[0] , nodo.pos[1]+1]
        nodoAspirante = []
        
        abajo = self.mapa[abajo_pos[0]][abajo_pos[1]]
        arriba = self.mapa[arriba_pos[0]][arriba_pos[1]]
        izquierda = self.mapa[izquierda_pos[0]][izquierda_pos[1]]
        derecha = self.mapa[derecha_pos[0]][derecha_pos[1]]
        
        if ((nodo.contBom < 0) and (nodo.bomba == True)):
            nodoAspirante = Nodo("Estallar",nodo.pos,nodo,[],nodo.mapa)
            nodoAspirante.bomba = False
            nodoAspirante.contBom = 0
            #nodoAspirante.posEncontrada()
            #nodoAspirante.mostrarValores()
            self.cerrada.append(nodoAspirante)
            nuevopadre = self.cerrada[-1]
            #self.abierta = vaciarLista(self.abierta)
        
        if (arriba_pos == nodo.posFinal or abajo_pos == nodo.posFinal or izquierda_pos == nodo.posFinal or derecha_pos == nodo.posFinal) and (nodo.bomba == False) and (nodo.puerta == False):
            inmediatos = []
            inmediatos.append(arriba_pos)
            inmediatos.append(abajo_pos)
            inmediatos.append(izquierda_pos)
            inmediatos.append(derecha_pos)
            activarBomba = Nodo("Bomba",[nodo.pos[0], nodo.pos[1]],nodo,inmediatos, nodo.mapa)
            activarBomba.bomba = True
            activarBomba.contBom = 2
            #activarBomba.mostrarValores()
            #activarBomba.posEncontrada()
            #print(activarBomba.mapa)
            self.cerrada.append(activarBomba)
            nuevopadre = self.cerrada[-1]
            #self.fin.pos = globals()["pos_f"]
            self.abierta = vaciarLista(self.abierta)

            
        ### Posiciones vacias
        if  abajo == 0 or abajo == 4 or abajo == 5:
            nodoAspirante = Nodo("Camino",[abajo_pos[0], abajo_pos[1]], nuevopadre, [], nuevopadre.mapa)
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta
            #nodoAspirante.mostrarValores()
            if (nuevopadre.muerte == False) :
                vecinos.append(nodoAspirante)   
                
        if  arriba == 0 or arriba == 4 or arriba == 5:
            nodoAspirante = Nodo("Camino",[arriba_pos[0], arriba_pos[1]], nuevopadre, [], nuevopadre.mapa) 
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta
            #nodoAspirante.mostrarValores()
            if (nuevopadre.muerte == False) :
                vecinos.append(nodoAspirante)  
                
        if  izquierda == 0 or izquierda == 4 or izquierda == 5:
            nodoAspirante = Nodo("Camino",[izquierda_pos[0], izquierda_pos[1]], nuevopadre, [], nuevopadre.mapa)  
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta
            #nodoAspirante.mostrarValores()
            if (nuevopadre.muerte == False) :
                vecinos.append(nodoAspirante) 
                
        if  derecha == 0 or derecha == 4 or derecha == 5:
            nodoAspirante = Nodo("Camino",[derecha_pos[0], derecha_pos[1]], nuevopadre, [], nuevopadre.mapa)
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta
            #nodoAspirante.mostrarValores()
            if (nuevopadre.muerte == False) :
                vecinos.append(nodoAspirante)    
                        
        return vecinos
 
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
                if self.select.g+1 < self.nodos[i].g:
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
                return 1
                    
        return 0
     
    # Retorna una lista con las posiciones del camino a seguir.
    def camino(self):
        for i in range(len(self.abierta)):
            if (self.abierta[i].pos == globals()["metaOculta"]):
                meta = self.abierta[i]
                print(meta.mapa)

        camino = []
        while meta.padre != None:
            camino.append(meta.mapa)
            #print(meta.mapa, "\n")
            print(meta.tipo, meta.pos, "Puerta ->", meta.puerta, meta.posFinal)
            meta = meta.padre
            #print("c", len(camino))
        camino.reverse()
        return camino

    
    
    
##//////////////////////////////////////////////



#Funciones /////////////////////////////////////

def vaciarLista(lista):
    while(len(lista) > 0):
        lista.pop()
        
    return lista

  
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

def enlistarLadrillos(mapa):
    lista = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 2:
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

##////////////////////////////////////////////////////
    
   
def main():
    tablerito = Tablero.Tablero()
    tablerito.GenLadrillos()
    globals()["metaOculta"] = tablerito.GenMeta()
    print(globals()["metaOculta"])
    mapaEnd = Mapa("aleatoria.txt")
    globals()["listaLadrillos"] = enlistarLadrillos(mapaEnd.mapa)
    """for i in range(len(mapaEnd.mapa)):
        for j in range(len(mapaEnd.mapa[0])):
            if(mapaEnd.mapa[i][j] == 2):
                globals()["metaOculta"] = [9,14]
    print(globals()["metaOculta"])"""
    ##print(mapaEnd)     
    A = AAsterisco(mapaEnd.mapa)
    print(mapaEnd.mapa)
    for i in  range(len(A.caminata)):
        print(i)            
       #print(A.camino[i])
    return 0

if __name__ == '__main__':
	main()
