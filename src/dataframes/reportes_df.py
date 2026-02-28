import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import src.lib.librerias_propias as lbp
from datetime import datetime
import os
from pathlib import Path
from models.modelos_clases import Persona, Productos
from src.services.reportes_service import crear_ventas_completas,filtrado_ultimos_12_meses,agrupar_por_mes
from src.ui import interfaz as ui
from config import CLIENTES_PATH, PRODUCTOS_PATH, FACTURAS_PATH, DETALLES_PATH, VENTAS_COMPLETAS_PATH
from src.graphics.graphics_ventas import ventas_globales_12_mes


def main():
    df_clientes=pd.read_csv(CLIENTES_PATH)
    df_productos = pd.read_csv(PRODUCTOS_PATH)
    df_ventas_completas = crear_ventas_completas()
    opciones=["Reporte venta globales 12 meses..1",
              "Reporte por cliente 12 meses.....2",
              "Generar por producto 12 meses....3",
              "Reporte por mayores ventas.......4",
              "Reporte por strock bajo..........5",
              "Volver ..........................6"]
    while True:
        os.system("cls")
        print("Gestión de reportes")  
        opcion=ui.seleccionar_opcion("Gestión de reportes",opciones)
        match opcion:
            case "1":
                print("Reporte venta globales 12 meses")
                ventas_globales_12(df_ventas_completas)
            case "2":

                ventas_cliente_12(df_ventas_completas,df_clientes)
            case "3":
                ventas_producto_12(df_ventas_completas,df_productos)
            case "4":
                ventas_productos_mas_vendidos(df_ventas_completas)
                print("Reporte por producto de mayores ventas")
            case "5":
                print("Reporte por strock bajo")
            case "6":
                df_ventas_completas.to_csv(VENTAS_COMPLETAS_PATH, index=False)
                return

def ventas_globales_12(df_ventas_completas):
    ventas_ultimos_12_meses = filtrado_ultimos_12_meses(df_ventas_completas)
    # Agrupar por año-mes y sumar total_factura
    ventas_por_mes = agrupar_por_mes(ventas_ultimos_12_meses, 'agno_mes')
    print("Ventas globales por mes en los últimos 12 meses:")
    print(ventas_por_mes)
    resp = input("¿Desea graficar el reporte? (s/n): ")
    if resp.lower() == 's':
        ventas_globales_12_mes(ventas_por_mes, 'agno_mes', 'total_factura', "Ventas Globales por Mes", "Año-Mes", "Total Facturado €")


def  ventas_cliente_12(df_ventas_completas,df_clientes):
    # Filtrar ventas de los últimos 12 meses
        ventas_ultimos_12_meses = filtrado_ultimos_12_meses(df_ventas_completas)    
        while True:
            os.system("cls")
            print("reporte por cliente 12 meses")
            id_cliente = lbp.validar_numero_int("Ingrese ID del cliente para el reporte [0 para finalizar]: ")

            if id_cliente == 0:
                break

            p=Persona(None,None,None,None,None,None,None)
            cliente = p.buscar_persona(df_clientes, id_cliente)
            if cliente is None:
                print("Cliente no encontrado.")
                nada=input("Presione Enter para continuar...")
                continue
            ventas_cliente = ventas_ultimos_12_meses[ventas_ultimos_12_meses['id_cliente'] == id_cliente]
            if ventas_cliente.empty:
                print("No hay ventas para este cliente en los últimos 12 meses.")
                nada=input("Presione Enter para continuar...")
                continue
            # Agrupar por cliente y sumar total_factura
            ventas_cliente = agrupar_por_mes(ventas_cliente, ['nombre_cliente', 'agno_mes'])
            
            print(f"Ventas del cliente '{cliente.nombre} {cliente.apellido}' en los últimos 12 meses:")
            print(ventas_cliente)
            resp=input("desea graficar el reporte? (s/n): ")
            if resp.lower() == 's':
                #ventas_cliente_12_grafica(ventas_cliente)
                ventas_globales_12_mes(ventas_cliente, 'agno_mes', 'total_factura', f"Ventas Globales por Mes del cliente {ventas_cliente['nombre_cliente'].iloc[0]}", "Año-Mes", "Total Facturado €")


