# -*- coding: utf-16 -*-
"""
Created on Wed Aug 10 10:25:56 2022

@author: Fede
"""
import csv
#%% Abro el archivo y cambio los nombres de los monitores Ciclotron 1 y 2
 
# asi monitores.py puede procesar los separadores sin problemas

def modificar_txt(nombre_archivo, encoding="utf-16", newline=''):
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
  
#%%  quiero tratar de cambiar los separadores a ;  
# with open("monitores_ambientales_2021\\2T2021_mod.csv", 'rt', encoding = "UTF-16") as f:
#     lineas = csv.reader(f, delimiter = ' ')
#     with open("monitores_ambientales_2021\\2T2021_mod.csv", 'w',encoding = "UTF-16") as mod:
#         for linea in lineas:
#             writer = csv.writer(mod, delimiter = ';')
#             writer.writerow(linea)

# i = 10
# linea_a = []
# for a in archivo:
#     if i > 0:
#         linea_a.append(a)
#         print(a)
#         i-=1
