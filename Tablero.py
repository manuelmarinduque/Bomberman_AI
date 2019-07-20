import random # Para generar numeros aleatorios
from io import open # Para generacion de txt
from tkinter import mainloop, Tk, Frame, PhotoImage, Label


# Generar el archivo de texto:
archivo=open("aleatoria.txt","w") # Genera un archivo txt "w" hace referencia a que vamos a escribir en el
ran=random.randint(15, 20) # Se crea una variable random entre 15 y 20 para generar el # de columnas aleatorias

# Se crea el tablero base sin ladrillos validando las orillas del tablero con unos y los muros del medio:
matriz = []
for i in range(11):
	matriz.append([])

	for j in range(ran):
		if j % 2 == 0 and i % 2 == 0 or i == 0 or j==0 or i==10 or j==ran-1:
			matriz[i].append(1)
		else:
			matriz[i].append(0)

# Función que genera los ladrillos: Recibe como parámetro una matriz:
def GenLadrillos(m):
	b=ran*11 # Numero de casillas
	a=int(b*0.2) # Numero de ladrillos
	c=3 # Numero de mostruos 

	m[1][1]=m[1][1]+6

	while c>0: # Ciclo para generar los monstruos
		x=random.randint(0, 10 )
		
		y=random.randint(0, ran-1)
		if m[x][y]==0 and y%2==0 and (x>2 or y>2): # Se generan lejos del agente en cualquier posicion donde exista un 0
			m[x][y]=m[x][y]+5
			c=c-1

				
	while a>0: # Ciclo para generar los ladrillos 
		x=random.randint(0, 10 )
		
		y=random.randint(0, ran-1)

				
		if m[x][y]==0 and (x>2 or  y>2 ):
			m[x][y]=m[x][y]+2	
	
			a=a-1
	return m

# Se genera la matriz tablero pasando como parámetro la matriz del tablero base:
tablero = GenLadrillos(matriz)

# ----------------------------------- Parte gráfica -----------------------------------

# Ventana raiz:
root = Tk()
root.title("Juego Boomberman")

# Frame que contiene los elementos del tablero:
miFrame = Frame(root, bg="#4ca404")
miFrame.pack()

# Labels con las imágenes de los elementos del tablero:
pared = PhotoImage(file="Images/lad.png")
agente = PhotoImage(file="Images/mun.png")
ladrillo = PhotoImage(file="Images/din.png")
bomba = PhotoImage(file="Images/bom.png")
puerta = PhotoImage(file="Images/pta.png")
monstruo1 = PhotoImage(file="Images/mon1.png")

# Función que genera gráficamente el tablero: Recibe como parámetro una matriz o lista de listas:
def generar_tablero(lista):
    for n,i in enumerate(lista):
        for k,j in enumerate(i):
                if j == 1: # Pared
                        Label(miFrame, image=pared, bd=0).grid(row=n, column=k)
                if j == 2: # Ladrillo
                        Label(miFrame, image=ladrillo, bd=0).grid(row=n, column=k)
                if j == 4: # Puerta
                        Label(miFrame, image=puerta, bd=0).grid(row=n, column=k)
                if j == 5: # Monstruo
                        Label(miFrame, image=monstruo1, bd=0).grid(row=n, column=k)
                if j == 6: # Agente
                        Label(miFrame, image=agente, bd=0).grid(row=n, column=k)
                if j == 7: # Bomba
                        Label(miFrame, image=bomba, bd=0).grid(row=n, column=k)

# Se genera el tablero pasando como parámetro la matriz "tablero" que hace referencia a la función GenLadrillos():
generar_tablero(tablero)

# Siempre el mainloop al final:
root.mainloop()
