# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 19:03:48 2022

@author: USUARIO
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import argrelextrema


class Espectros:
    '''
    Lee datos, plotearlos y conseguir máximos y minimos
    El header del archivo tiene que ser lambda \tabulacion T
    '''
    def __init__(self, nombre, **kwargs):
        sep='\t'

        if 'sep' in kwargs:
            sep = kwargs['sep']
            if sep == 'defecto':
                self.data = pd.read_csv(nombre)
            else:
                sep = kwargs['sep']
                self.data = pd.read_csv(nombre, sep)
        else:
            self.data = pd.read_csv(nombre, sep)
        
        self.name = nombre
        self.lambdas = np.array(self.data['lambda'])
        self.transmitancia = np.array(self.data['T'])

        if 'und' in kwargs:
            if kwargs['und'] == 'm':
                self.lambdas= self.lambdas*10**9
                self.transmitancia = self.transmitancia*100
        sigm = 10
        if kwargs.get('sigma')!=None:
            sigm = kwargs['sigma']
        
        self.transmitanciaG = gaussian_filter1d(self.transmitancia, sigma=sigm)
        
        self.leyenda = None
        if kwargs.get('leyenda')!=None: 
            self.leyenda = kwargs['leyenda']
            
        self.color = None
        if kwargs.get('color')!=None:
            self.color = kwargs['color']
        
    def __str__(self):
        
        return self.lambdas
    
    def plotear(self, **kwargs):    
        S = 15
        label= self.leyenda
        l = False
        if 'label' in kwargs and self.leyenda ==None:
            label = kwargs['label']
            l = True
        plt.plot(self.lambdas, self.transmitancia, '-', markersize=S, 
                 color=self.color, label = r'{}'.format(label))
        plt.xlabel(r'$\lambda$ / nm', size=15)
        plt.ylabel(r'$T$ / %', size=15)
        #plt.ylim(0, 12)
        plt.xlim(602, 880)
        
        if self.leyenda != None or l==True:
            plt.legend(loc= 'best', frameon=True) #Muestra el label de cada plt.plot()
        plt.show()
    
    def plotearG(self, **kwargs):
        '''
        kwargs  
            clave: 'label'  element: lo de la leyenda
        '''
        S = 15
        label= self.leyenda
        l = False
        if 'label' in kwargs and self.leyenda ==None:
            label = kwargs['label']
            l = True
        if 'color' in kwargs:
            plt.plot(self.lambdas, self.transmitanciaG, '-', markersize=S, 
                 color=kwargs['color'], label = r'{}'.format(label))
        else:
            plt.plot(self.lambdas, self.transmitanciaG, '-', markersize=S, 
                     color=self.color, label = r'{}'.format(label))
        plt.xlabel(r'$\lambda$ / nm', size=15)
        plt.ylabel(r'$T$ / %', size=15)
        #plt.ylim(0, 12)
        plt.xlim(602, 880)
        
        if self.leyenda != None or l==True:
            plt.legend(loc= 'best', frameon=True) #Muestra el label de cada plt.plot()
        plt.show()
        
    def maximos(self, **kwargs):
        '''
        kwargs 
            clave: 'lim'  elemnt: tupla con los limites o cotas del maximo
                    sino devuelve todos los maximos
            clave:  'G' : bool = si es False hace lo de maximos y minimos sin suavizar
                        si pone True o no lo defines lo hace suavizando
        '''
        if 'G' in kwargs and kwargs['G'] == False:
            maxs = argrelextrema(self.transmitancia, np.greater)
        else:
            maxs = argrelextrema(self.transmitanciaG, np.greater)
        
        l = np.array(self.lambdas)
        maxis=l[maxs]
        if 'lim' in kwargs:
            pequeno, grande = kwargs['lim']
            for M in maxis:
                if M>pequeno and M<grande:
                    return M
            return 'No se ha encontrado maximos'
        else:
            return maxis
        
    def minimos(self, **kwargs):
        '''
        kwargs 
            clave: 'lim'  elemento: tupla con los limites o cotas del minimo
            sino devuelve todos los minimos
            clave:  'G' : elemento = bool si es False hace lo de maximos y minimos sin suavizar
                        si pone True o no lo defines lo hace suavizando
        
        '''
        if 'G' in kwargs and kwargs['G'] == False:
            mins = argrelextrema(self.transmitancia, np.less)
        else:
            mins = argrelextrema(self.transmitanciaG, np.less)
        l = np.array(self.lambdas)
        minis =l[mins]
        if 'lim' in kwargs:
            pequeno, grande = kwargs['lim']
            for m in minis:
                if m>pequeno and m<grande:
                    return m
            return 'No se ha encontrado minimo'
        else:
            return minis
    def intensidad(self, **kwargs):
        
        if 'lim' in kwargs:
            intensidad = sum(self.transmitancia)
            return intensidad
        else:
            intensidad = 5
            return intensidad



