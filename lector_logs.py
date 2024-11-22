# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 19:58:42 2021

@author: Fede
"""

'''
Discontinuado, lector_logs y analisis_logs se unificaron en monitores.py 
'''

# modulos
import csv
import matplotlib.pyplot as plt
import sys
import pandas as pd

#%%
def datos_log(archivo):
    '''Recorre un batch y devuelve los datos del archivo en un dataframe'''
    datos_lineas = []
    with open(archivo, 'rt', encoding='utf-8') as logs:
        logs = csv.reader(logs, delimiter='\t') # separacion por tabulacion
        #contiene el nro de blanco, no batch y la fecha
        linea1= next(logs)
        while '' in linea1:
            linea1.remove('')
        next(logs) # linea lugar Fleni
        next(logs) #vacia
        tipos = [str, int, int] + [float]*22 + [int] # defino el tipo de dato
        encabezados = next(logs) 
        for lineas in logs:
            convertir = [funcion(valor) for funcion, valor in zip(tipos, lineas)]
            datos_lineas.append(convertir) 
    
    return pd.DataFrame(datos_lineas, columns=encabezados)

def ver_log(num_log):
    ''' Dado el numero del log, imprime graficos de IS, Colimadores, target y 
    foil, Presion de vacio y presion del target.
    Precondicion: el num_log debe ser un entero'''
    a = datos_log(str(num_log)+'.log')
    x = [3/60 * i for i in range(len(a))] #convierto eje x a minutos
    # genero la base para los 6 plots
    fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2, 3, 
                                    num = "Batch "+str(num_log), sharex=True)
    plt.xlim(0, (len(x)-1)*3/60)
    for i in [ax4,ax5,ax6]:
        i.set_xlabel("min")
    # Fuente de iones    
    ax1.plot(x, a['Arc-I'])
    ax1.set_title('Fuente Iones')
    ax1.set_ylabel("mA")
    # target y colimadores
    ax2.plot(x,a['Foil-I'], label='Foil-I')
    ax2.plot(x,a['Coll-l-I'], label='Coll-l-I')
    ax2.plot(x,a['Target-I'], label='Target-I')
    ax2.plot(x,a['Coll-r-I'], label='Coll-r-I')
    ax2.legend()
    ax2.set_title('Target y colimadores')
    ax2.set_ylabel("µA")
    # vacio
    ax3.plot(x,a['Vacuum-P'])
    ax3.set_title('Vacuum-P')
    ax3.set_yscale('log')
    # presion de target
    ax4.plot(x,a['Target-P'])
    ax4.set_title('Target-P')
    ax4.set_ylabel("psi")
    # perdida de corriente
    ax5.plot(x,(a['Foil-I']-a['Coll-l-I']-a['Target-I']-a['Coll-r-I']))
    ax5.set_title('Perdida de corriente')
    ax5.set_ylabel("µA")
    # dee
    ax6.plot(x,a['Dee-1-kV'], label='Dee-1')
    ax6.plot(x,a['Dee-2-kV'], label='Dee-2')
    ax6.set_ylabel("kV")
    ax6.legend()
    ax6.set_title('Dee')
    plt.show(block = False)

def varios_logs(desde, hasta):
    '''Genera varios plot especificando un rango de batchs
    desde y hasta tienen que ser números enteros'''
    #figsize = (12.8, 9.6)
    for i in range(hasta-desde+1):
        num_log = desde + i
        ver_log(num_log)
        
        
#%%
#Funcion principal:
def main(parametros):
    if len(parametros) < 2:
        print(f'Uso adecuado: {parametros[0]} ' 'número del log')
    else:
        ver_log(parametros[1])
    
if __name__ == '__main__':
    main(sys.argv)
