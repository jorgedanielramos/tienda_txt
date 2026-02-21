import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
from . import librerias_propias as lbp
from datetime import datetime
import os
from pathlib import Path
from models.modelos_clases import Persona, Productos
from src import clientes_df, productos_df

# Declaracion de rutas base
BASE_DIR = Path(__file__).resolve().parents[1]
BD_DIR = BASE_DIR / "dataframes"
CLIENTES_PATH = BD_DIR / "clientes.csv"
PRODUCTOS_PATH = BD_DIR / "productos.csv"
FACTURAS_PATH = BD_DIR / "facturas.csv"
DETALLES_PATH = BD_DIR / "detalles.csv"

def main():
    df_facturas = pd.read_csv(FACTURAS_PATH)
    df_detalles = pd.read_csv(DETALLES_PATH)
    df_clientes=pd.read_csv(CLIENTES_PATH)
    df_productos = pd.read_csv(PRODUCTOS_PATH)

    # Unir facturas con detalles
    #ventas_completas = pd.merge(df_facturas, df_detalles, on='FacturaID')
    
    # Unir con clientes
    #ventas_completas = pd.merge(ventas_completas, df_clientes, on='ClienteID')
    
    # Unir con productos
    #ventas_completas = pd.merge(ventas_completas, df_productos, on='ProductoID')
    
    #print(ventas_completas.head())

    opciones=["Crear facturas...1","Consultar facturas...2","Volver al menú principal...3"]
    while True:
        os.system("cls")
        print("Gestión de ventas")  
        opcion=lbp.seleccionar_opcion("Gestión de ventas",opciones)
        match opcion:
            case "1":
               crear_factura()
            case "2":
                print("Consultar facturas")
            case "3":
                return

def crear_factura():
    os.system("cls")
    print("Creación de factura")
    while True:        
        idCli = input("Ingrese el ID del cliente o 'fin' para terminar: ")
        if idCli.lower() == 'fin':
            break
        idCli = int(idCli)
        p=Persona(None,"","",None,None)
        cliente=p.buscar_persona(df_clientes,idCli)
        if cliente is None:
            print("Cliente no encontrado. Intente nuevamente.")
            continue
        hoy = datetime.now().strftime("%Y-%m-%d")
        subtotal = 0
        iva = 0
        descuento = 0
        id_factura = generar_id_unico(df_facturas, "FacturaID")
        mostrar_encabezado_factura(id_factura, cliente, hoy)
        detalles = []
        while True:
            producto_id = input("Ingrese el ID del producto (o 'fin' para terminar): ")
            if producto_id.lower() == 'fin':
                break
            producto = Productos(None,"",None,None)
            producto = producto.buscar_producto(df_productos, producto_id)
            if producto.empty:
                print("Producto no encontrado. Intente nuevamente.")
                continue
            print(f"Producto: {producto['nombre'].values[0]}, Descripción: {producto['descripcion'].values[0]}, Precio: {producto['precio'].values[0]}")
            cantidad = lbp.validar_numero_int("Ingrese la cantidad: ")
            if cantidad > producto['stock'].values[0]:
                print("Stock insuficiente. Intente nuevamente.")
                continue
            precio_unitario = producto['precio'].values[0]
            total_producto = cantidad * precio_unitario
            subtotal += total_producto
            print(f"Subtotal del producto: {total_producto}")
            detalles.append({
                "id_factura": id_factura,
                "id_producto": int(producto_id),
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
            })
        if detalles:
            resp=input("¿Desea guardar la factura? (s/n): ")
            if resp.lower() != 's':
                continue
            iva = subtotal * 0.19
            descuento = 0
            total_factura = subtotal + iva - descuento
            print(f"Subtotal: {subtotal}, IVA: {iva}, Descuento: {descuento}, Total: {total_factura}")
            nueva_factura = {
                "id": id_factura,
                "id_cliente": int(idCli),
                "fecha": hoy,
                "subtotal": subtotal,
                "iva": iva,
                "descuento": descuento,
                "estado": "Pendiente"
            }
            df_facturas = df_facturas.append(nueva_factura, ignore_index=True)
            df_detalles = df_detalles.append(detalles, ignore_index=True)
            df_facturas.to_csv(FACTURAS_PATH, index=False)
            df_detalles.to_csv(DETALLES_PATH, index=False)
            print("Factura creada exitosamente.")

def generar_id_unico(df, columna_id):
    if df.empty:
        return 1
    else:
        return df[columna_id].max() + 1

def mostrar_encabezado_factura(id_factura, cliente, fecha):
    print(f"Factura #: {id_factura}")
    print(f"Cliente: {cliente.nombre} {cliente.apellido}")
    print(f"Fecha: {fecha}")

if __name__=="__main__":
    main()