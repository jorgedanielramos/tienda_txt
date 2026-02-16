import os
from pathlib import Path
from . import librerias_propias as lbp
from models.modelos_clases import Persona

BASE_DIR = Path(__file__).resolve().parents[1]
CLIENTES_PATH = BASE_DIR / "BD" / "Clientes.txt"



        
def main():
    while True:
        os.system("cls")
        print("Gestión de clientes")
        opciones=["Alta de clientes.....1",
              "Modificacón de datos...2",
              "Bajas de clientes......3",
              "Listado de clientes....4",
              "Reactivar clientes.....5",
              "Volver.................6"]
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
                cliente=Persona(None,nombre.capitalize(),apellido.capitalize(),correo,telefono)
                resp=input("Desea guardar el cliente? (s/n)")
                if resp.lower()=="s":
                    cliente.grabar_persona(CLIENTES_PATH)
            case "2":
                os.system("cls")
                print("Gestión de clientes")
                print("Modificacón de datos")
                print("=========== == =====")
                idCli=int(input("Indique ID del cliente a modificar:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(CLIENTES_PATH,idCli)
                    if cliente and cliente.estado=="Activo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        nombre=input("Indique nuevo nombre del cliente:")
                        apellido=input("Indique nuevo apellido del cliente:") 
                        correo=lbp.validar_correo()
                        telefono=lbp.validar_telefono()
                        if nombre:
                            cliente.nombre=nombre.capitalize()
                        if apellido:
                            cliente.apellido=apellido.capitalize()
                        if correo:
                            cliente.correo=correo
                        if telefono:
                            cliente.telefono=telefono
                        if not (nombre or apellido or correo or telefono):
                            print("No se realizaron cambios.")
                        else:
                            resp=input("Desea guardar los cambios? (s/n)")
                            if resp.lower()=="s":
                                cliente.modificar_persona(CLIENTES_PATH)
                    else:
                        print("Cliente no encontrado o inactivo")
                        nada=input("Presione Enter para continuar...")
            case "3":
                os.system("cls")
                print("Bajas de clientes")
                idCli=int(input("Indique ID del cliente a dar de baja:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(CLIENTES_PATH,idCli)
                    if cliente and cliente.estado=="Activo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        resp=input("Desea dar de baja al cliente? (s/n)")
                        if resp.lower()=="s":
                            cliente.estado="Inactivo"
                            cliente.modificar_persona(CLIENTES_PATH)
                    else:
                        print("Cliente no encontrado o inactivo")
                        nada=input("Presione Enter para continuar...")
            case "4":
                os.system("cls")
                print("Listado de clientes")
                print("===================")
                personas = Persona(None,"","",None,None,None,None).listar_personas(CLIENTES_PATH)
                for persona in personas:
                    if persona.estado=="Activo":
                        print(f"ID: {persona.id}, Nombre: {persona.nombre}, Apellido: {persona.apellido}, Correo: {persona.correo}, Teléfono: {persona.telefono}")
                nada=input("Presione Enter para continuar...")
            case "5":
                os.system("cls")
                print("Reactivar clientes")
                idCli=int(input("Indique ID del cliente a reactivar:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(CLIENTES_PATH,idCli)
                    if cliente and cliente.estado=="Inactivo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        resp=input("Desea reactivar al cliente? (s/n)")
                        if resp.lower()=="s":
                            cliente.estado="Activo"
                            cliente.modificar_persona(CLIENTES_PATH)
                    else:
                        print("Cliente no encontrado o ya activo")
                        nada=input("Presione Enter para continuar...")
            case "6":
                break