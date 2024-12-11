# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 08:32:55 2024

@author: Samuel Brambila
"""

import matplotlib.pyplot as plt
import numpy as np

def polinomio(x):
    return 3*x**4-5*x**3+2*x**2-7*x+4

def primer_derivada(x):
    return 12*x**3-15*x**2+4*x-7

def segunda_derivada(x):
    return 36*x**2-30*x+4

t = np.arange(-5,7,0.5)
plt.figure()
plt.grid()
plt.suptitle(r'Gráfico de $f(x)$ y sus derivadas')
plt.xlabel('Valores del arreglo')
plt.ylabel('Valores evaluados en la función y sus derivadas')

plt.plot(t, polinomio(t), 'r*-', label='Polinomio',
         t, primer_derivada(t), 'bo-', label='Primera derivada',
         t, segunda_derivada(t), 'ks-', label='Segunda derivada')
plt.legend()
plt.savefig('grafico_final.eps', format='eps')
plt.show()

