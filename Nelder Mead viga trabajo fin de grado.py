from random import * #random
import random
import math
import numpy as np #vectores
import pandas as pd #Para cargar datos
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

print("NELDER MEAD")
longitud = 500
densidad = 7850/(10**6)
peso = 1
young = 21000

def area(punto):
    area = punto[0]*punto[1]
    return area

def desplazamiento(punto):
    a,b = punto[0], punto[1]
    momento_inercia = (a*(b)**3)/12
    desplazamiento = ((peso*(longitud)**3)/(3*young*momento_inercia)) 
    return desplazamiento


def func_to_optimize(vars):
    punto = vars
    valor_funcion = area(punto)*longitud*densidad
    print(desplazamiento(punto))
    if desplazamiento(punto) >= (longitud/300):
        valor_funcion = 1000000000000000000000000000000000000000000
    return valor_funcion
    
restricciones = ({'type': 'ineq', 'fun': lambda x: x[0] - 1e-5},  # a > 0
                 {'type': 'ineq', 'fun': lambda x: x[1] - 1e-5})  # b > 0

# Establecer un punto inicial dentro de los límites permitidos
initial_guess = np.array([1.32, 22.22])


# Aplicar el método de Nelder-Mead
result = minimize(func_to_optimize, initial_guess, constraints=restricciones, method='Nelder-Mead')

# Imprimir los resultados
print("Resultado de la optimización:")
print(result.x)

print("Valor de la función =", result.fun)
