import pandas as pd

class Persona:
    def __init__(self, id, nombre, apellido, correo, telefono, tipo="Cliente",estado="Activo"):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.tipo = tipo
        self.estado = estado
    
    def __str__(self):
        return f"{self.id};{self.nombre};{self.apellido};{self.correo};{self.telefono}" 
    
    def determinar_id_persona(self, df_personas):
        if df_personas.empty:
            return 1
        return df_personas.iloc[-1, 0] + 1

    def buscar_persona(self, df_personas, id_persona):
        persona=df_personas[df_personas['id'] == id_persona]
        if not persona.empty:
            self.id = persona.iloc[0]['id']
            self.nombre = persona.iloc[0]['nombre']
            self.apellido = persona.iloc[0]['apellido']
            self.correo = persona.iloc[0]['correo']
            self.telefono = persona.iloc[0]['telefono']
            self.tipo = persona.iloc[0]['tipo']
            self.estado = persona.iloc[0]['estado']
            return self
        return None
        
    def listar_personas(self, personas):
        encabezado=personas.columns.tolist()
        print(";".join(encabezado))
        for _, fila in personas.iterrows():
            print(fila['id'], fila['nombre'], fila['apellido'], fila['correo'], fila['telefono'], fila['tipo'], fila['estado']) 
        return 
       
    def grabar_persona(self, df_personas, persona):
        self.id=self.determinar_id_persona(df_personas)
        persona.id=self.id
        df_personas.loc[len(df_personas)] = vars(persona)
        return df_personas


    def modificar_persona(self, personas,persona):
        #persona=personas[personas['id'] == persona.id]
        #if not persona.empty:
        personas.loc[personas['id'] == persona.id, 'nombre'] = persona.nombre
        personas.loc[personas['id'] == persona.id, 'apellido'] = persona.apellido
        personas.loc[personas['id'] == persona.id, 'correo'] = persona.correo
        personas.loc[personas['id'] == persona.id, 'telefono'] = persona.telefono
        personas.loc[personas['id'] == persona.id, 'tipo'] = persona.tipo
        personas.loc[personas['id'] == persona.id, 'estado'] = persona.estado
        return personas
    
class Productos:
    def __init__(self, id,nombre, descripcion, precio, stock, estado="Activo"):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.estado = estado
    
    def __str__(self):
        return f"{self.id};{self.nombre};{self.descripcion};{self.precio};{self.stock};{self.estado}"
   
    def determinar_id_producto(self, df_productos):
        if df_productos.empty:
            return 1
        return df_productos.iloc[-1, 0] + 1
    
    def grabar_producto(self, productos, producto):
        self.id=self.determinar_id_producto(productos)
        producto.id=self.id
        productos.loc[len(productos)] = vars(producto)
        return productos
    
    def modificar_producto(self, productos, producto):
        productos.loc[productos['id'] == producto.id, 'nombre'] = producto.nombre
        productos.loc[productos['id'] == producto.id, 'descripcion'] = producto.descripcion
        productos.loc[productos['id'] == producto.id, 'precio'] = producto.precio
        productos.loc[productos['id'] == producto.id, 'stock'] = producto.stock
        productos.loc[productos['id'] == producto.id, 'estado'] = producto.estado
        return productos
    
    def buscar_producto(self, productos, id_producto):
        producto=productos[productos['id'] == id_producto]
        if not producto.empty:
            self.id = producto.iloc[0]['id']
            self.nombre = producto.iloc[0]['nombre']
            self.descripcion = producto.iloc[0]['descripcion']
            self.precio = producto.iloc[0]['precio']
            self.stock = producto.iloc[0]['stock']
            self.estado = producto.iloc[0]['estado']
            return self
        return None
    
    def listar_productos(self, productos):
        encabezado=productos.columns.tolist()
        print(";".join(encabezado))
        for _, fila in productos.iterrows():
            print(fila['id'], fila['nombre'], fila['descripcion'], fila['precio'], fila['stock'], fila['estado']) 
        return
    