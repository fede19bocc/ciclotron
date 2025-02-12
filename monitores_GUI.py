import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def procesar_datos_txt(archivo, separador=";", encoder='utf-16'):
    datos = pd.read_csv(archivo, sep=separador, encoding=encoder, low_memory=False)
    datos.rename(columns={'LOCATION': 'Ubicacion', 'READING': 'Dosis', 'SYSTEM_REPORT_TIME': 'Tiempo'}, inplace=True)
    datos['Dosis'] = pd.to_numeric(datos['Dosis'], errors='coerce')
    datos['Tiempo'] = pd.to_datetime(datos['Tiempo'], errors='coerce')
    datos.dropna(subset=['Dosis', 'Tiempo'], inplace=True)
    datos.set_index(['Ubicacion', 'Tiempo'], inplace=True)
    return datos

def agrupar_monitores(datos):
    monitores = {k: None for k in ['Ciclotron 1', 'Ciclotron 2', 'Celdas', 'Control', 'Produccion', 'Desarrollo', 'Calidad', 'Despacho']}
    for monitor in monitores.keys():
        try:
            monitores[monitor] = datos.loc[monitor]
        except KeyError:
            pass
    return monitores

def graficar_monitores(monitores, monitores_elegidos, fecha, tiempo_i, tiempo_f, intervalo):
    fecha_hora_inicio = datetime.strptime(fecha + ' ' + tiempo_i, "%Y-%m-%d %H:%M")
    fecha_hora_fin = datetime.strptime(fecha + ' ' + tiempo_f, "%Y-%m-%d %H:%M")
    
    fig, ax = plt.subplots()
    for m in monitores_elegidos:
        if m in monitores and monitores[m] is not None:
            datos_filtrados = monitores[m].loc[fecha_hora_inicio:fecha_hora_fin]
            ax.plot(datos_filtrados.index, datos_filtrados['Dosis'], label=m)
    
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=intervalo))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    ax.set_ylabel('Tasa dosis [µSv/h]')
    ax.legend()
    plt.show()

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Archivos RPT", "*.rpt"), ("Todos los archivos", "*.*")])
    if archivo:
        datos = procesar_datos_txt(archivo)
        monitores = agrupar_monitores(datos)
        ventana_principal(monitores)

def ventana_principal(monitores):
    def graficar():
        monitores_elegidos = [lb_monitores.get(i) for i in lb_monitores.curselection()]
        fecha = entrada_fecha.get()
        tiempo_i = entrada_hora_ini.get()
        tiempo_f = entrada_hora_fin.get()
        intervalo = int(entrada_intervalo.get())
        graficar_monitores(monitores, monitores_elegidos, fecha, tiempo_i, tiempo_f, intervalo)
    
    ventana = tk.Toplevel(root)
    ventana.title("Parámetros del gráfico")
    
    tk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack()
    entrada_fecha = tk.Entry(ventana)
    entrada_fecha.pack()
    
    tk.Label(ventana, text="Hora inicio (HH:MM):").pack()
    entrada_hora_ini = tk.Entry(ventana)
    entrada_hora_ini.pack()
    
    tk.Label(ventana, text="Hora fin (HH:MM):").pack()
    entrada_hora_fin = tk.Entry(ventana)
    entrada_hora_fin.pack()
    
    tk.Label(ventana, text="Intervalo en minutos:").pack()
    entrada_intervalo = tk.Entry(ventana)
    entrada_intervalo.pack()
    
    tk.Label(ventana, text="Selecciona Monitores:").pack()
    lb_monitores = tk.Listbox(ventana, selectmode=tk.MULTIPLE)
    for monitor in monitores.keys():
        lb_monitores.insert(tk.END, monitor)
    lb_monitores.pack()
    
    tk.Button(ventana, text="Graficar", command=graficar).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Seleccionar archivo")
    
    btn_cargar = tk.Button(root, text="Cargar Archivo", command=seleccionar_archivo)
    btn_cargar.pack()
    
    root.mainloop()
