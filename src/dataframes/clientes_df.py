import os
import pandas as pd
from pathlib import Path
from src.ui import interfaz as ui
from models.modelos_clases import Persona
from config import CLIENTES_PATH

def main():
    df_clientes=pd.read_csv(CLIENTES_PATH)
    while True:
        os.system("cls")
        print("Gestión de clientes")
        opciones=["Alta de clientes.....1",
              "Modificacón de datos...2",
              "Bajas de clientes......3",
              "Reactivar clientes.....4",
              "Listado de clientes....5",
              "Volver.................6"]
        opcion=ui.seleccionar_opcion("Gestión de clientes",opciones)
        match opcion:
            case "1":
                os.system("cls")
                print("Alta de clientes")
                print("=================")
                nombre,apellido,correo,telefono,tipo,estado=ui.entrada_datos_cliente()
                cliente=Persona(None,nombre.capitalize(),apellido.capitalize(),correo,telefono)
                resp=input("Desea guardar el cliente? (s/n)")
                if resp.lower()=="s":
                    df_clientes=cliente.grabar_persona(df_clientes,cliente)
                    
            case "2":
                os.system("cls")
                print("Gestión de clientes")
                print("Modificacón de datos")
                print("=========== == =====")
                idCli=int(input("Indique ID del cliente a modificar:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(df_clientes,idCli)
                    if cliente and cliente.estado=="Activo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        nombre,apellido,correo,telefono,tipo,estado=ui.entrada_datos_cliente()
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
                                df_clientes=cliente.modificar_persona(df_clientes, cliente)
                    else:
                        print("Cliente no encontrado o inactivo")
                        nada=input("Presione Enter para continuar...")
            case "3":
                os.system("cls")
                print("Bajas de clientes")
                idCli=int(input("Indique ID del cliente a dar de baja:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(df_clientes,idCli)
                    if cliente and cliente.estado=="Activo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        resp=input("Desea dar de baja al cliente? (s/n)")
                        if resp.lower()=="s":
                            df_clientes.loc[df_clientes['id'] == cliente.id, 'estado'] = 'Inactivo'
                            
                    else:
                        print("Cliente no encontrado o inactivo")
                        nada=input("Presione Enter para continuar...")
            case "4":
                os.system("cls")
                print("Reactivar clientes")
                idCli=int(input("Indique ID del cliente a reactivar:"))
                if idCli>=0:
                    p=Persona(None,"","",None,None)
                    cliente=p.buscar_persona(df_clientes,idCli)
                    if cliente and cliente.estado=="Inactivo":
                        print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
                        resp=input("Desea reactivar al cliente? (s/n)")
                        if resp.lower()=="s":
                            df_clientes.loc[df_clientes['id'] == cliente.id, 'estado'] = 'Activo'
                            #df_clientes.to_csv(CLIENTES_PATH, index=False)
                    else:
                        print("Cliente no encontrado o ya activo")
                        nada=input("Presione Enter para continuar...")
            
            case "5":
                os.system("cls")
                print("Listado de clientes")
                print("===================")
                personas = Persona(None,"","",None,None,None,None).listar_personas(df_clientes)
                nada=input("Presione Enter para continuar...")
            case "6":
                df_clientes.to_csv(CLIENTES_PATH, index=False)
                break