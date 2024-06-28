#CARGO PAQUETES
from random import * #random
import random
import numpy as np #vectores
import pandas as pd #Para cargar datos
import matplotlib.pyplot as plt  # Biblioteca para graficar
import time

seed = 2 #Establezco semillas
random.seed(seed)
np.random.seed(seed)

t1 = time.time() #Para calcular el tiempo de ejecución

class evolutivo: #Creo clase del evolutivo
    def __init__(self, pesos, valores, num_generaciones, peso_max, tamaño_poblacion, prob_mutacion=0.05):
        self.pesos = pesos
        self.valores = valores
        self.num_generaciones = num_generaciones
        self.peso_max = peso_max
        self.longitud_individuo = len(pesos) 
        self.poblacion = []
        self.tamaño_poblacion = tamaño_poblacion
        self.poblacion_hijos = []
        self.prob_mutacion = prob_mutacion 
        self.poblacion_hijos_mutados = []
        self.poblacion_completa = []
        self.poblacion_evaluada = []
        self.valores_medios_por_generacion = []  # Para almacenar el mejor valor por generación

   #FUNCIÓN QUE ME CREA INDIVIDUOS: COGE LOS PESOS Y LE PONE 0 Y 1 ALEATORIAMENTE: 1 ENTRA MOCHILA, 0 NO ENTRA.
   #SE CREA CON LA RESTRICCIÓN DE QUE PESOMAX=11. HAGO SUMATORIO EN EL TAMAÑO DE LA POBLACIÓN Y OBTENGO POBLACIÓN.
    
    def crea_individuos(self):
        suma = 0
        individuo = []
        for i in range (self.longitud_individuo):
            valor = randint(0,1) #Mete enteros aleatorios 0 y 1
            if valor == 1:
                posible_suma = suma + self.pesos[i]
                if posible_suma >= self.peso_max:
                    valor = 0
                else:
                    suma = suma + self.pesos[i]
            individuo.append(valor)
        valor_ev = sum(self.valores[i] for i in range(len(individuo)) if individuo[i] == 1)

        return {"Individuo": individuo, "Valor": valor_ev}
    def crea_poblacion(self):
        for i in range (self.tamaño_poblacion):
            self.poblacion.append(self.crea_individuos())
        return self.poblacion
    
    

    def cruce(self, individuo1, individuo2, indice=2): 
        parte_individuo1 = individuo1[0:indice] #NORMAL
        parte_individuo2 = individuo2[indice:] 

        parte_individuo1_inv = individuo1[indice:] #A LA INVERSA. Asi voy creando más hijos.
        parte_individuo2_inv = individuo2[0:indice]

        individuo3 = [] #Por cada dos padres de "normal" creo un hijo.
        individuo4 = [] #Por cada dos padres de "a la inversa" creo un hijo.
        
        # Manejo de la primera parte de los individuos
        for el in parte_individuo1:
            individuo3.append(el)
        for el in parte_individuo2:
            individuo3.append(el)
        for el in parte_individuo2_inv:
            individuo4.append(el)
        for el in parte_individuo1_inv:
            individuo4.append(el)

        # Aplicación de las restricciones de peso máximo. 
        pesos3 = sum(self.pesos[i] for i in range(len(individuo3)) if individuo3[i] == 1)
        pesos4 = sum(self.pesos[i] for i in range(len(individuo3)) if individuo3[i] == 1)

        
        valor3 = sum(self.valores[i] for i in range(len(individuo3)) if individuo3[i] == 1)

        valor4 = sum(self.valores[i] for i in range(len(individuo4)) if individuo4[i] == 1)

        if pesos3 > self.peso_max:
            valor3 = -1000000

        if pesos4 > self.peso_max:
            valor4 = -1000000



        return {"Individuo": individuo3, "Valor": valor3}, {"Individuo": individuo4, "Valor": valor4}
        
 

    #Creo población de hijos generados de haber hecho el cruce
    def crea_poblacion_hijos(self):
        for i in range(0,self.tamaño_poblacion-1,2):
            padre1 = self.poblacion[i]["Individuo"]  #CREA PADRES. 
            padre2 = self.poblacion[i+1]["Individuo"]
            hijo1,hijo2 = self.cruce(padre1, padre2)
            
            self.poblacion_hijos.append(hijo2)
            self.poblacion_hijos.append(hijo1)
        return self.poblacion_hijos
    
    #AHORA CREO OTRA NUEVA POBLACIÓN DE HIJOS CON LA MUTACIÓN
    def mutacion(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.prob_mutacion:
                individuo[i] = 1 if individuo[i] == 0 else 0
        pesos_in = sum(self.pesos[i] for i in range(len(individuo)) if individuo[i] == 1)
        valor = -1000000
        if pesos_in <=self.peso_max:
            valor = sum(self.valores[i] for i in range(len(individuo)) if individuo[i] == 1)
            
        return {"Individuo": individuo, "Valor": valor}
        
    def crea_poblacion_hijos_mutados(self):
        for i in range(len(self.poblacion_hijos)):
            mutacion_hijo=self.mutacion(self.poblacion_hijos[i]["Individuo"])
            
            self.poblacion_hijos[i]=mutacion_hijo

        return self.poblacion_hijos
    

    def crea_poblacion_completa(self): #Creo población completa de padres, hijos (m+c)
        
        self.poblacion_completa = self.poblacion + self.poblacion_hijos
     
        return self.poblacion_completa

    def seleccion_elitista(self):
        self.poblacion_completa.sort(key=lambda x: x["Valor"], reverse=True) 
        self.poblacion = self.poblacion_completa[0:self.tamaño_poblacion]
        return self.poblacion
    
    def graficar_resultados(self):
        plt.plot(range(1, self.num_generaciones + 1), self.valores_medios_por_generacion, marker=' ', color="blue", linestyle='solid', linewidth=1.2, markersize=5)
        plt.xlabel('Generación')
        plt.ylabel('Valor medio')
        plt.title('Evolución del valor medio de la población')
        plt.grid(True)
        plt.show()

    def run(self):
        self.crea_poblacion()
        print("Población inicial: ", self.poblacion)
        for g in range(self.num_generaciones):
            self.poblacion_hijos = []
            self.crea_poblacion_hijos()
            self.crea_poblacion_hijos_mutados()
            self.crea_poblacion_completa()
            self.seleccion_elitista()
            print("Tras la generación: ", g, " la población es: ", self.poblacion, "\n")
            # Calcular el valor medio de la generación actual y almacenarlo
            valores_generacion = [individuo["Valor"] for individuo in self.poblacion]
            valor_medio = np.mean(valores_generacion)
            self.valores_medios_por_generacion.append(valor_medio)
        self.graficar_resultados()

evol = evolutivo([1,5,3,2,4], [10,50,20,30,60], 100, 11, 4)
evol.run()

t2 = time.time()

print("Tiempo: ", t2-t1)

