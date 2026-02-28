import os
from pathlib import Path
import pandas as pd
from src.lib.librerias_propias import validar_correo, validar_telefono, validar_precio, validar_stock, validar_numero_int, verificar_archivos

def seleccionar_opcion(titulo, opciones):
    while True:
        os.system("cls")
        print(titulo)
        for opcion in opciones:
            print(opcion)
        op=input("Indique opción:")
        if not op.isdigit() or int(op) < 1 or int(op) > len(opciones):
            nada=input("Opción no válida. Intente nuevamente. Presione Enter para continuar...")
        else:
            break
    return op

def entrada_datos_cliente():
    nombre=input("Indique nombre del cliente:")
    apellido=input("Indique apellido del cliente:")
    correo=validar_correo()
    telefono=validar_telefono()
    tipo=seleccionar_opcion("Seleccione tipo de cliente:", ["1. Regular", "2. Premium"])
    estado="Activo"
    return nombre, apellido, correo, telefono, tipo, estado

def entrada_datos_producto():
    nombre=input("Indique nombre del producto:")
    descripcion=input("Indique descripción del producto:")
    precio=validar_precio()
    stock=validar_stock()
    estado="Activo"
    return nombre, descripcion, precio, stock, estado