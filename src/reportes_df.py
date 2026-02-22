import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from . import librerias_propias as lbp
from datetime import datetime
import os
from pathlib import Path
from models.modelos_clases import Persona, Productos

# Declaracion de rutas base
BASE_DIR = Path(__file__).resolve().parents[1]
BD_DIR = BASE_DIR / "dataframes"
CLIENTES_PATH = BD_DIR / "clientes.csv"
PRODUCTOS_PATH = BD_DIR / "productos.csv"
FACTURAS_PATH = BD_DIR / "facturas.csv"
DETALLES_PATH = BD_DIR / "detalles.csv"
VENTAS_COMPLETAS_PATH = BD_DIR / "ventas_completas.csv"

def main():
    df_facturas = pd.read_csv(FACTURAS_PATH)
    df_detalles = pd.read_csv(DETALLES_PATH)
    df_clientes=pd.read_csv(CLIENTES_PATH)
    df_productos = pd.read_csv(PRODUCTOS_PATH)

    df_ventas_completas = merge_tablas(df_facturas, df_detalles, df_clientes, df_productos)
    df_ventas_completas = preparar_datos_para_reportes(df_ventas_completas)
    
    opciones=["Reporte venta globales 12 meses..1",
              "Reporte por cliente 12 meses.....2",
              "Generar por producto 12 meses....3",
              "Reporte por mayores ventas.......4",
              "Reporte por strock bajo..........5",
              "Volver ..........................6"]
    while True:
        os.system("cls")
        print("Gestión de reportes")  
        opcion=lbp.seleccionar_opcion("Gestión de reportes",opciones)
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

def preparar_datos_para_reportes(ventas_completas):
    ventas_completas['fecha'] = pd.to_datetime(ventas_completas['fecha'])

    ventas_completas['total_detalle'] = ventas_completas['cantidad'] * ventas_completas['precio']

    ventas_completas['total_factura'] = ventas_completas.groupby('id_factura')['total_detalle'].transform('sum')
    ventas_completas['total_factura'] = pd.to_numeric(ventas_completas['total_factura'], errors='coerce')

    ventas_completas['agno_mes'] = ventas_completas['fecha'].dt.to_period('M').astype(str)

    ventas_completas['agno'] = ventas_completas['fecha'].dt.year
    ventas_completas['mes'] = ventas_completas['fecha'].dt.month

    ventas_completas['nombre_cliente'] = ventas_completas['nombre_x'] + ' ' + ventas_completas['apellido']

    return ventas_completas

def merge_tablas(df_facturas, df_detalles, df_clientes, df_productos):
    
 # Merge de dataframes para reportes
    # Unir facturas con detalles
    df_ventas_completas = pd.merge(df_facturas, df_detalles,
                                left_on="id",
                                right_on="id_factura")
    
    # Unir con clientes
    df_ventas_completas = pd.merge(df_ventas_completas, df_clientes,
                                left_on="id_cliente",
                                right_on="id")
    
    # Unir con productos
    df_ventas_completas = pd.merge(df_ventas_completas, df_productos, 
                                left_on="id_producto",
                                right_on="id")
    return df_ventas_completas   

def ventas_globales_12(df_ventas_completas):
    # Filtrar ventas de los últimos 12 meses
    fecha_hoy = datetime.now()
    fecha_12_meses_atras = fecha_hoy - pd.DateOffset(months=12)
    ventas_ultimos_12_meses = df_ventas_completas[df_ventas_completas['fecha'] >= fecha_12_meses_atras]

    # Agrupar por año-mes y sumar total_factura
    ventas_por_mes = ventas_ultimos_12_meses.groupby('agno_mes')['total_factura'].sum().reset_index()

    #Graficar
    ventas_globales_12_mes(ventas_por_mes)

def ventas_globales_12_mes(ventas_por_mes):
    # Asegurar un solo valor por mes
    ventas_por_mes = ventas_por_mes.groupby('agno_mes', as_index=False)['total_factura'].sum()
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.lineplot(
        data=ventas_por_mes,
        x='agno_mes',
        y='total_factura',
        marker='o',
        ci=None,
        ax=ax
    )

    ax.set_title("Ventas Globales por Mes")
    ax.set_xlabel("Año-Mes")
    ax.set_ylabel("Total Facturado €")

    plt.setp(ax.get_xticklabels(), rotation=0, ha='right')

    # Etiquetas sobre cada punto
    for i, row in ventas_por_mes.iterrows():
        ax.text(
            row['agno_mes'],
            row['total_factura'],
            f"{row['total_factura']:.0f}",
            ha='center',
            va='bottom',
            fontsize=9,
            color='red'
        )

    plt.tight_layout()
    plt.show()

def  ventas_cliente_12(df_ventas_completas,df_clientes):
    # Filtrar ventas de los últimos 12 meses
        fecha_hoy = datetime.now()
        fecha_12_meses_atras = fecha_hoy - pd.DateOffset(months=12)
        ventas_ultimos_12_meses = df_ventas_completas[df_ventas_completas['fecha'] >= fecha_12_meses_atras]
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
            ventas_por_cliente = ventas_cliente.groupby(['nombre_cliente', 'agno_mes'])['total_factura'].sum().reset_index()
            
            print(f"Ventas del cliente '{cliente.nombre} {cliente.apellido}' en los últimos 12 meses:")
            print(ventas_por_cliente)
            resp=input("desea graficar el reporte? (s/n): ")
            if resp.lower() == 's':
                ventas_cliente_12_grafica(ventas_por_cliente)

