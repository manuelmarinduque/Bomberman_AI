import random

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

def posEncontrada(mapa, lista):
    posFinal = buscarPos(4, mapa)
    if(posFinal == 0) and (len(lista) != 0):
        posFinal = lista[0]
        del lista[0]
        #print(globals()["listaLadrillos"])
    return [posFinal, lista]
 
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