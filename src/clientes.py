import os
from pathlib import Path
from . import librerias_propias as lbp

BASE_DIR = Path(__file__).resolve().parents[1]
CLIENTES_PATH = BASE_DIR / "BD" / "Clientes.txt"


def determinar_id_cliente():
    with open(CLIENTES_PATH, "r", encoding="utf-8") as arcCli:
        lineas=arcCli.readlines()
        if len(lineas)==0:
            return 1
        else:
            ultimo_cliente=lineas[-1]
            id_ultimo_cliente=int(ultimo_cliente.split(";")[0])
            return id_ultimo_cliente+1
def main():
    while True:
        os.system("cls")
        print("Gestión de clientes")
        opciones=["Alta de clientes...1",
              "Modificacón de datos...2",
              "Bajas de clientes......3",
              "Volver.................4"]
        opcion=lbp.seleccionar_opcion("Gestión de clientes",opciones)
        match opcion:
            case "1":
                os.system("cls")
                print("Alta de clientes")
                print("=================")
                nombre=input("Indique nombre del cliente:")
                apellido=input("Indique apellido del cliente:") 
                correo=lbp.validar_correo()
                telefono=lbp.validar_telefono()
                resp=input("Desea guardar el cliente? (s/n)")
                if resp.lower()=="s":
                    id_cliente=determinar_id_cliente()
                    with open(CLIENTES_PATH, "a", encoding="utf-8") as arcCli:
                        arcCli.write(f"{id_cliente};{nombre.capitalize()};{apellido.capitalize()};{correo};{telefono}\n")
            case "2":
                print("Modificacón de datos")
            case "3":
                print("Bajas de clientes")
            case "4":
                break