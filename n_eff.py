# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 13:34:48 2022

@author: USUARIO
"""

import numpy as np

def volumenE(R, d, pinhole, s, N):
    """Calcula el volumen del cilindro, 
    el medio contenido en el y 
    la interseccion con la esfea
    
    Args:
        R: float = radio de la esfera
        d: float = distancia esfera-chip
        pinholes: float = diametro del circlo iluminado
        s: float = distancia del centro xy de la esfera al centro del circulo iluminado
        N: int = particion del plano xy para el metodo numerico
    Returns:
        V_t, V_e, V_m: tuple = volumen cilindro total, 
                               volumen intersecioncon esfera,
                               volumen del medio e el cilindro
        
    """
    
    pinhole = pinhole/2 #Para calcular usamos el radio
    g = 0.2             #penetracion plasmon
    V_t =pinhole**2 * np.pi *g
    def e(r):
        if r<R:
            e=R-np.sqrt(R**2-r**2)+d
            return e
        else:
            return 999999999
        
    def dist(xx, yy):
        r = np.sqrt(xx**2+yy**2) 
        r_pin = np.sqrt((xx-s)**2+yy**2) 
        if r_pin>pinhole:
            return 0
        elif r>R or r==R:
            return 0
        elif g<e(r) and r<R:
            return 0
        else:
            dist = g-e(r)
            return dist 
    
    def Simpson2D(f,a,b,c,d):
        mx = (a+b)/2
        my = (c+d)/2
        S = f(a,c) + f(a,d) + f(b,c) + f(b,d)
        S = S + 4*(f(a,my)+f(b,my)+f(mx,c)+f(mx,d))
        S = S + 16*f(mx,my)
        return S*(d-c)*(b-a)/36
    
    def SimpsonComp2D(f,a,b,c,d,k):
        pasox = (b-a)/k
        pasoy = (d-c)/k
        S = 0 
        for i in range(0,k):
            for j in range(0, k):
                S = S + Simpson2D(f,a + i*pasox, a + (i+1)*pasox, c + j*pasoy, c + (j+1)*pasoy)
        return(S)
        
    V_e = SimpsonComp2D(dist, -pinhole+s, pinhole+s, -pinhole, pinhole, N)
    V_m =V_t-V_e
    return V_t, V_e, V_m
    

def n_eff(pinholes, n_m, n_esf, R, d, s, N):
    """Calcula el indice de refracción efectivo llamando a la funcion volumenE()
    Args:
        n_m: float = indice de refraccion del medio
        n_esf: float = indice de refracion de la esfera
        R: float = radio de la esfera
        d: float = separcion esfera-chip
        s: float = distancia del centro xy de la esfera al centro del circulo iluminado
        N: int = particion del plano xy para el metodo numerico
    Returns:
        n_eff: float = indice de refraccion efectivo sobre el chip
    """
    V_t, V_e, V_m = volumenE(R, d, pinholes, s, N)
    n_eff = n_esf *V_e/V_t + n_m *V_m /V_t
    return n_eff
        
    
def desplazamiento(n_ef, n_m, S):
    """Calcula el desplazamiento del espectro a partir del indice 
    de refraccion efectivo, el del medio y la sensibilidad del chip
    
    Args:
        n_ef: float = indide de refraccion efectivo sobre el chip
        n_m: float = indice de refraccion del medio sobre el chip
        S: float = sensibilidad optica del chip
    """
    dl = (n_ef-n_m)*S
    return dl

if __name__ == "__main__":
    
    '''
    ###Unicos parametros del problema
    '''
    #Toda distancia en micras
    pinhole = 20     #DIAMETRO del pinhole, micras
    R = 10           #Radio de la esfera, micras
    d = 0            #Distancia esfera plano, micras
    s = 2.5          #Distancia esfera zona iluminada en el plano xy
    N = 40           #Particion de la integracion numérica
    
    n_agua = 1.3323054
    n_vidrio = 1.51
    n_metil = 1.48
    n_aire=1
    sens = 311       #Sensibilidad del chip (nm/RIU)
    '''
    ###########
    '''
    
    n = n_eff(pinhole, n_aire, n_vidrio, R, d, s, N)
    despl = desplazamiento(n, n_aire, sens)
    print('El desplazamiento del espectro es: {} nm'.format(round(despl, 3)))











#%%
