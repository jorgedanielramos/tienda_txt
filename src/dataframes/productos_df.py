import os
import pandas as pd
from pathlib import Path
from src.ui import interfaz as ui
from config import PRODUCTOS_PATH
from models.modelos_clases import Productos
from config import PRODUCTOS_PATH

def main():
    df_productos=pd.read_csv(PRODUCTOS_PATH)
    while True:
        os.system("cls")
        print("Gestión de productos")
        opciones=[
              "Alta de productos....1",
              "Modificacón de datos.2",
              "Bajas de productos...3",
              "Reactivar productos..4",
              "Listado de productos.5",
              "Volver...............6"]
        opcion=ui.seleccionar_opcion("Gestión de productos",opciones)
        match opcion:
            case "1":
                os.system("cls")
                print("Alta de productos")
                print("=================")
                nombre,descripcion,precio,stock,estado=ui.entrada_datos_producto()
                resp=input("Desea guardar el producto? (s/n)")
                if resp.lower()=="s":
                    producto = Productos(None, nombre.capitalize(), descripcion.capitalize(), precio, stock, estado)
                    df_productos = producto.grabar_producto(df_productos, producto)    
            case "2":
                print("Modificacón de datos")
                idProd=int(input("Indique ID del producto a modificar:"))
                if idProd>=0:             
                    p=Productos(None,"","",None,None)
                    producto=p.buscar_producto(df_productos,idProd)
                    if producto and producto.estado=="Activo":
                        print(f"Producto encontrado: {producto.nombre} {producto.descripcion}")
                        nombre,descripcion,precio,stock,estado=ui.entrada_datos_producto()
                        if nombre:
                            producto.nombre=nombre.capitalize()
                        if descripcion:
                            producto.descripcion=descripcion.capitalize()
                        if precio is not None:
                            producto.precio=precio
                        if stock is not None:
                            producto.stock=stock
                        if estado:
                            producto.estado=estado
                        if not (nombre or descripcion or precio is not None or stock is not None or estado):
                            print("No se realizaron cambios.")
                        else:
                            resp=input("Desea guardar los cambios? (s/n)")
                            if resp.lower()=="s":
                                df_productos=producto.modificar_producto(df_productos, producto)
            case "3":
                print("Bajas de productos")
                idProd=int(input("Indique ID del producto a dar de baja:"))
                if idProd>=0:          
                    p=Productos(None,"","",None,None)
                    producto=p.buscar_producto(df_productos,idProd)
                    if producto and producto.estado=="Activo":
                        print(f"Producto encontrado: {producto.nombre} {producto.descripcion}")
                        resp=input("Desea dar de baja al producto? (s/n)")
                        if resp.lower()=="s":
                            df_productos.loc[df_productos['id'] == producto.id, 'estado'] = 'Inactivo'
                    else:
                        print("Producto no encontrado o ya inactivo")
                        nada=input("Presione Enter para continuar...")
            case "4":
                print("Reactivar productos")
                idProd=int(input("Indique ID del producto a reactivar:"))
                if idProd>=0:          
                    p=Productos(None,"","",None,None)
                    producto=p.buscar_producto(df_productos,idProd)
                    if producto and producto.estado=="Inactivo":
                        print(f"Producto encontrado: {producto.nombre} {producto.descripcion}")
                        resp=input("Desea reactivar el producto? (s/n)")
                        if resp.lower()=="s":
                            df_productos.loc[df_productos['id'] == producto.id, 'estado'] = 'Activo'
                    else:
                        print("Producto no encontrado o ya activo")
                        nada=input("Presione Enter para continuar...")
            case "5":
                print("Listado de productos")
                p=Productos(None,"","",None,None)
                p.listar_productos(df_productos)
                nada=input("Presione Enter para continuar...")
            case "6":                 
                df_productos.to_csv(PRODUCTOS_PATH, index=False)
                break