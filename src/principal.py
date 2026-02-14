import os
from pathlib import Path
from src import librerias_propias as lbp
from src import clientes as cli
from src import productos as pro


# Declaracion de rutas base
BASE_DIR = Path(__file__).resolve().parents[1]
BD_DIR = BASE_DIR / "BD"
CLIENTES_PATH = BD_DIR / "Clientes.txt"
PRODUCTOS_PATH = BD_DIR / "Productos.txt"
VENTAS_PATH = BD_DIR / "Ventas.txt"


def verificar_archivos():
    BD_DIR.mkdir(exist_ok=True)
    if not CLIENTES_PATH.exists():
        with open(CLIENTES_PATH, "w", encoding="utf-8") as arcCli:
            pass
    if not PRODUCTOS_PATH.exists():
        with open(PRODUCTOS_PATH, "w", encoding="utf-8") as arcPro:
            pass
    if not VENTAS_PATH.exists():
        with open(VENTAS_PATH, "w", encoding="utf-8") as arcVen:
            pass


def main():
    verificar_archivos()
    while True:
        os.system("cls")
        print("Sistema de control de ventas")
        opciones=["Gestión de clientes...1",
              "Gestión de productos..2",
              "Efectuar Ventas ......3",
              "Salir.................4"]
        opcion=lbp.seleccionar_opcion("Menú principal",opciones)
        match opcion:
            case "1":
                cli.main()
            case "2":
                pro.main()   
            case "3":
                print("Efectuar Ventas")
            case "4":
                break
            
if __name__=="__main__":    
    main()