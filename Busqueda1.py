# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:20:36 2019

@author: diego
"""

import Tablero
import Funciones


##Clases ///////////////////////////////////////

class Mapa:
    def __init__(self, archivo="mapa3.txt"):
        self.mapa = Funciones.leerMapa(archivo)
        
    def camino(self, nodo):
        if (nodo.tipo == "Camino"):
            posAgente = Funciones.buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = Funciones.buscarPos(6, self.mapa)
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
        
        posMonstro = Funciones.buscarPos(5, self.mapa)
        while(posMonstro != 0):
            self.mapa[posMonstro[0]][posMonstro[1]] = 0
            posMonstro = Funciones.buscarPos(5, self.mapa)
        for i in range(len(nodo.posEnemigos)):
            if(self.mapa[nodo.posEnemigos[i][0]][nodo.posEnemigos[i][1]] != 4):
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
            busqueda = Funciones.posEncontrada(self.mapa, globals()["listaLadrillos"])
            self.posFinal = busqueda[0]
            globals()["listaLadrillos"] = busqueda[1]
            self.posEnemigos = Funciones.enlistarLadrillos(self.mapa, 5)
            self.posEnemigos[0].append("Derecha")
            self.posEnemigos[1].append("Izquierda")
            self.posEnemigos[2].append("Abajo")
            print(self.posFinal)
            
        else:
            self.g = self.padre.g + 1
            self.posFinal = self.padre.posFinal
            #self.actualizarMatriz()

        self.h = Funciones.distancia(self.pos, self.posFinal)
        self.f = self.g + self.h
        print(self.tipo, self.pos , self.posFinal, globals()["metaOculta"], " , ", self.f)
        



    def actualizarMatriz(self):
        if (self.tipo == "Camino"):
            posAgente = Funciones.buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = Funciones.buscarPos(6, self.mapa)
            if self.mapa[self.pos[0]][self.pos[1]] != 7:
                self.mapa[self.pos[0]][self.pos[1]] = 6
        
        if (self.tipo == "Bomba"):
            posAgente = Funciones.buscarPos(6, self.mapa)
            while(posAgente != 0):
                self.mapa[posAgente[0]][posAgente[1]] = 0
                posAgente = Funciones.buscarPos(6, self.mapa)
            self.mapa[self.pos[0]][self.pos[1]] = 7
            posiciones = []
            for i in range(len(self.inmediatos)):
                if (self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] == 2):
                    self.mapa[self.inmediatos[i][0]][self.inmediatos[i][1]] = 8

                for j in range(len(globals()["listaLadrillos"])):
                    if(self.inmediatos[i] == globals()["listaLadrillos"][j]):
                        posiciones.append(j)
                
            posiciones.reverse()
            tamaño = len(globals()["listaLadrillos"])
            for i in range(len(posiciones)):
                del(globals()["listaLadrillos"][posiciones[i]])
                print(len(globals()["listaLadrillos"]), tamaño)
                print("a")

            
        
        if (self.tipo == "Estallar"):
            padre = self.padre
            estallar = []
            while (padre != None):
                if (padre.tipo == "Bomba"):
                    estallar = padre.inmediatos
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
                    busqueda = Funciones.posEncontrada(self.mapa, globals()["listaLadrillos"])
                    self.posFinal = busqueda[0]
                    globals()["listaLadrillos"] = busqueda[1]
                else:
                    if(self.mapa[estallar[i][0]][estallar[i][1]] != 1):
                        self.mapa[estallar[i][0]][estallar[i][1]] = 0
                
                for j in range(len(self.posEnemigos)):
                    if (estallar[i][0] == self.posEnemigos[j][0]) and (estallar[i][1] == self.posEnemigos[j][1]):
                        posiciones.append(j)

            for i in range(len(posiciones)):
                del(self.posEnemigos[posiciones[i]])
                print("a")
        
        posAgente = Funciones.buscarPos(5, self.mapa)
        while(posAgente != 0):
            if posAgente == self.pos:
                self.muerte = True
            self.mapa[posAgente[0]][posAgente[1]] = 0
            posAgente = Funciones.buscarPos(5, self.mapa)
        for i in range(len(self.posEnemigos)):
            self.mapa[self.posEnemigos[i][0]][self.posEnemigos[i][1]] = 5


    def mostrarValores(self):
        mensajePapa = None
        if self.padre != None:
            mensajePapa =  (self.padre.pos, self.padre.h , self.padre.g)
        print(self.bomba, self.contBom, self.tipo, self.pos, self.posFinal, mensajePapa, 
                self.inmediatos, self.h, self.g, self.f, self.muerte, self.puerta)
        
class AAsterisco:
    def __init__(self, mapa):
        self.mapa = mapa
        self.contador = 0
        
        # Nodos de inicio
        pos_inicial = Funciones.buscarPos(6, mapa)
        self.inicio = Nodo("Camino", pos_inicial, None, [],  mapa)

 
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
                self.abierta = Funciones.llenarLista(self.temp, self.abierta)
            self.buscar()
            """if(self.contador <= 10000):
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
        
        if(nuevopadre.muerte == False and self.peligroMorir(nuevopadre) and nodo.bomba == True):
            nodoAspirante = Nodo("Camino", [nuevopadre.pos[0], nuevopadre.pos[1]], nuevopadre, [] , nuevopadre.mapa)
            nodoAspirante.bomba = nuevopadre.bomba
            nodoAspirante.contBom = nuevopadre.contBom
            nodoAspirante.puerta = nuevopadre.puerta 
            nodoAspirante.f += 10  
            nodoAspirante.mapa = mapa
            nodoAspirante.posEnemigos = listaEnemigos
            nodoAspirante.actualizarMatriz()
            nodoAspirante.posEnemigos = self.enemigos(nodoAspirante.mapa, listaEnemigos)
            vecinos.append(nodoAspirante)
        

        if ((nodo.contBom < 0) and (nodo.bomba == True)):
            nodoAspirante = Nodo("Estallar",nodo.pos,nodo,[],nodo.mapa)
            nodoAspirante.bomba = False
            nodoAspirante.contBom = 0
            nodoAspirante.mapa = nodo.mapa
            nodoAspirante.posEnemigos = nodo.posEnemigos
            nodoAspirante.actualizarMatriz()
            self.cerrada.append(nodoAspirante)
            nuevopadre = self.cerrada[-1]

            mapa = self.nuevoMapa(nuevopadre.mapa)
            for i in range(len(listaEnemigos)):
                mapa[listaEnemigos[i][0]][listaEnemigos[i][1]] = 5
                print([listaEnemigos[i][0], listaEnemigos[i][1]], nuevopadre.pos)
                if(listaEnemigos[i][0] == nuevopadre.pos[0] and listaEnemigos[i][1] == nuevopadre.pos[1]):
                    nuevopadre.muerte = True

            abajo_pos     = [nuevopadre.pos[0]+1 , nuevopadre.pos[1]]
            arriba_pos    = [nuevopadre.pos[0]-1 , nuevopadre.pos[1]]
            izquierda_pos = [nuevopadre.pos[0] , nuevopadre.pos[1]-1]
            derecha_pos   = [nuevopadre.pos[0] , nuevopadre.pos[1]+1]
            nodoAspirante = []

            abajo = mapa[abajo_pos[0]][abajo_pos[1]]
            arriba = mapa[arriba_pos[0]][arriba_pos[1]]
            izquierda = mapa[izquierda_pos[0]][izquierda_pos[1]]
            derecha = mapa[derecha_pos[0]][derecha_pos[1]]
        
        if ((arriba == 2 or abajo == 2 or izquierda == 2 or derecha == 2) or (arriba == 5 or abajo == 5 or izquierda == 5 or derecha == 5)) and (nuevopadre.bomba == False) and (nuevopadre.puerta == False):
            inmediatos = []
            inmediatos.append(nuevopadre.pos)
            inmediatos.append(arriba_pos)
            inmediatos.append(abajo_pos)
            inmediatos.append(izquierda_pos)
            inmediatos.append(derecha_pos)
            activarBomba = Nodo("Bomba",[nuevopadre.pos[0], nuevopadre.pos[1]],nuevopadre,inmediatos, nuevopadre.mapa)
            activarBomba.bomba = True
            activarBomba.contBom = 2
            activarBomba.mapa = nuevopadre.mapa
            activarBomba.posEnemigos = nuevopadre.posEnemigos
            activarBomba.actualizarMatriz()
            if(arriba_pos == nuevopadre.posFinal or abajo_pos == nuevopadre.posFinal or izquierda_pos == nuevopadre.posFinal or derecha_pos == nuevopadre.posFinal):
                final = Funciones.posEncontrada(self.mapa, globals()["listaLadrillos"])
                globals()["listaLadrillos"] = final[1]
                if(final[0] != 0):
                    self.posFinal = final

            self.cerrada.append(activarBomba)
            nuevopadre = self.cerrada[-1]
            
            mapa = self.nuevoMapa(nuevopadre.mapa)
            for i in range(len(listaEnemigos)):
                mapa[listaEnemigos[i][0]][listaEnemigos[i][1]] = 5
                print([listaEnemigos[i][0], listaEnemigos[i][1]], nuevopadre.pos)
                if(listaEnemigos[i][0] == nuevopadre.pos[0] and listaEnemigos[i][1] == nuevopadre.pos[1]):
                    nuevopadre.muerte = True
            
            abajo = self.mapa[abajo_pos[0]][abajo_pos[1]]
            arriba = self.mapa[arriba_pos[0]][arriba_pos[1]]
            izquierda = self.mapa[izquierda_pos[0]][izquierda_pos[1]]
            derecha = self.mapa[derecha_pos[0]][derecha_pos[1]]
            encerrado = False
            if(arriba != 5 and abajo != 5 and derecha != 5 and izquierda != 5):
                self.temp = Funciones.llenarLista(self.abierta, self.temp)
                self.abierta = Funciones.vaciarLista(self.abierta)

        
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
                nodoAspirante.posEnemigos = self.enemigos(nodoAspirante.mapa, listaEnemigos)
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
                nodoAspirante.posEnemigos = self.enemigos(nodoAspirante.mapa, listaEnemigos)
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
                nodoAspirante.posEnemigos = self.enemigos(nodoAspirante.mapa, listaEnemigos)
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
                nodoAspirante.posEnemigos = self.enemigos(nodoAspirante.mapa, listaEnemigos)
                vecinos.append(nodoAspirante) 
        
        return vecinos

    def enemigos(self, mapa, rutina):
        lista = Funciones.enlistarLadrillos(mapa, 5)
        for i in range(len(rutina)):
            lista[i].append(rutina[i][2])
        
        return lista
 
    def nuevosEnemigos(self, lista, mapa):
        listaFinal = []
        for i in range(len(lista)):
            posicion = False
            if(lista[i][2] == "Derecha"):
                if((mapa[lista[i][0]][lista[i][1]+1] == 0) or (mapa[lista[i][0]][lista[i][1]+1] == 4) or (mapa[lista[i][0]][lista[i][1]+1] == 6)):
                    if not (self.posicionOcupada(lista, listaFinal, [lista[i][0], lista[i][1]+1])):
                        listaFinal.append([lista[i][0], lista[i][1]+1, "Derecha"])
                        posicion = True
                        continue
                    else:
                        lista[i][2] = "Izquierda"
                else:
                    lista[i][2] = "Izquierda"

            if(lista[i][2] == "Izquierda"):
                if((mapa[lista[i][0]][lista[i][1]-1] == 0) or (mapa[lista[i][0]][lista[i][1]-1] == 4) or (mapa[lista[i][0]][lista[i][1]-1] == 6)):
                    if not (self.posicionOcupada(lista, listaFinal, [lista[i][0], lista[i][1]-1] )):
                        listaFinal.append([lista[i][0], lista[i][1]-1, "Izquierda"])
                        posicion = True
                        continue
                    else:
                        lista[i][2] = "Arriba"
                else:
                    lista[i][2] = "Arriba"
            
            if(lista[i][2] == "Arriba"):
                if((mapa[lista[i][0]-1][lista[i][1]] == 0) or (mapa[lista[i][0]-1][lista[i][1]] == 4) or (mapa[lista[i][0]-1][lista[i][1]] == 6)):
                    if not (self.posicionOcupada(lista, listaFinal, [lista[i][0]-1,lista[i][1]])):
                        listaFinal.append([lista[i][0]-1, lista[i][1], "Arriba"])
                        posicion = True
                        continue
                    else:
                        lista[i][2] = "Abajo"
                else:
                    lista[i][2] = "Abajo"

            if(lista[i][2] == "Abajo"):     
                if((mapa[lista[i][0]+1][lista[i][1]] == 0) or (mapa[lista[i][0]+1][lista[i][1]] == 4) or (mapa[lista[i][0]+1][lista[i][1]] == 6)):
                    if not (self.posicionOcupada(lista, listaFinal, [lista[i][0]+1, lista[i][1]])):
                        listaFinal.append([lista[i][0]+1, lista[i][1], "Abajo"])
                        posicion = True
                        continue
                    else:
                        lista[i][2] = "Derecha"
                else:
                    lista[i][2] = "Derecha"
        
            if (posicion == False):
                listaFinal.append(lista[i])
        
        return listaFinal

    def posicionOcupada(self, listapos, lista1, lista2):
        for i in range(len(lista1)):
            if((lista1[i][0] == lista2[0]) and (lista1[i][1] == lista2[1])):
                return True
                
        for i in range(len(listapos)):
            if((listapos[i][0] == lista2[0]) and (listapos[i][1] == lista2[1])):
                return True

        return False

    def nuevoMapa(self, mapa):
        mapaFinal = []
        for i in range(len(mapa)):
            mapaFinal.append(mapa[i])

        posAgente = Funciones.buscarPos(5, mapaFinal)
        while(posAgente != 0):
            mapaFinal[posAgente[0]][posAgente[1]] = 0
            posAgente = Funciones.buscarPos(5, mapaFinal)
        
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
        
    # Comprueba si un nodo está en una lista.
    def en_lista(self, nodo, lista):
        for i in range(len(lista)):
            if nodo.pos == lista[i].pos:
                return 1
        return 0
 
    # Gestiona los vecinos del nodo seleccionado.
    def ruta(self):
        for i in range(len(self.nodos)):
            if not self.en_lista(self.nodos[i], self.abierta):
                self.abierta.append(self.nodos[i])
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
            meta = meta.padre
        camino.append(meta)
        camino.reverse()
        return camino

    
   
def listaFinal():
    opcion = int(input("Ingrese"))
    if opcion == 1:
        archivo = "aleatoria.txt"
        tablerito = Tablero.Tablero()
        tablerito.GenLadrillos()
        globals()["metaOculta"] = tablerito.GenMeta()
    else:
        archivo = "mapa3.txt"

    mapaEnd = Mapa(archivo)
    globals()["listaLadrillos"] = Funciones.enlistarLadrillos(mapaEnd.mapa,2)
    globals()["metaOculta"] = Funciones.generarMeta(globals()["listaLadrillos"])
  
    A = AAsterisco(mapaEnd.mapa)
    print(mapaEnd.mapa)

    for i in range(len(A.caminata)):
        print(A.caminata[i].tipo, A.caminata[i].pos, A.caminata[i].muerte,  "Puerta ->", A.caminata[i].puerta, A.caminata[i].posFinal, " , ", A.caminata[i].f, " , ",A.caminata[i].posEnemigos )

    """for i in range(len(A.caminata)):
        print(dibujarMapa.camino(A.caminata[i]), "\n", i)"""
    
    return [A.caminata, archivo]