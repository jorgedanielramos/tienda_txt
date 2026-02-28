from config import CLIENTES_PATH, PRODUCTOS_PATH, FACTURAS_PATH, DETALLES_PATH, VENTAS_COMPLETAS_PATH
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import CANTIDAD_MESES

def crear_ventas_completas():
    df_facturas = pd.read_csv(FACTURAS_PATH)
    df_detalles = pd.read_csv(DETALLES_PATH)
    df_clientes=pd.read_csv(CLIENTES_PATH)
    df_productos = pd.read_csv(PRODUCTOS_PATH)

    df_ventas_completas = merge_tablas(df_facturas, df_detalles, df_clientes, df_productos)
    df_ventas_completas = preparar_datos_para_reportes(df_ventas_completas)
    return df_ventas_completas

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

def filtrado_ultimos_12_meses(df):
    fecha_actual = pd.to_datetime("today")
    fecha_limite = fecha_actual - pd.DateOffset(months=CANTIDAD_MESES)
    df_filtrado = df[df['fecha'] >= fecha_limite]
    return df_filtrado

def agrupar_por_mes(df, agrupador):
    df['agno_mes'] = df['fecha'].dt.to_period('M').astype(str)
    ventas_por_mes = df.groupby(agrupador)['total_factura'].sum().reset_index()
    return ventas_por_mes