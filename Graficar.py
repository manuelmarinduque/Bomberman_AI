from tkinter import Label, PhotoImage

class Graficar:

    def __init__(self):
        # Labels con las imágenes de los elementos del tablero:
        self.pared = PhotoImage(file="Images/lad.png")
        self.agente = PhotoImage(file="Images/mun.png")
        self.ladrillo = PhotoImage(file="Images/din.png")
        self.bomba = PhotoImage(file="Images/bom.png")
        self.puerta = PhotoImage(file="Images/pta.png")
        self.monstruo1 = PhotoImage(file="Images/mon1.png")

    def __del__(self):
        print("borrando objeto")    

    # Función que genera gráficamente el tablero: Recibe como parámetro una matriz o lista de listas:
    def generar_tablero(self, frame, lista):
        for n,i in enumerate(lista):
            for k,j in enumerate(i):
                    if j == 1: # Pared
                            Label(frame, image=self.pared, bd=0).grid(row=n, column=k)
                    if j == 2: # Ladrillo
                            Label(frame, image=self.ladrillo, bd=0).grid(row=n, column=k)
                    if j == 4: # Puerta
                            Label(frame, image=self.puerta, bd=0).grid(row=n, column=k)
                    if j == 5: # Monstruo
                            Label(frame, image=self.monstruo1, bd=0).grid(row=n, column=k)
                    if j == 6: # Agente
                            Label(frame, image=self.agente, bd=0).grid(row=n, column=k)
                    if j == 7: # Bomba
                            Label(frame, image=self.bomba, bd=0).grid(row=n, column=k)