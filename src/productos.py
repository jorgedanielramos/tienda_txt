import os
from pathlib import Path
from . import librerias_propias as lbp

BASE_DIR = Path(__file__).resolve().parents[1]
PRODUCTOS_PATH = BASE_DIR / "BD" / "Productos.txt"


def determinar_id_producto():
    with open(PRODUCTOS_PATH, "r", encoding="utf-8") as arcPro:
        lineas=arcPro.readlines()
        if len(lineas)==0:
            return 1
        else:
            ultimo_producto=lineas[-1]
            id_ultimo_producto=int(ultimo_producto.split(";")[0])
            return id_ultimo_producto+1
def main():
    while True:
        os.system("cls")
        print("Gestión de productos")
        opciones=["Alta de productos...1",
              "Modificacón de datos...2",
              "Bajas de productos......3",
              "Volver.................4"]
        opcion=lbp.seleccionar_opcion("Gestión de productos",opciones)
        match opcion:
            case "1":
                os.system("cls")
                print("Alta de productos")
                print("=================")
                nombre=input("Indique nombre del producto:")
                descripcion=input("Indique descripción del producto:")
                precio=lbp.validar_precio()
                stock=lbp.validar_stock()
                resp=input("Desea guardar el producto? (s/n)")
                if resp.lower()=="s":
                    id_producto=determinar_id_producto()
                    with open(PRODUCTOS_PATH, "a", encoding="utf-8") as arcPro:
                        arcPro.write(f"{id_producto};{nombre.capitalize()};{descripcion.capitalize()};{precio};{stock}\n")
            case "2":
                print("Modificacón de datos")
            case "3":
                print("Bajas de productos")
            case "4":
                break