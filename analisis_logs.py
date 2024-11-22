# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 09:11:07 2022

@author: tecciclotron
"""
'''
Discontinuado, lector_logs y analisis_logs se unificaron en monitores.py 
'''
# modulos
import csv
import matplotlib.pyplot as plt
import sys
import pandas as pd
import datetime

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
        datosProduccion = procesarLinea1Produccion(linea1)
        
        next(logs) # linea lugar Fleni
        next(logs) #vacia
        
        #dataframe
        tipos = [str, int, int] + [float]*22 + [int] # defino el tipo de dato
        encabezados = next(logs) 
        for lineas in logs:
            convertir = [funcion(valor) for funcion, valor in zip(tipos, lineas)]
            datos_lineas.append(convertir) 
    
    return datosProduccion, pd.DataFrame(datos_lineas, columns=encabezados)

def varios_logs(desde, hasta):
    '''Devuelve un dataframe de los logs solicitados 
    Ingresar solo el número de log'''
    logs =[]
    direccion ="logs-pruebas\\"
    encabezados = ['Posicion', 'Blanco', 'Batch', 'Fecha', 'logs']
    for  i in range(desde, hasta+1):
        try:
            num_log = direccion + str(i) + ".log"
            logs.append(creaListaDatosProduccion(datos_log(num_log)))
        except FileNotFoundError:
            pass
        
    return pd.DataFrame(logs, columns=encabezados)

def procesarLinea1Produccion(linea1):
    ''' Devuelve una lista con el numero de blanco y posicion, num de batch y 
    fecha '''
    blanco = linea1[0].split(' ')
    blanco.pop(0)
    posicion = int(blanco[0].strip('()'))
    blanco = blanco[1]
    batch = linea1[1].split(' ')
    batch = int(batch[2])
    fecha = linea1[2].split(' ')
    if len(fecha) > 2:
        fecha[1] = fecha[1] + "0" + fecha[2].strip(' ')
    fecha = datetime.datetime.strptime(fecha[1],"%Y-%m-%d")
    fecha = datetime.datetime.date(fecha) 
   
    return  [posicion, blanco, batch, fecha]

def creaListaDatosProduccion(log):
    ''' Dado un log en formato tupla con los datos de produccion y DF del log
    lo unifica en una sola lista que contiene los datos del encabezado'''
    
    log = [log[0][0], log[0][1], log[0][2], log[0][3], log[1]]
    
    return log
#%%
nombreCol = ['Time', 'Arc-I', 'Arc-V', 'Gas flow', 'Dee-1-kV', 'Dee-2-kV', 'Magnet-I', 
 'Foil-I', 'Coll-l-I', 'Target-I', 'Coll-r-I', 'Vacuum-P', 'Target-P', 
 'Delta Dee-kV', 'Phase load', 'Dee ref-V', 'Probe-I', 'He cool-P', 
 'Flap1-pos', 'Flap2-pos', 'Step pos', 'Extr pos', 'Balance', 'RF fwd-W', 
 'RF refl-W', 'Foil No']

ejeY = ['[seg]', '[mA]', '[V]', '[sccm]', '[kV]', '[kV]', '[A]', '[µA]',
        '[µA]', '[µA]', '[µA]', '[mbar]', '[psi]', '[kV]', '[°]', '[kV]',
        '[µA]', '[psi]', '[%]', '[%]', '[%]', '[%]', '[%]', '[W]', '[W]', '']

nombreCol = pd.DataFrame(nombreCol, columns=['Nombre'])
ejeY = pd.DataFrame(ejeY, columns=['unidades'])
datosGraficos = [nombreCol, ejeY]
datosGraficos = pd.concat(datosGraficos, 1)
#%%
def graficoParametro(index, batch, producciones):
    datosBatch = producciones[producciones['Batch']==batch]
    dfDatosBatch = datosBatch['logs'][datosBatch.index[0]] #selecciono el df dentro de la lista
    x = [3/60 * i for i in range(len(dfDatosBatch))] #convierto eje x a minutos
    plt.plot(x, dfDatosBatch[datosGraficos['Nombre'][index]], 
             label = datosGraficos['Nombre'][index])
    plt.ylabel(datosGraficos['unidades'][index])
    plt.xlabel('[min]')
    

