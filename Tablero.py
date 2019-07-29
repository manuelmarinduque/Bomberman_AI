import random

class Tablero:

    ran=random.randint(15, 20)
    archivo=open("aleatoria.txt","w")
    meta = []

    def __generar_tablero_base(self):
        matriz = []
        for i in range(11):
            matriz.append([])
            for j in range(self.ran):
                if j % 2 == 0 and i % 2 == 0 or i == 0 or j==0 or i==10 or j==self.ran-1:
                    matriz[i].append(1)
                else:
                    matriz[i].append(0)
        return matriz

    def GenLadrillos(self):
        m = self.__generar_tablero_base()
        b=self.ran*11 # Numero de casillas
        a=int(b*0.2) # Numero de ladrillos
        c=3 # Numero de mostruos 
        m[1][1]=m[1][1]+6
        while c>0: # Ciclo para generar los monstruos
            x=random.randint(0, 10 )
            y=random.randint(0, self.ran-1)
            if m[x][y]==0 and y%2==0 and (x>2 or y>2): # Se generan lejos del agente en cualquier posicion donde exista un 0
                m[x][y]=m[x][y]+5
                c=c-1         
        while a>0: # Ciclo para generar los ladrillos 
            x=random.randint(0, 10 )
            y=random.randint(0, self.ran-1)  
            if m[x][y]==0 and (x>2 or  y>2 ):
                m[x][y]=m[x][y]+2
                # Generar meta en el último ladrilo generado aleatoriamente:
                if a == 1:
                    self.meta.append(x)
                    self.meta.append(y)
                a=a-1
        for i in range(11):
            for j in range(self.ran):
                self.archivo.writelines('% s'%m[i][j])
            self.archivo.writelines('\n')
        self.archivo.close()
        return m

    def GenMeta(self):
        return self.meta