def ventas_producto_12(df_ventas_completas,df_productos):
    # Filtrar ventas de los últimos 12 meses
        ventas_ultimos_12_meses = filtrado_ultimos_12_meses(df_ventas_completas)
        while True:
            os.system("cls")
            print("reporte por producto 12 meses")
            id_producto = lbp.validar_numero_int("Ingrese ID del producto para el reporte [0 para finalizar]: ")
            if id_producto == 0:
                break

            p=Productos(None,None,None,None,None,None)
            producto = p.buscar_producto(df_productos, id_producto)
            if producto is None:
                print("Producto no encontrado.")
                nada=input("Presione Enter para continuar...")
                continue
            ventas_producto = ventas_ultimos_12_meses[ventas_ultimos_12_meses['id_producto'] == id_producto]
            if ventas_producto.empty:
                print("No hay ventas para este producto en los últimos 12 meses.")
                nada=input("Presione Enter para continuar...")
                continue
            # Agrupar por producto y sumar total_factura
            ventas_por_producto = ventas_producto.groupby(['nombre_y', 'agno_mes'])['total_factura'].sum().reset_index()
            print(f"Ventas del producto '{producto.nombre}' en los últimos 12 meses:")
            print(ventas_por_producto)
            resp=input("desea graficar el reporte? (s/n): ")
            if resp.lower() == 's':
                #ventas_producto_12_grafica(ventas_por_producto)
                ventas_globales_12_mes(ventas_por_producto, 'agno_mes', 'total_factura', f"Ventas Globales por Mes del producto {ventas_por_producto['nombre_y'].iloc[0]}", "Año-Mes", "Total Facturado €")


def ventas_productos_mas_vendidos(df_ventas_completas):
    # Filtrar ventas de los últimos 12 meses
    ventas_ultimos_12_meses = filtrado_ultimos_12_meses(df_ventas_completas)
    # Agrupar por producto: cantidad total y monto facturado total
    ventas_por_producto = (ventas_ultimos_12_meses.groupby('nombre_y').agg(
    cantidad_total=('cantidad', 'sum'),
    monto_total=('total_detalle', 'sum')
).reset_index()).sort_values(by='cantidad_total', ascending=False).head(10)

    # Ordenar por cantidad vendida y mostrar los top 10
   # productos_mas_vendidos = ventas_por_producto.sort_values(
   #     by='cantidad_total',
   #     ascending=False
    #).head(10)

    print("Top 10 Productos Más Vendidos en los Últimos 12 Meses:")
    print(ventas_por_producto)

    resp = input("¿Desea graficar el reporte? (s/n): ")
    if resp.lower() == 's':
        ventas_globales_12_mes(ventas_por_producto, 'nombre_y', 'cantidad_total', "Top 10 Productos Más Vendidos en los Últimos 12 Meses", "Producto", "Cantidad Vendida","barra")

#def productos_mas_vendidos_grafica(productos_mas_vendidos):
#    fig, ax = plt.subplots(figsize=(12, 8))

    # Ordenar para que la barra más larga quede arriba
#    productos_mas_vendidos = productos_mas_vendidos.sort_values("cantidad_total", ascending=True)

#    sns.barplot(
#        data=productos_mas_vendidos,
#        x='cantidad_total',
#        y='nombre_y',
#        ax=ax,
#        color='steelblue'
#    )

    # Aumentar el límite del eje X para que se vean las etiquetas
#    ax.set_xlim(0, productos_mas_vendidos['cantidad_total'].max() * 1.30)

#    ax.set_title("Top 10 Productos Más Vendidos en los Últimos 12 Meses")
#    ax.set_xlabel("Cantidad Vendida")
#    ax.set_ylabel("Producto")

    # Etiquetas al final de cada barra
#    for index, row in productos_mas_vendidos.iterrows():
#        cantidad_fmt = f"{row['cantidad_total']:,.0f}".replace(",", ".")
#        monto_fmt = f"{row['monto_total']:,.0f}".replace(",", ".")

#        ax.text(
#            row['cantidad_total'] * 1.02,
#            index,
#            f"{cantidad_fmt} uds | € {monto_fmt}",
#            va='center',
#            ha='left',
#            fontsize=10,
#            color='black',
#            fontweight='bold'
#        )

#    plt.tight_layout()
#    plt.show()