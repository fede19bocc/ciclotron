# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 10:25:56 2022

@author: Fede
"""
import csv
import os
import datetime
import pandas as pd

#%% Abro el archivo y cambio los nombres de los monitores Ciclotron 1 y 2
 
# asi monitores.py puede procesar los separadores sin problemas

def modificar_txt(nombre_archivo, encoding="utf-8", newline=''):
    with open(nombre_archivo,encoding = encoding) as f:
        lineas = csv.reader(f)
        nombre_archivo_mod = nombre_archivo.split('.')
        nombre_archivo_mod.pop()
        with open(nombre_archivo_mod[0] + '_mod.txt', 'w', newline='' ,encoding = "utf-16") as mod:
            for linea in lineas:
                if len(linea)==1:
                    linea[0] = linea[0].replace('Ciclotron 1', 'Ciclotron_1')
                    linea[0] = linea[0].replace('Ciclotron 2', 'Ciclotron_2')
                    linea = linea[0].split(' ')
                    if len(linea) == 4:
                        linea[2] = linea[2] + ' ' + linea[3]
                        linea.pop()
                    linea[0] = linea[0].replace('Ciclotron_1', 'Ciclotron 1')
                    linea[0] = linea[0].replace('Ciclotron_2', 'Ciclotron 2')
                    writer = csv.writer(mod, delimiter = ';')
                    writer.writerow(linea)

def unir_monitores_csv(path=None):
    if path is None:
        path = os.getcwd()
    if not os.path.exists(path):
        raise FileNotFoundError(f"La ruta especificada no existe: {path}")
    datos = procesar_csv(path)
    output_file = os.path.join(path, 'logs.csv')
    if datos.empty:
        print("No se encontraron datos para procesar.")
        return
    datos.to_csv(output_file, index=False)
    print(f"Archivo guardado en: {output_file}")

def procesar_csv(path):
    if os.path.isdir(path):  # Si es una carpeta
        return leer_carpeta(path)
    return pd.DataFrame()

def leer_carpeta(carpeta_path):
    '''
    Lee todos los archivos CSV de la carpeta especificada y devuelve sus contenidos como un único DataFrame.
    '''
    datos = []
    for file in os.listdir(carpeta_path):
        if file.endswith(".csv"):
            archivo_path = os.path.join(carpeta_path, file)
            print(f"Leyendo archivo: {archivo_path}")
            contenido = leer_spe(archivo_path)
            datos.append(contenido)
    if datos:
        return pd.concat(datos, ignore_index=True)
    return pd.DataFrame()

def leer_spe(archivo):
    '''
    Devuelve el contenido del archivo CSV como un DataFrame.
    '''
    try:
        return pd.read_csv(archivo)
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")
        return pd.DataFrame()

#%%
unir_monitores_csv(r"\Users\federico.boccazzi\Documents\Python Scripts\10-Octubre")