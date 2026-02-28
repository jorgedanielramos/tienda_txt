from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[0]
BD_DIR = BASE_DIR / "datos/dataframes"
CLIENTES_PATH = BD_DIR / "Clientes.csv"
PRODUCTOS_PATH = BD_DIR / "Productos.csv"
FACTURAS_PATH = BD_DIR / "Facturas.csv"
DETALLES_PATH = BD_DIR / "Detalles.csv"
VENTAS_COMPLETAS_PATH = BD_DIR / "Ventas_completas.csv"
CANTIDAD_MESES=12