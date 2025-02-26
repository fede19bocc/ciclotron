import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from lector_logs import datos_log

def ver_log_real_time(num_log):
    """
    Grafica en tiempo real los parámetros del log especificado.
    Se actualiza cada 3 segundos para reflejar nuevos datos.
    """
    archivo_log = f"{num_log}.log"
    
    if not os.path.exists(archivo_log):
        print(f"El archivo {archivo_log} no existe.")
        return
    
    plt.ion()  # Modo interactivo
    fig, axes = plt.subplots(2, 3, figsize=(12, 8), num=f"Batch {num_log}")
    ax1, ax2, ax3 = axes[0]
    ax4, ax5, ax6 = axes[1]
    
    while True:
        try:
            df = datos_log(archivo_log)
            x = [3/60 * i for i in range(len(df))]  # Convierte eje x a minutos
            
            ax1.clear()
            ax1.plot(x, df['Arc-I'])
            ax1.set_title('Fuente Iones')
            ax1.set_ylabel("mA")
            
            ax2.clear()
            ax2.plot(x, df['Foil-I'], label='Foil-I')
            ax2.plot(x, df['Coll-l-I'], label='Coll-l-I')
            ax2.plot(x, df['Target-I'], label='Target-I')
            ax2.plot(x, df['Coll-r-I'], label='Coll-r-I')
            ax2.legend()
            ax2.set_title('Target y colimadores')
            ax2.set_ylabel("µA")
            
            ax3.clear()
            ax3.plot(x, df['Vacuum-P'])
            ax3.set_title('Vacuum-P')
            ax3.set_yscale('log')
            
            ax4.clear()
            ax4.plot(x, df['Target-P'])
            ax4.set_title('Target-P')
            ax4.set_ylabel("psi")
            
            ax5.clear()
            ax5.plot(x, (df['Foil-I'] - df['Coll-l-I'] - df['Target-I'] - df['Coll-r-I']))
            ax5.set_title('Perdida de corriente')
            ax5.set_ylabel("µA")
            
            ax6.clear()
            ax6.plot(x, df['Dee-1-kV'], label='Dee-1')
            ax6.plot(x, df['Dee-2-kV'], label='Dee-2')
            ax6.legend()
            ax6.set_title('Dee')
            ax6.set_ylabel("kV")
            
            plt.pause(3)  # Espera 3 segundos antes de actualizar
        except KeyboardInterrupt:
            print("Detenido por el usuario.")
            break
    
    plt.ioff()
    plt.show()
    
# Llamar a ver_log_real_time con el número de batch deseado
# ver_log_real_time(123)