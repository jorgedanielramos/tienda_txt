import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('es_ES')

# -----------------------------
# 1. CLIENTES
# -----------------------------
num_clientes = 300
clientes = []

for i in range(1, num_clientes + 1):
    clientes.append({
        'id': i,
        'nombre': fake.first_name(),
        'apellido': fake.last_name(),
        'correo': fake.email(),
        'telefono': fake.phone_number(),
        'tipo': random.choice(['Regular', 'Premium', 'VIP']),
        'estado': random.choice(['Activo', 'Inactivo'])
    })

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv("clientes.csv", index=False)

# -----------------------------
# 2. PRODUCTOS
# -----------------------------
num_productos = 200
productos = []

for i in range(1, num_productos + 1):
    productos.append({
        'id': i,
        'nombre': fake.word().capitalize(),
        'descripcion': fake.sentence(),
        'precio': round(random.uniform(5, 500), 2),
        'stock': random.randint(0, 500),
        'estado': random.choice(['Disponible', 'Agotado'])
    })

df_productos = pd.DataFrame(productos)
df_productos.to_csv("productos.csv", index=False)

# -----------------------------
# 3. FACTURAS
# -----------------------------
num_facturas = 500
facturas = []

for i in range(1, num_facturas + 1):
    subtotal = round(random.uniform(20, 2000), 2)
    iva = round(subtotal * 0.21, 2)
    descuento = round(random.uniform(0, 100), 2)

    facturas.append({
        'id': i,
        'id_cliente': random.randint(1, num_clientes),
        'fecha': fake.date_between(start_date='-1y', end_date='today'),
        'subtotal': subtotal,
        'iva': iva,
        'descuento': descuento,
        'estado': random.choice(['Pagada', 'Pendiente', 'Cancelada'])
    })

df_facturas = pd.DataFrame(facturas)
df_facturas.to_csv("facturas.csv", index=False)

# -----------------------------
# 4. DETALLES DE FACTURA
# -----------------------------
num_detalles = 1500
detalles = []

for _ in range(num_detalles):
    id_factura = random.randint(1, num_facturas)
    id_producto = random.randint(1, num_productos)
    cantidad = random.randint(1, 10)

    # Obtener precio del producto
    precio_unitario = df_productos.loc[df_productos['id'] == id_producto, 'precio'].values[0]

    detalles.append({
        'id_factura': id_factura,
        'id_producto': id_producto,
        'cantidad': cantidad,
        'precio_unitario': precio_unitario
    })

df_detalles = pd.DataFrame(detalles)
df_detalles.to_csv("detalles.csv", index=False)

print("CSV generados correctamente.")