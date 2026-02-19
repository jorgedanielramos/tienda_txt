import os
from pathlib import Path
from . import librerias_propias as lbp
import pandas as pd
from models.modelos_clases import Productos

BASE_DIR = Path(__file__).resolve().parents[1]
PRODUCTOS_PATH = BASE_DIR / "dataframes" / "Productos.csv"


def main():
    df_productos=pd.read_csv(PRODUCTOS_PATH)
    while True:
        os.system("cls")
        print("Gestión de productos")
        opciones=["Alta de productos...1",
              "Modificacón de datos...2",
              "Bajas de productos......3",
              "Reactivar productos.....4",
              "Listado de productos....5",
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
                    producto = Productos(None, nombre.capitalize(), descripcion.capitalize(), precio, stock)
                    df_productos = producto.grabar_producto(df_productos, producto)    
            case "2":
                print("Modificacón de datos")
                idProd=int(input("Indique ID del producto a modificar:"))
                if idProd>=0:             
                    p=Productos(None,"","",None,None)
                    producto=p.buscar_producto(df_productos,idProd)
                    if producto and producto.estado=="Activo":
                        print(f"Producto encontrado: {producto.nombre} {producto.descripcion}")
                        nombre=input("Indique nuevo nombre del producto:")
                        descripcion=input("Indique nueva descripción del producto:")
                        precio=lbp.validar_precio()
                        stock=lbp.validar_stock()
                        if nombre:
                            producto.nombre=nombre.capitalize()
                        if descripcion:
                            producto.descripcion=descripcion.capitalize()
                        if precio is not None:
                            producto.precio=precio
                        if stock is not None:
                            producto.stock=stock
                        if not (nombre or descripcion or precio is not None or stock is not None):
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