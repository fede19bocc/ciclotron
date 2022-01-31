# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 09:11:07 2022

@author: tecciclotron
"""

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
        next(logs) # linea lugar Fleni
        next(logs) #vacia
        tipos = [str, int, int] + [float]*22 + [int] # defino el tipo de dato
        encabezados = next(logs) 
        for lineas in logs:
            convertir = [funcion(valor) for funcion, valor in zip(tipos, lineas)]
            datos_lineas.append(convertir) 
    
    return linea1, pd.DataFrame(datos_lineas, columns=encabezados)

def varios_logs(desde, hasta):
    '''Devuelve una lista de dataframes de los logs solicitados
    Ingresar solo el número de log'''
    logs =[]
    direccion ="logs-pruebas\\"
    for  i in range(desde, hasta+1):
        num_log = direccion + str(i) + ".log"
        logs.append(datos_log(num_log))
        
    return logs

def procesarLinea1Produccion(linea1):
    blanco = linea1[0].split(' ')
    blanco.pop(0)
    blanco[0] = int(blanco[0].strip('()'))
    batch = linea1[1].split(' ')
    batch = int(batch[2])
    fecha = linea1[2].split(' ')
    fecha = datetime.datetime.strptime(fecha[1],"%Y-%m-%d")
    fecha = datetime.datetime.date(fecha)
    
    produccion=[blanco, batch, fecha]
    return produccion
    

