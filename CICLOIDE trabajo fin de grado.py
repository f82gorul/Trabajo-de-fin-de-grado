#CARGO PAQUETES
from random import * #random
import random
import math
import numpy as np #vectores
import pandas as pd #Para cargar datos
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


seed = 2
random.seed(seed)
np.random.seed(seed)


class evolutivo:
    def __init__(self, xf, yf, num_generaciones, num_puntos, tamaño_poblacion, prob_mutacion=0.05):
        self.xf = xf
        self.yf = yf
        self.num_puntos = num_puntos 
        self.num_generaciones = num_generaciones
        self.poblacion = []
        self.tamaño_poblacion = tamaño_poblacion
        self.poblacion_hijos = []
        self.poblacion_padres = []
        self.prob_mutacion = prob_mutacion 
        self.poblacion_completa = []
        self.poblacion_evaluada = []
   
    def funcion_optimizar(self, punto, p_anterior):
        g = 9.81
        [x, y] = punto

        [x_ant, y_ant] = p_anterior
        tiempo =(math.sqrt(2/g))* (math.sqrt((x - x_ant)**2 + (y - y_ant)**2)/(math.sqrt(-y)+ math.sqrt(-y_ant)))
        
        return tiempo

    def crea_individuos(self): 
        vector_puntos = []
        tiempo_total = 0
        
        for i in range(self.num_puntos):
            if i==0:
                punto_anterior = (0,0)
                rango_x = (0,5)
            else:
                punto_anterior = (x, y)
                rango_x = (x,5)

            x = random.uniform(*rango_x) 
            y = random.uniform(-5, 0)
            punto = (x,y)
            
            tiempo = self.funcion_optimizar(punto, punto_anterior)
            vector_puntos.append([x,y,tiempo])
            tiempo_total = tiempo_total + tiempo #suma el tiempo de cada vector a tiempo_total
        tiempo_total += self.funcion_optimizar((self.xf,self.yf), (x,y))
        return {"Individuo": vector_puntos, "Tiempo Total": tiempo_total}
    
    def crea_poblacion(self): #He añadido restricción porque me generaba individos iguales
        while len(self.poblacion) < self.tamaño_poblacion:
            individio = self.crea_individuos()
            if individio not in self.poblacion:
                self.poblacion.append(individio)
        return self.poblacion

    def seleccion_ruleta_padres(self, k=4):
   
        copia_poblacion = self.poblacion
        for i in range(int(self.tamaño_poblacion*0.5)):

            padres_posibles = np.random.choice(copia_poblacion, k, replace=False)
            grupo_ordenado = sorted(padres_posibles, key=lambda ind: ind["Tiempo Total"]) 
            copia_poblacion = [individuo for individuo in copia_poblacion if individuo not in [grupo_ordenado[0]]]

            self.poblacion_padres.append(grupo_ordenado[0])

        return self.poblacion_padres

    def cruce(self, individuo1, individuo2):
        individuo3 = []
        tiempo_total3 = 0
        i = 0
        for punto1, punto2 in zip(individuo1, individuo2):
            if i==0:
                p_anterior = (0,0)
            else:
                p_anterior = (punto3[0], punto3[1])
            punto3 = [(punto1[0] + punto2[0]) / 2, (punto1[1] + punto2[1]) / 2]
            tiempo3 = self.funcion_optimizar(punto3, p_anterior)
            individuo3.append([punto3[0], punto3[1], tiempo3])
            tiempo_total3 = tiempo_total3 + tiempo3
         
            i = i+1
        tiempo_total3 += self.funcion_optimizar((self.xf,self.yf), (punto3[0],punto3[1]))

        return {"Individuo": individuo3, "Tiempo Total": tiempo_total3}
    
    def crea_poblacion_hijos(self): #Creo población de hijos generados de haber hecho el cruce.
        for i in range(0, len(self.poblacion_padres)-1, 2): 
            padre1 = self.poblacion_padres[i]["Individuo"]  #CREA PADRES. 
            padre2 = self.poblacion_padres[i+1]["Individuo"] 
            hijo1 = self.cruce(padre1, padre2)
            #self.poblacion_hijos.append(hijo2)
            self.poblacion_hijos.append(hijo1)
        return self.poblacion_hijos 
     
    def mutacion(self, individuo): #Solo muto la y
        tiempo_total_mut = 0
        #tiempo_total_individuo = 0
        for i in range(len(individuo)):
            if random.random() < self.prob_mutacion:
                if i==0:
                    p_anterior = (0,0)
                else:
                    p_anterior = (individuo[i-1][0], individuo[i-1][1])

                individuo[i][1] = random.uniform(-5, 0)
                individuo[i][2] = self.funcion_optimizar((individuo[i][0], individuo[i][1]), p_anterior)
                if i!=self.num_puntos-1:
                    individuo[i+1][2] = self.funcion_optimizar((individuo[i+1][0], individuo[i+1][1]), (individuo[i][0], individuo[i][1]))
                
            tiempo_total_mut += individuo[i][2]
        tiempo_total_mut += self.funcion_optimizar((self.xf,self.yf), (individuo[len(individuo)-1][0], individuo[len(individuo)-1][1]))

        return {"Individuo": individuo, "Tiempo Total": tiempo_total_mut}
        
    def crea_poblacion_hijos_mutados(self):
        for i in range(len(self.poblacion_hijos)):
            mutacion_hijo = self.mutacion(self.poblacion_hijos[i]["Individuo"])
            self.poblacion_hijos[i]["Individuo"] = mutacion_hijo["Individuo"]  
            self.poblacion_hijos[i]["Tiempo Total"] = mutacion_hijo["Tiempo Total"] 
        return self.poblacion_hijos

    def crea_poblacion_completa(self): #Creo población completa de padres, hijos (m+c)
        self.poblacion_completa = self.poblacion + self.poblacion_hijos
        return self.poblacion_completa

    def seleccion_elitista(self):
        self.poblacion_completa.sort(key=lambda x: x["Tiempo Total"], reverse=False)  # Ordena la población completa por tiempo de menor a mayor
        self.poblacion = self.poblacion_completa[0:self.tamaño_poblacion]  # Selecciona los mejores del tamaño de la población
        return self.poblacion

    def run(self):
        self.crea_poblacion()  # Crear la población inicial
        print("La población inicial es:", self.poblacion)
        mejor = self.poblacion[0]
        generaciones_sin_cambio = 0
        for g in range(self.num_generaciones):
            self.poblacion_padres = []
            self.poblacion_hijos = []
    
            self.seleccion_ruleta_padres()
            
            self.crea_poblacion_hijos()
            
            self.crea_poblacion_hijos_mutados()
    
            self.crea_poblacion_completa()
            
            self.poblacion = self.seleccion_elitista()
            if mejor["Tiempo Total"] <= self.poblacion[0]["Tiempo Total"]:
                generaciones_sin_cambio+=1
            else:
                generaciones_sin_cambio = 0
                mejor = self.poblacion[0]
            
            print(f"Tras la generación {g}, el mejor es:", self.poblacion[0], "\n")

            if generaciones_sin_cambio == 500:
                return mejor
        return mejor

