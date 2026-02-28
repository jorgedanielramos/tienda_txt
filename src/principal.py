import os

from pathlib import Path

import src.lib.librerias_propias as lbp
import src.dataframes.clientes_df as cli
from src.ui import interfaz as ui
import src.dataframes.productos_df as pro
import src.dataframes.ventas_df as ven
import src.dataframes.reportes_df as rep
from config import BASE_DIR, BD_DIR, CLIENTES_PATH, PRODUCTOS_PATH, FACTURAS_PATH, DETALLES_PATH

def main():
    lbp.verificar_archivos()
    while True:
        os.system("cls")
        print("Sistema de control de ventas")
        opciones=[
              "Gestión de clientes...1",
              "Gestión de productos..2",
              "Efectuar Ventas ......3",
              "Reportes..............4",
              "Salir.................5"]
        opcion=ui.seleccionar_opcion("Menú principal",opciones)
        match opcion:
            case "1":
                cli.main()
            case "2":
                pro.main()   
            case "3":
                ven.main()
            case "4":
                rep.main()
            case "5":
                break
            
if __name__=="__main__":    
    main()