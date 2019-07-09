# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:20:36 2019

@author: diego
"""

##Clases ///////////////////////////////////////

class Mapa:
    def __init__(self, archivo="mapa1.txt"):
        self.contador = 0
        self.mapa = leerMapa(archivo)
        ##print(self.mapa)
        self.fila = len(self.mapa)
        self.columna = len(self.mapa[0])
        ##print(self.fila)
        ##print(self.columna)
        ##print(self.mapa)
        ##print(self.mapa[0][8])
 
    def __str__(self):
        salida = ""
        for f in range(self.fila):
            ##print(f)
            for c in range(self.columna):
                ##print(c)
                if self.mapa[f][c] == 0:
                    salida += "  "
                if self.mapa[f][c] == 1:
                    salida += "1 "
                if self.mapa[f][c] == 2:
                    salida += "2 "
                if self.mapa[f][c] == 3:
                    salida += "3 "
                if self.mapa[f][c] == 4:
                    salida += "4 "
                if self.mapa[f][c] == 5:
                    salida += "5 "
                if self.mapa[f][c] == 6:
                    salida += "6 "
                if self.mapa[f][c] == 7:
                    salida += "7 "
                if self.mapa[f][c] == 8:
                    salida += "1 "
                    
            salida += "\n"
            ##print(salida, "\n")
        return salida
    
    def camino(self, lista, i, coor):
        #del lista[-1]    
        print(coor)		
        self.mapa[lista[i][0]][lista[i][1]] = 6
        self.mapa[coor[0]][coor[1]] = 0            
		
class Nodo:
    def __init__(self, pos=[0, 0], padre=None):
        self.pos = pos
        ##print(self.pos)
        self.padre = padre
        ##print(padre)
        self.h = distancia(self.pos, pos_f)
        ##print(self.h)
 
        if self.padre == None:
            self.g = 0
        else:
            self.g = self.padre.g + 1
        self.f = self.g + self.h
        ##print(self.g)
        ##print(self.f)
        ##3

class AAsterisco:
    def __init__(self, mapa):
        self.mapa = mapa
        self.contador = 0
        ##print(mapa)
        
        # Nodos de inicio y fin.
        pos_inicial = buscarPos(6, mapa)
        print(pos_inicial)
        self.inicio = Nodo(pos_inicial)
        pos_final = buscarPos(4, mapa)
        print(pos_final)
        self.fin = Nodo(pos_final)
 
        # Crea las listas abierta y cerrada.
        self.abierta = []
        self.cerrada = []
 
        # Añade el nodo inicial a la lista cerrada.
        self.cerrada.append(self.inicio)
   
        # Añade vecinos a la lista abierta
        self.abierta += self.vecinos(self.inicio)
 
        # Buscar mientras meta no este en la lista cerrada.
        while self.meta():
            self.contador += 1
            if self.contador <= 13:
                self.buscar()
            else:
                break
 
        self.camino = self.camino()
        print(self.camino)
 
    # Devuelve una lista con los nodos vecinos transitables.
    def vecinos(self, nodo):
        vecinos   = []
        abajo     = [nodo.pos[0]+1 , nodo.pos[1]]
        arriba    = [nodo.pos[0]-1 , nodo.pos[1]]
        izquierda = [nodo.pos[0] , nodo.pos[1]-1]
        derecha   = [nodo.pos[0] , nodo.pos[1]+1]
        
        
        if self.mapa.mapa[abajo[0]][abajo[1]] != 1:
            vecinos.append(Nodo([abajo[0], abajo[1]], nodo))
    
        if self.mapa.mapa[arriba[0]][arriba[1]] != 1:
            vecinos.append(Nodo([arriba[0], arriba[1]], nodo))
            
        if self.mapa.mapa[izquierda[0]][izquierda[1]] !=1:
            vecinos.append(Nodo([izquierda[0], izquierda[1]], nodo))
            
        if self.mapa.mapa[derecha[0]][derecha[1]] != 1:
            vecinos.append(Nodo([derecha[0], derecha[1]], nodo))
            
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
 
    # Comprueba si un nodo está en una lista.
    def en_lista(self, nodo, lista):
        for i in range(len(lista)):
            if nodo.pos == lista[i].pos:
                return 1
        return 0
 
    # Gestiona los vecinos del nodo seleccionado.
    def ruta(self):
        for i in range(len(self.nodos)):
            if self.en_lista(self.nodos[i], self.cerrada):
                continue
            elif not self.en_lista(self.nodos[i], self.abierta):
                self.abierta.append(self.nodos[i])
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
            if self.fin.pos == self.abierta[i].pos:
                return 0
        return 1
 
    # Retorna una lista con las posiciones del camino a seguir.
    def camino(self):
        for i in range(len(self.abierta)):
            if self.fin.pos == self.abierta[i].pos:
                meta = self.abierta[i]
 
        camino = []
        while meta.padre != None:
            
            camino.append(meta.pos)
            meta = meta.padre
        camino.reverse()
        return camino
    
##//////////////////////////////////////////////



#Funciones /////////////////////////////////////

  
def distancia(a, b):
    ##print(a, "\n", b)
    dis = abs(a[0] - b[0]) + abs(a[1] - b[1]) #Valor absoluto.      
    return dis

def buscarPos(x, mapa):
    for f in range(mapa.fila):
        for c in range(mapa.columna):
            if mapa.mapa[f][c] == x:
                return [f, c]
            else: 
                if mapa.mapa[f][c] == 8:
                    return [f, c]
    return 0
    
# Quita el ultimo caracter de una lista.
def quitarUltimo(lista):
    for i in range(len(lista)):
        lista[i] = lista[i][:-1]
    return lista
 
# Covierte una cadena en una lista.
def listarCadena(cadena):
    lista = []
    for i in range(len(cadena)):
        if cadena[i] == "0":
            lista.append(0)
        if cadena[i] == "1":
            lista.append(1)
        if cadena[i] == "2":
            lista.append(2)
        if cadena[i] == "3":
            lista.append(3)
        if cadena[i] == "4":
            lista.append(4)
        if cadena[i] == "5":
            lista.append(5)
        if cadena[i] == "6":
            lista.append(6)
        if cadena[i] == "7":
            lista.append(7)
        if cadena[i] == "8":
            lista.append(8)
            
    return lista
 
# Lee un archivo de texto y lo convierte en una lista.
def leerMapa(archivo):
    mapa1 = open(archivo, "r")
    mapa1 = mapa1.readlines()
    mapa1 = quitarUltimo(mapa1)
    for i in range(len(mapa1)):
        mapa1[i] = listarCadena(mapa1[i])
    return mapa1

##////////////////////////////////////////////////////
    
   
def main():
    mapaEnd = Mapa()
    ##print(mapaEnd)
    globals()["pos_f"] = buscarPos(4, mapaEnd)
    globals()["bomba"] = True
    globals()["contBom"] = 0
    if(pos_f == 0):
        print("Meta no establecida")
    else:
        A = AAsterisco(mapaEnd)
        print(mapaEnd)
        for i in range(len(A.camino)):
            coor = buscarPos(6, mapaEnd)
            print(i)
            mapaEnd.camino(A.camino, i, coor)
            print(mapaEnd)
    return 0

if __name__ == '__main__':
	main()