# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 17:03:23 2024

@author: SamuelBrambila
"""

import matplotlib.pyplot as plt
import numpy as np

# Comparación de ecuaciones/polinomios de los método burbuja según el conteo de operaciones

# Burbuja no mejorado
def burbuja_no_mejorado(n):
    return 15*n**2 - 9*n + 8

# Burbuja mejorado
def burbuja_mejorado(n):
    return 16*n**2 - 7*n + 8

# Valores de n
t = np.arange(1, 40, 2)

# Graficar
plt.figure()
plt.grid()
plt.suptitle('Comparación de burbuja no mejorado vs burbuja mejorado')
plt.xlabel('Tamaño del arreglo (n)')
plt.ylabel('Operaciones según la ecuación')
plt.plot(t, burbuja_no_mejorado(t), 'bo-', label='Burbuja no mejorado')
plt.plot(t, burbuja_mejorado(t), 'ks-', label='Burbuja mejorado')
plt.legend()
plt.savefig('grafico_burbujas.eps', format='eps')
plt.show()


# Comparación de los 3 códigos compartidos por el profesor

# Decimal binario 1
def decimal_binario_1(numero):
    return 13 + 14*np.log2(numero)

# Decimal binario 2
def decimal_binario_2(numero):
    return 13 + 15*np.log2(numero)

# Decimal binario 3
def decimal_binario_3(numero):
    return 9 + 10*np.log2(numero)

# Valores muestra de números
nums = np.arange(1,10,1)

# Gráfica 2
plt.figure()
plt.grid()
plt.suptitle('Comparación de 3 algoritmos de conversión de decimal a binario')
plt.xlabel('Número ingresado')
plt.ylabel('Operaciones')
plt.plot(nums, decimal_binario_1(nums), 'ks-', label='Decimal Binario 1')
plt.plot(nums, decimal_binario_2(nums), 'bo-', label='Decimal Binario 2')
plt.plot(nums, decimal_binario_3(nums), 'r*-', label='Decimal Binario 3')
plt.legend()
plt.savefig('grafico_decimal-binario.eps', format='eps')
plt.show()







