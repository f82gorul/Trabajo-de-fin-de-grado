import matplotlib.pyplot as plt
import random
import numpy as np
import time

seed = 3
random.seed(seed)
np.random.seed(seed)

t1 = time.time() #Para calcular el tiempo de ejecución

import matplotlib.pyplot as plt
import random
import numpy as np

seed = 3
random.seed(seed)
np.random.seed(seed)

class Evolutivo:
    def __init__(self, longitud, densidad, peso, young, num_generaciones, tamaño_poblacion, prob_mutacion=0.05):
        self.longitud = longitud
        self.densidad = densidad
        self.peso = peso
        self.young = young
        self.num_generaciones = num_generaciones
        self.tamaño_poblacion = tamaño_poblacion
        self.prob_mutacion = prob_mutacion 
        
        self.poblacion = []
        self.poblacion_hijos = []
        self.poblacion_padres = []
        self.poblacion_completa = []
        self.mejores_areas = []
        self.probabilidades_mutacion = []
        self.areas_poblaciones = []
        self.mejor_masa = []
        
    def area(self, punto):
        (a, b) = punto
        area = a * b
        return area
    
    def desplazamiento(self, punto):
        (a, b) = punto
        momento_inercia = (a * (b)**3) / 12
        desplazamiento = ((self.peso * (self.longitud)**3) / (3 * self.young * momento_inercia)) 
        return desplazamiento

    def funcion_optimizar(self, punto):
        (a, b) = punto
        valor_funcion = self.area(punto) * self.longitud * self.densidad
        if self.desplazamiento(punto) >= (self.longitud / 300):
            valor_funcion = valor_funcion + 1000 * self.desplazamiento(punto)
        return valor_funcion
    
    def crea_individuos(self):
        a = random.uniform(0.001, 100)
        b = random.uniform(0.001, 100)
        punto = (a, b)
        valor = self.funcion_optimizar(punto)
        return (a, b, valor)
 
    def crea_poblacion(self):
        while len(self.poblacion) < self.tamaño_poblacion:
            individuo = self.crea_individuos()
            if individuo not in self.poblacion:
                self.poblacion.append(individuo)
        return self.poblacion

    def seleccion_ruleta_padres(self, k=4):
        copia_poblacion = self.poblacion.copy()
        while len(self.poblacion_padres) < int(self.tamaño_poblacion * 0.5):
            indices = np.random.choice(len(copia_poblacion), k, replace=False)
            padres_posibles = [copia_poblacion[i] for i in indices]
            grupo_ordenado = sorted(padres_posibles, key=lambda ind: ind[2])
            for padre in grupo_ordenado[:1]:
                self.poblacion_padres.append(padre)
                copia_poblacion.remove(padre)
        return self.poblacion_padres
    
    def cruce(self, individuo1, individuo2):
        hijo1 = (individuo1[0], individuo2[1])
        hijo1_valor = self.funcion_optimizar(hijo1)

        hijo2 = (individuo2[0], individuo1[1])
        hijo2_valor = self.funcion_optimizar(hijo2)
        
        return (hijo1[0], hijo1[1], hijo1_valor), (hijo2[0], hijo2[1], hijo2_valor)
    
    def crea_poblacion_hijos(self): 
        for i in range(0, len(self.poblacion_padres) - 1, 2): 
            padre1 = self.poblacion_padres[i] 
            padre2 = self.poblacion_padres[i + 1]
            hijo1, hijo2 = self.cruce(padre1, padre2)
            self.poblacion_hijos.append(hijo1)
            self.poblacion_hijos.append(hijo2)
        return self.poblacion_hijos

    def mutacion(self, individuo):
        a, b, valor = individuo
        if random.random() < self.prob_mutacion:
            posible_a = random.uniform(0.001, 100)
            if 0 < posible_a < b:
                a = posible_a
                valor = self.funcion_optimizar((a, b))
        if random.random() < self.prob_mutacion:
            posible_b = random.uniform(0.001, 100)
            if a < posible_b:
                b = posible_b
                valor = self.funcion_optimizar((a, b))
        return (a, b, valor)
    
    def crea_poblacion_hijos_mutados(self):
        for i in range(len(self.poblacion_hijos)):
            mutacion_hijo = self.mutacion(self.poblacion_hijos[i])
            self.poblacion_hijos[i] = mutacion_hijo 
        return self.poblacion_hijos

    def crea_poblacion_completa(self):
        self.poblacion_completa = self.poblacion + self.poblacion_hijos
        return self.poblacion_completa

    def seleccion_elitista(self):
        self.poblacion_completa.sort(key=lambda x: x[2], reverse=False)  
        self.poblacion = self.poblacion_completa[0:self.tamaño_poblacion]  
        return self.poblacion

    def run(self):
        prob_mut_ini = self.prob_mutacion
        pop_cambiada = 0
        gen_sin_mejora = 0
        mejor_anterior = 100000000000000000000000000000
        self.crea_poblacion()
        print("La población inicial es:", self.poblacion)
        for g in range(self.num_generaciones):
            self.poblacion_padres = []
            self.poblacion_hijos = []
            self.seleccion_ruleta_padres()
            self.crea_poblacion_hijos()
            self.crea_poblacion_hijos_mutados()
            pob_hijos_aux = []
            for ind in self.poblacion_hijos:
                if ind not in self.poblacion:
                    pob_hijos_aux.append(ind)
            self.poblacion_hijos = pob_hijos_aux
            self.crea_poblacion_completa()
            self.poblacion = self.seleccion_elitista()
            mejor_individuo = self.poblacion[0]
            mejor_area = self.area((mejor_individuo[0], mejor_individuo[1]))
            self.mejores_areas.append(mejor_area)
            self.areas_poblaciones.append([self.area((p[0], p[1])) for p in self.poblacion])  # Almacenar áreas de la población actual
            self.probabilidades_mutacion.append(self.prob_mutacion)
            self.mejor_masa.append(self.funcion_optimizar((mejor_individuo[0], mejor_individuo[1])))

            best = self.poblacion[0]
            a_mejor, b_mejor, valor_mejor = self.poblacion[0]
            if valor_mejor < mejor_anterior:
                mejor_anterior = valor_mejor
                gen_sin_mejora = 0
                self.prob_mutacion = prob_mut_ini
                pop_cambiada = 0
            else:
                gen_sin_mejora += 1
            if gen_sin_mejora > 100:
                self.prob_mutacion = self.prob_mutacion + 0.05
                gen_sin_mejora = 0
            print("Tras la generación: ", g, " el mejor es: ", self.poblacion[0], "\n")
            print("Probabilidad de mutación: ", self.prob_mutacion)

            if self.prob_mutacion > 1:
                self.poblacion = []
                self.crea_poblacion()
                self.poblacion[0] = best
                self.prob_mutacion = prob_mut_ini
                gen_sin_mejora = 0
                pop_cambiada = pop_cambiada + 1

            if pop_cambiada > 2:
                print("CORTA POR CONVERGENCIA")
                break
        
        return self.poblacion[0]
    
        
    def grafica_masa(self):
        generaciones = range(1, len(self.mejor_masa) + 1)
        plt.plot(generaciones, self.mejor_masa, color='green', linestyle='-', marker='', label='Masa del Mejor Individuo')
        plt.xlabel('Generación')
        plt.ylabel('Masa')
        plt.title('Evolución de la masa')
        plt.grid(True)
        plt.legend()
        plt.show()
        

# Ejecución del algoritmo
evol = Evolutivo(500, (7850 / (10**6)), 10, 21000, 80000, 100, 0.05)
evol.run()
evol.grafica_masa()


t2 = time.time()

print("Tiempo: ", t2-t1)


