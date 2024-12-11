# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 07:29:24 2024

@author: samue
"""

# Conteo de operaciones
    # Asignación de variables
    # Operaciones aritméticas
    # Operaciones booleanas
    # Acceso a arreglos
    # Prints
    
if (a==3):  # 1 
    a = a+1 # 2
    b = a+3 # 2
    c = b+a = 3 # 3
else:
    a = a-1 # 2
    
# Verdadero (8 operaciones)
# Falso (3 operaciones)


def busLineal(A,n,elemento):
    for i in range(n):
        if(A[i] == elemento):   # 2
            return i
    return -1

# El for es una sumatoria de i = 0 a n-1
# Quedando 1 (limite final) + 1 (inicio) + la sumatoria del for con 3 de rigor 
# (2 del incremento y 1 de comparación), quedando 5n+2

for i in range(n):
    for j in range(n-1):
        if(A[j]>A[j+1]):  # 4
            temp = A[j]   # 2
            A[j] = A[j+1] # 4
            A[j+1] = temp # 3
            
            
# Tarea
# Investigar como puedo saber cuantas veces puedo dividir un número entre otro (operación matemática)
# Sacar el polinomio de los algoritmos de los códigos que subirá el profe y graficarlos
# En una gráfica, poner el burbuja y el burbuja mejorado
# Los otros parecidos van en otra gráfica

            