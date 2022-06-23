# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:00:41 2022

@author: USUARIO
"""

import numpy as np
import pandas as pd

def biseccion(f, a, b, e, other):
    # f es la función que define f(x)=0. a y b son dos puntos tales que el signo de f(a) y el de f(b) son distintos. Finalmente, "e" es el "epsilon" que marca cuándo consideramos que podemos parar
    
    #print("      ")
    #print("------Biseccion-------")
    fa = f(a, other)
    fb = f(b, other)
    if np.sign(fa) == np.sign(fb):
        print("Error: la función tiene igual signo en los extremos")
        return # La función no devuelve ningún resultado
    else:
        #print("a=Extremo_izdo\tc=Punto_Medio\tb=Extremo_dcho\t\tf(c)") # Escribiremos una tabla para ir mostrando los resultados
        c = (a+b)/2
        fc = f(c, other)
        contador = 1
        #print(f"{a:.5f}\t\t\t{c:.5f}\t\t\t{b:.5f}\t\t\t{fc:.5f}")
        condicion_parada = (np.abs(fc) < e) or (np.abs(b-a)<e)
        while not(condicion_parada):
            if np.sign(fc) == np.sign(fa):
                a = c # El nuevo intervalo será [c,b], ahora se llama [a,b]
                fa = f(a, other)
                c = (a+b)/2 # El nuevo punto medio
                fc = f(c, other)
            else:
                b = c # El nuevo intervalo será [a,c], ahora se llama [a,b]
                fb = f(b, other)
                c = (a+b)/2 # El nuevo punto medio
                fc = f(c, other)
            condicion_parada = (np.abs(fc) < e) or (np.abs(b-a)<e)
            contador= contador+1
            #print(f"{a:.5f}\t\t\t{c:.5f}\t\t\t{b:.5f}\t\t\t{fc:.5f}")
        #print("La solución aproximada es c={}".format(c))
        #print("Las divisiones de intervalos realizadas son: ", contador)
    return c



path_n = './n_au.txt'
path_k = '.k_au.txt'

data_n = pd.read_csv(path_n, '\t')
data_k = pd.read_csv(path_k, '\t')

wl = data_n['wl']*10**-6 #en m
n = data_n['n']
k = data_k['k']

limm = min(wl)-(max(wl)-min(wl))*0.05
limM = max(wl)+(max(wl)-min(wl))*0.05

xx = np.linspace(limm, limM, 200)
grado_polinomio = 6
pol_n = np.polyfit(wl, n, grado_polinomio)
pol_k = np.polyfit(wl, k, grado_polinomio)

nn = np.polyval(pol_n, xx)
kk = np.polyval(pol_k,xx)

def lamB(l, e_d):

    def e_m_(l):
        n_R = np.polyval(pol_n, l)
        n_I = np.polyval(pol_k,l)
        e_R = n_R**2 - n_I**2
        e_I = 2*n_R*n_I
        e_m = complex(e_R, e_I)
        return e_m
    e_m = e_m_(l)
    l_spp = P/ij*np.sqrt((e_d*e_m)/(e_d+e_m))
    return l-l_spp.real



P =550*10**-9  #periodo
#modos de vibracion
i = 1
j = 0
ij = np.sqrt(i**2+j**2)

e_d = 1.33**2     #constante dielectrica del medio
#Intervalo de la solucion
l_min = 10*10**-9 
l_max = 1000*10**-9
dl = 0.03*10**-9  #error de la solucion numerica

sol = biseccion(lamB, l_min, l_max, dl, e_d)
print('lambda = {}'.format(sol))