evol = evolutivo(5, -5, 1000, 2, 20, 0.05)
mejor = evol.run()
print("MEJOR: ", mejor)


# Constante gravitacional
g = 9.81

# Valores de self.xf y self.yf.
xf = 5
yf = -5

para_pintar_evolutivo_x = [0]
para_pintar_evolutivo_y = [0]

for punto in mejor["Individuo"]:
    print(punto)
    para_pintar_evolutivo_x.append(punto[0])
    para_pintar_evolutivo_y.append(punto[1])

para_pintar_evolutivo_x.append(5)
para_pintar_evolutivo_y.append(-5)

# Definición de la función cicloide
def cicloide(tita):
    return (1 - np.cos(tita)) / (tita - np.sin(tita)) + yf / xf

# Resolviendo la ecuación para encontrar titaG
titaG = fsolve(cicloide, np.pi)[0]
titaGgrados = titaG * 180 / np.pi

# Cálculo de R
R = -yf / (1 - np.cos(titaG))

# Creación de puntos en el rango de tita
vtita = np.linspace(0, titaG, 1000)
vx = R * (vtita - np.sin(vtita))
vy = -R * (1 - np.cos(vtita))


# Graficando la función cicloide y el evolutivo
plt.plot(vx, vy, 'b', color="red", label='Cicloide')
plt.plot(para_pintar_evolutivo_x, para_pintar_evolutivo_y, color='blue', label='Algoritmo Genético')

# Ajustes de la gráfica
plt.axis('equal')
plt.title('n = 3')
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()

