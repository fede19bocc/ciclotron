# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 19:03:20 2022

@author: Fede
"""
# librerias
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#%% Datos desde txt base de datos

datos = pd.read_csv("prueba_c11.txt", sep = ";", encoding = 'utf-16')
# Renombro las columnas y cambio Tiempo a datetime
datos.rename(columns = {'LOCATION': 'Ubicacion', 'READING': 'Dosis', 'SYSTEM_REPORT_TIME': 'Tiempo'}, inplace = True )
datos['Tiempo'] = pd.to_datetime(datos['Tiempo'])
# uso ubicacionb y tiempo como indice del dataframe
datos.set_index(['Ubicacion','Tiempo'], inplace = True)

#%% usar esto de modelo para generar las funciones para graficar
# Separo por monitor y ordeno por fecha
ciclo1 = datos.loc['Ciclotron 1']
ciclo2 = datos.loc['Ciclotron 2']
celdas = datos.loc['Celdas']

ciclo1.sort_index(inplace=True)
ciclo2.sort_index(inplace=True)
celdas.sort_index(inplace=True)

# Creo subplots del rango a visualizar y ploteo
fecha_hora = '2023-12-19 10:25'
fecha_hora_fin = '2023-12-19 10:43:37'
ax1 = ciclo1.loc[fecha_hora : fecha_hora_fin]['Dosis'].plot(label = 'Ciclotron 1')
ax2 = ciclo2.loc[fecha_hora : fecha_hora_fin]['Dosis'].plot(label = 'Ciclotron 2')
ax3 = celdas.loc[fecha_hora : fecha_hora_fin]['Dosis'].plot(label = 'Celdas')

# hace ticks cada minuto:
ax1.xaxis.set_major_locator(mdates.MinuteLocator())
# Get only the minute to show in the x-axis:
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation='vertical')
ax1.set_ylabel('Tasa dosis [µSv/h]')
ax1.legend()

#%% Funciones

def procesar_datos_txt(archivo, separador=";", encoder='utf-16'):
    '''
    Parameters
    ----------
    archivo : .txt
        base de datos de los monitores ambientales
    separador : TYPE
        por defecto es ;.

    Returns
    -------
    datos : dataframe
        
    '''
    datos = pd.read_csv(archivo, sep = separador, encoding = encoder, low_memory=False)
    datos.rename(columns = {'LOCATION': 'Ubicacion', 'READING': 'Dosis', 'SYSTEM_REPORT_TIME': 'Tiempo'}, inplace = True )
    datos['Dosis'] = pd.to_numeric(datos['Dosis'])
    datos['Tiempo'] = pd.to_datetime(datos['Tiempo'])
    # uso ubicacion y tiempo como indice del dataframe
    datos.set_index(['Ubicacion','Tiempo'], inplace = True)
    return datos

def agrupar_monitores(datos):
    '''
    Procesa dataframe y separa por monitor y ordena por fecha

    Parameters
    ----------
    datos : pandas

    Returns
    -------
    Lista con tuplas pd de cada monitor y str con su nombre
    [Ciclo1, Ciclo2, Celdas, Control, Prod, Desa, QC, Despacho].

    '''
    #dict monitores con Nonew
    monitores = {'Ciclotron 1': None,'Ciclotron 2': None,'Celdas': None,'Control': None,'Produccion': None,
                 'Desarrollo': None,'Calidad': None,'Despacho': None}
    
    #hacer un loop con ese listado y que genere las variables con cada df
    
    #meter ese loop en un try except para cuando falte un monitor
    for monitor, lectura in monitores.items():
        try:
            monitores[monitor] = datos.loc[monitor]
    
        except KeyError as k:
            print(k)
    
    for m, l in monitores.items():
        if type(l) == type(None):
            continue
        else:
            l.sort_index(inplace=True)
    
    return monitores

def graficar_monitores(monitores, monitores_elegidos, fecha_i, fecha_f, tiempo_i, tiempo_f, formato=None):
    '''
    Grafica una lista de monitores, segun un agrupacion de un delta tiempo

    Parameters
    ----------
    monitores : listado con todos los monitores
    monitores_elegidos : lista de monitores para graficar
    fecha : str
    inicio : str hh:mm
    fin : str hh:mm
    formato: str hora, minuto
    '''
    fecha_hora_inicio = fecha_i + ' ' + tiempo_i
    fecha_hora_fin = fecha_f + ' ' + tiempo_f
    subplots = {}   
    for i, m in enumerate(monitores_elegidos):
        subplots = {'ax'+str(i) : monitores[m].loc[fecha_hora_inicio: fecha_hora_fin]['Dosis'].plot(label = list(monitores.keys())[i])}
    for ax, sub in subplots.items():
        sub
    
    
    if formato is None:
        pass
    elif formato == 'hora':
        # hace ticks cada minuto:
        sub.xaxis.set_major_locator(mdates.HourLocator())
        # Get only the minute to show in the x-axis:
        sub.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    elif formato == 'minuto':
        # hace ticks cada minuto:
        sub.xaxis.set_major_locator(mdates.MinuteLocator())
        # Get only the minute to show in the x-axis:
        sub.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation='vertical')
    sub.set_ylabel('Tasa dosis [µSv/h]')
    sub.legend()

    plt.show()
    
# m=agrupar_monitores(d)
# d=procesar_datos_txt('DATOS_AREA_4T2019_mod.txt')
# monitores = agrupar_monitores(d)
# graficar_monitores(monitores, ['Ciclotron 1', 'Ciclotron 2'], '2023-12-19', '2023-12-19', '10:25', '10:44', 'minuto')

# #%% Funciones para agrupar por fecha y hora 

# # No usar quedaron desactualizadas con lo que quiero hacer

# def agrupar_fecha_hora (datos, fechaI, fechaF = None, horaI = None, horaF = None):
#     ''' 
#     Parameters
#     ----------
#     datos : Ingresar DataFrame
#     fechaI : string
#         formato AA-MM-DD
#     fechaF : string, optional
#         formato AA-MM-DD. The default is None.
#     horaI : string , optional
#         formato HH:MM:SS. The default is None.
#     horaF : string, optional
#         formato HH:MM:SS. The default is None.

#     Returns
#     -------
#     monitores : groupby dataframe
#         devuelve los datos agrupados por monitor del rango de fechas seleccionadas.

#     '''
#     tiempo = generar_delta_tiempo(fechaI, fechaF, horaI, horaF)
#     if type(tiempo) is str:
#         monitores = datos.loc[tiempo].groupby('Ubicacion')
#     else:
#         monitores = datos.loc[tiempo[0] : tiempo[1]].groupby('Ubicacion')
#     return monitores

# def generar_delta_tiempo(fechaI, fechaF, horaI, horaF):
#     fin = fechaF is None or horaI is None or horaF is None
#     if fin:
#         return (str(fechaI))
#     else:
#         if horaI is None:
#             horaI = ""
#         else:
#             horaI = " " + str(horaI)
#         t_inicio = str(fechaI) + horaI
        
#         if horaF is None:
#             horaF = ""
#         else:
#             horaF = " " + str(horaF)
#         t_fin = str(fechaF) + horaF
            
#         return t_inicio, t_fin
    
    
# # #%% agrupo por ubicacion para despues plotear segun monitor en una fecha
# # ylabel = 'Tasa dosis [µSv/h]'
# # monitores = datos.loc['2022-07-06 04:15:00' : '2022-07-06 06:30:00'].groupby('Ubicacion')

# # #%% grafico por ubicacion un dia
# # datos.loc['2022-07-22'].groupby('Ubicacion')['Dosis'].plot( legend = True)
# # #%% grafico por ubicacion en un rango de dias y horas
# # datos.loc['2022-07-06 04:15:00' : '2022-07-06 06:30:00'].groupby(['Ubicacion'])['Dosis'].plot(ylabel = ylabel , legend = True)

# # #%% grafico por grupo (tengo que generar una variable con el agrupamiento y el delta tiempo elegido)
# # # hacer un for para graficar lo que quiero
# # ax1 = monitores.get_group('Ciclotron 1').loc['2022-07-06 04:15:00' : '2022-07-06 06:30:00']['Dosis'].plot(label = 'Ciclotron 1')
# # ax2 = monitores.get_group('Ciclotron 2').loc['2022-07-06 04:15:00' : '2022-07-06 06:30:00']['Dosis'].plot(label = 'Ciclotron 2')
# # ax1.legend()
# # ax1.set_ylabel('Tasa dosis [µSv/h]')
# # plt.show()