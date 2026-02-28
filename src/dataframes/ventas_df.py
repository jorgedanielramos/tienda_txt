import pandas as pd
import src.lib.librerias_propias as lbp
from datetime import datetime
import os

from models.modelos_clases import Persona, Productos
#from src.dataframes import clientes_df, productos_df
from src.ui import interfaz as ui
from config import FACTURAS_PATH, DETALLES_PATH, CLIENTES_PATH, PRODUCTOS_PATH
    
def main():
    df_facturas = pd.read_csv(FACTURAS_PATH)
    df_detalles = pd.read_csv(DETALLES_PATH)
    df_clientes=pd.read_csv(CLIENTES_PATH)
    df_productos = pd.read_csv(PRODUCTOS_PATH)
    opciones=["Crear facturas.......1",
              "Consultar facturas...2",
              "Volver ..............3"]
    while True:
        os.system("cls")

        print("Gestión de ventas")  
        opcion=ui.seleccionar_opcion("Gestión de ventas",opciones)
        match opcion:
            case "1":
               df_facturas, df_detalles,df_productos = crear_factura(df_facturas, df_detalles, df_clientes, df_productos)
            case "2":
                print("Consultar facturas")
                consultar_factura(df_facturas, df_detalles, df_clientes, df_productos)
            case "3":
                df_clientes.to_csv(CLIENTES_PATH, index=False)
                df_productos.to_csv(PRODUCTOS_PATH, index=False)    
                df_facturas.to_csv(FACTURAS_PATH, index=False)
                df_detalles.to_csv(DETALLES_PATH, index=False)
                return

def crear_factura(df_facturas, df_detalles, df_clientes, df_productos):
    os.system("cls")
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
        
        id_factura = generar_id_unico(df_facturas)
        mostrar_encabezado_factura(id_factura, cliente, hoy)
        detalles = []
        while True:
            producto_id = input("Ingrese el ID del producto (o 'fin' para terminar): ")
            if producto_id.lower() == 'fin':
                break
            producto = Productos(None,"",None,None,None)
            producto = producto.buscar_producto(df_productos, int(producto_id))
            if producto is None:
                print("Producto no encontrado. Intente nuevamente.")
                continue
            print(f"Producto: {producto.nombre}, Descripción: {producto.descripcion}, Precio: {producto.precio}")
            cantidad = lbp.validar_numero_int("Ingrese la cantidad: ")
            if cantidad > producto.stock:
                print("Stock insuficiente. Intente nuevamente.")
                continue
            precio_unitario = producto.precio
            total_producto = cantidad * precio_unitario
            subtotal += total_producto
            print(f"Subtotal del producto: {total_producto}")
            detalles.append({
                "id_factura": id_factura,
                "id_producto": int(producto_id),
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
            })
        iva = subtotal * 0.19
        descuento = 0
        total_factura = subtotal + iva - descuento
        print(f"Subtotal: {subtotal}, IVA: {iva}, Descuento: {descuento}, Total: {total_factura}")
        if detalles:
            resp=input("¿Desea guardar la factura? (s/n): ")
            if resp.lower() != 's':
                continue
            nueva_factura = {
                "id": id_factura,
                "id_cliente": int(idCli),
                "fecha": hoy,
                "subtotal": subtotal,
                "iva": iva,
                "descuento": descuento,
                "estado": "Pendiente"
            }
            
            df_facturas = pd.concat([df_facturas, pd.DataFrame([nueva_factura])], ignore_index=True)
            df_detalles = pd.concat([df_detalles, pd.DataFrame(detalles)], ignore_index=True)
            for detalle in detalles:
                producto_id = detalle["id_producto"]
                cantidad = detalle["cantidad"]
                df_productos.loc[df_productos['id'] == producto_id, 'stock'] -= cantidad
            print("Factura creada exitosamente.")
            nada=input("Presione Enter para continuar...")
    return df_facturas, df_detalles, df_productos

def consultar_factura(df_facturas, df_detalles, df_clientes, df_productos):
    os.system("cls")
    id_factura = lbp.validar_numero_int("Ingrese el ID de la factura a consultar: ")
    factura = df_facturas[df_facturas['id'] == id_factura]
    if factura.empty:
        print("Factura no encontrada.")
        nada=input("Presione Enter para continuar...")
        return
    factura = factura.iloc[0]
    cliente = df_clientes[df_clientes['id'] == factura['id_cliente']].iloc[0]
    detalles = df_detalles[df_detalles['id_factura'] == id_factura]
    print(f"Factura #: {factura['id']}")
    print(f"Cliente: {cliente['nombre']} {cliente['apellido']}")
    print(f"Fecha: {factura['fecha']}")
    print(f"Subtotal: {factura['subtotal']}, IVA: {factura['iva']}, Descuento: {factura['descuento']}, Total: {factura['subtotal'] + factura['iva'] - factura['descuento']}")
    print("\nDetalles:")
    for _, detalle in detalles.iterrows():
        producto = df_productos[df_productos['id'] == detalle['id_producto']].iloc[0]
        print(f"Producto: {producto['nombre']}, Cantidad: {detalle['cantidad']}, Precio Unitario: {detalle['precio_unitario']} Subtotal: {detalle['cantidad'] * detalle['precio_unitario']}")
    nada=input("Presione Enter para continuar...")  
def generar_id_unico(df):
    if df.empty:
        return 1
    else:
        return df['id'].max() + 1

def mostrar_encabezado_factura(id_factura, cliente, fecha):
    print(f"Factura #: {id_factura}")
    print(f"Cliente: {cliente.nombre} {cliente.apellido}")
    print(f"Fecha: {fecha}")



if __name__=="__main__":
    main()