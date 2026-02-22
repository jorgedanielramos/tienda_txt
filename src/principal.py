import os
import pandas as pd
from pathlib import Path
from src import librerias_propias as lbp
from src import clientes_df as cli
from src import productos_df as pro
from src import ventas_df as ven
from src import reportes_df as rep


# Declaracion de rutas base
BASE_DIR = Path(__file__).resolve().parents[1]
BD_DIR = BASE_DIR / "dataframes"
CLIENTES_PATH = BD_DIR / "Clientes.csv"
PRODUCTOS_PATH = BD_DIR / "Productos.csv"
VENTAS_PATH = BD_DIR / "Ventas.csv"

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
        opcion=lbp.seleccionar_opcion("Menú principal",opciones)
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