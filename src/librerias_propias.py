import os
from pathlib import Path
import pandas as pd


def seleccionar_opcion(titulo, opciones):
    os.system("cls")
    print(titulo)
    for opcion in opciones:
        print(opcion)
    op=input("Indique opción:")
    return op

def validar_correo():
    while True:
        correo=input("Indique correo electrónico del cliente:")
        if "@" in correo and "." in correo:
            return correo
        else:
            print("Correo no válido. Intente nuevamente.")

def validar_telefono():
    while True:
        telefono=input("Indique teléfono del cliente:")
        if telefono.isdigit() or telefono == "":
            return telefono
        else:
            print("Teléfono no válido. Intente nuevamente.")

def validar_precio():
    while True:
        precio=input("Indique precio del producto:")
        try:
            precio_float=float(precio)
            if precio_float > 0:
                return precio_float
            else:
                print("El precio debe ser mayor a cero. Intente nuevamente.")
        except ValueError:
            print("Precio no válido. Intente nuevamente.")

def validar_stock():
    while True:
        stock=input("Indique stock del producto:")
        if stock.isdigit() and int(stock) >= 0:
            return int(stock)
        else:
            print("Stock no válido. Intente nuevamente.")   

def verificar_archivos():
    BASE_DIR = Path(__file__).resolve().parents[1]
    BD_DIR = BASE_DIR / "dataframes"
    CLIENTES_PATH = BD_DIR / "Clientes.csv"
    PRODUCTOS_PATH = BD_DIR / "Productos.csv"
    FACTURAS_PATH = BD_DIR / "Facturas.csv"
    DETALLES_PATH = BD_DIR / "Detalles.csv"
    BD_DIR.mkdir(exist_ok=True)
    if not CLIENTES_PATH.exists():      
        df_clientes = pd.DataFrame(columns=['id', 'nombre', 'apellido', 'correo', 'telefono','tipo', 'estado'])
        df_clientes.to_csv(CLIENTES_PATH, index=False)

    if not PRODUCTOS_PATH.exists():
        df_productos = pd.DataFrame(columns=['id', 'nombre', 'descripcion', 'precio', 'stock', 'estado'])
        df_productos.to_csv(PRODUCTOS_PATH, index=False)
    if not FACTURAS_PATH.exists():
        df_facturas = pd.DataFrame(columns=['id', 'id_cliente', 'fecha', 'subtotal','iva','descuento', 'estado'])
        df_facturas.to_csv(FACTURAS_PATH, index=False)
        df_detalles = pd.DataFrame(columns=['id_factura', 'id_producto', 'cantidad', 'precio_unitario'])
        df_detalles.to_csv(DETALLES_PATH, index=False)
