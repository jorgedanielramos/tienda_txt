import os


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
        if telefono.isdigit() and len(telefono) == 10:
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