# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 08:48:52 2022

@author: tecciclotron
Procesa todos los logs de la carpeta donde esta el archivo y genera un .csv con 
fecha, hora y cuentas acumuladas

v1.1 Funcion extraer datos modificada. Toma la ROI del primer archivo y la usa en acumuladaROI.
     funcion acumuladaROI mnodificacda. Agrego variable ROI y modifico error en el calculo. 
     Variable acumulada no partia de cero y variable ROI_inf sumaba siempre del canal 1.
"""
import os
import datetime
import pandas as pd

# test="2022-11-28_ 8Hs02min48seg"

def genero_CSV(path):
    '''Creo el csv para exportar el df con los datos de la chimenea de todo el
    trimestre'''
    datos = procesar_carpetas(path)
    datos.to_csv(os.path.join(path, 'logs.csv'))

def procesar_carpetas(wdir=None):
    if wdir==None:
        wdir = os.getcwd()
    carpetas = os.listdir()
    datos=[]
    for carpeta in carpetas:
        datos.append(procesar_Spe(carpeta, wdir))
        
    return pd.DataFrame(datos, columns=['Fecha', 'Hora', 'acumulada'])

def procesar_Spe(carpeta, directorio_trabajo):
    path = os.path.join(directorio_trabajo, carpeta) 
    if os.path.isdir(path): # si es una archivo lo evito
        os.chdir(path) #cambio el directorio de trabajo
        lista = leer_carpeta()
        return extraer_datos(lista)

def leer_spe(archivo):
    '''
    Devuelve el texto adentro del archivo
    '''
    with open(archivo, "r") as f:
        return f.read()


def leer_carpeta():
    '''
    lee todos los archivos de la carpeta actual
    y genera una lista con los textos
    '''
    lista = []
    
    for file in os.listdir():
        if file.endswith(".Spe"):
            lista.append(leer_spe(file))
            
    return lista

def extraer_datos(lista):
    '''
    Dada una lista con los archivos de lectura de chimenea devuelve fecha, 
    hora y la suma acumulada de la ROI.
    '''
    base = []
    for l in lista:
        aux = l.split("\n")   
        aux = aux[12:1036]
        for i in range(len(aux)):
            aux[i] = int(aux[i].strip(" "))
        base.append(aux)
        
    #tomo la fecha y hora del primero archivo *000.Spe
    f_h_aux = lista[0].split("\n")[7]
    fecha_hora = datetime.datetime.strptime(f_h_aux, "%m/%d/%Y %H:%M:%S")
    
    #tomo la roi
    ROI = lista[0].split("\n")[1038]
    ROI = ROI.split()
    #si el dataframe no se exporta bien en cvs lo convierto a texto la fecha 
    #hora
    return (fecha_hora.date(), #.isoformat(), -> lo convierte en texto
            fecha_hora.time(),#.isoformat(),   -> lo convierte en texto
            acumulada_ROI(base, ROI))

def acumulada_ROI(base, ROI):
    '''
    Dada una lista con los valores por canal de la chimenea, devuelve la suma
    acumulada en la ROI determinada.
    '''
    
    ROI_inf = int(ROI[0]) #Nro de canal no energia!!
    ROI_sup = int(ROI[1])
    acumulada = 0
    for b in base:
        acumulada += sum(b[ROI_inf-1:ROI_sup])
    return acumulada

#%%
#Funcion principal:
if __name__ == '__main__':
    path = os.getcwd() #obtengo path carpeta actual
    print("procesando... no cerrar la ventana!!!!")
    genero_CSV(path)   # crea un archivo csv logs.csv