def ventas_cliente_12_grafica(ventas_por_cliente):

    # Ordenar meses correctamente
    ventas_por_cliente['agno_mes'] = pd.to_datetime(ventas_por_cliente['agno_mes'])
    ventas_por_cliente = ventas_por_cliente.sort_values('agno_mes')
    ventas_por_cliente['agno_mes'] = ventas_por_cliente['agno_mes'].dt.strftime('%Y-%m')

    # Obtener nombre del cliente
    cliente_nombre = ventas_por_cliente['nombre_cliente'].iloc[0]

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.barplot(
        data=ventas_por_cliente,
        x='agno_mes',
        y='total_factura',
        ax=ax
    )

    ax.set_title(f"Ventas de {cliente_nombre} en los Últimos 12 Meses")
    ax.set_xlabel("Año-Mes")
    ax.set_ylabel("Total Facturado €")

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Etiquetas sobre cada barra
    for i, row in ventas_por_cliente.iterrows():
        valor_formateado = f"{row['total_factura']:,.0f}".replace(",", ".")
        ax.text(
            i,
            row['total_factura'],
            valor_formateado,
            ha='center',
            va='bottom',
            fontsize=9,
            color='red'
        )

    plt.tight_layout()
    plt.show()

def ventas_producto_12(df_ventas_completas,df_productos):
    # Filtrar ventas de los últimos 12 meses
        fecha_hoy = datetime.now()
        fecha_12_meses_atras = fecha_hoy - pd.DateOffset(months=12)
        ventas_ultimos_12_meses = df_ventas_completas[df_ventas_completas['fecha'] >= fecha_12_meses_atras]
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
                ventas_producto_12_grafica(ventas_por_producto)

def ventas_producto_12_grafica(ventas_por_producto):

    # Ordenar meses correctamente
    ventas_por_producto['agno_mes'] = pd.to_datetime(ventas_por_producto['agno_mes'])
    ventas_por_producto = ventas_por_producto.sort_values('agno_mes')
    ventas_por_producto['agno_mes'] = ventas_por_producto['agno_mes'].dt.strftime('%Y-%m')
    # Graficar
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.barplot(
        data=ventas_por_producto,
        x='agno_mes',
        y='total_factura',
        ax=ax
    )

    ax.set_title(f"Ventas del producto '{ventas_por_producto['nombre_y'].iloc[0]}' en los Últimos 12 Meses")
    ax.set_xlabel("Año-Mes")
    ax.set_ylabel("Total Facturado €")

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    # Etiquetas sobre cada barra
    for i, row in ventas_por_producto.iterrows():
        ax.text(
            i,
            row['total_factura'],
            f"{row['total_factura']:,.0f}".replace(",", "."),
            ha='center',
            va='bottom',
            fontsize=9,
            color='red'
        )

    plt.tight_layout()
    plt.show()

def ventas_productos_mas_vendidos(df_ventas_completas):
    # Filtrar ventas de los últimos 12 meses
    fecha_hoy = datetime.now()
    fecha_12_meses_atras = fecha_hoy - pd.DateOffset(months=12)
    ventas_ultimos_12_meses = df_ventas_completas[df_ventas_completas['fecha'] >= fecha_12_meses_atras]

    # Agrupar por producto: cantidad total y monto facturado total
    ventas_por_producto = ventas_ultimos_12_meses.groupby('nombre_y').agg(
    cantidad_total=('cantidad', 'sum'),
    monto_total=('total_detalle', 'sum')
).reset_index()

    # Ordenar por cantidad vendida y mostrar los top 10
    productos_mas_vendidos = ventas_por_producto.sort_values(
        by='cantidad_total',
        ascending=False
    ).head(10)

    print("Top 10 Productos Más Vendidos en los Últimos 12 Meses:")
    print(productos_mas_vendidos)

    resp = input("¿Desea graficar el reporte? (s/n): ")
    if resp.lower() == 's':
        productos_mas_vendidos_grafica(productos_mas_vendidos)

def productos_mas_vendidos_grafica(productos_mas_vendidos):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Ordenar para que la barra más larga quede arriba
    productos_mas_vendidos = productos_mas_vendidos.sort_values("cantidad_total", ascending=True)

    sns.barplot(
        data=productos_mas_vendidos,
        x='cantidad_total',
        y='nombre_y',
        ax=ax,
        color='steelblue'
    )

    # Aumentar el límite del eje X para que se vean las etiquetas
    ax.set_xlim(0, productos_mas_vendidos['cantidad_total'].max() * 1.30)

    ax.set_title("Top 10 Productos Más Vendidos en los Últimos 12 Meses")
    ax.set_xlabel("Cantidad Vendida")
    ax.set_ylabel("Producto")

    # Etiquetas al final de cada barra
    for index, row in productos_mas_vendidos.iterrows():
        cantidad_fmt = f"{row['cantidad_total']:,.0f}".replace(",", ".")
        monto_fmt = f"{row['monto_total']:,.0f}".replace(",", ".")

        ax.text(
            row['cantidad_total'] * 1.02,
            index,
            f"{cantidad_fmt} uds | € {monto_fmt}",
            va='center',
            ha='left',
            fontsize=10,
            color='black',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.show()