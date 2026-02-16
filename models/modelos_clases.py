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
    
    def determinar_id_persona(self, PERSONA_PATH):
        with open(PERSONA_PATH, "r", encoding="utf-8") as arcPer:
            lineas=arcPer.readlines()
            if len(lineas)==0:
                return 1
            else:
                ultimo_cliente=lineas[-1]
                id_ultimo_cliente=int(ultimo_cliente.split(";")[0])
        return id_ultimo_cliente+1
        

    def buscar_persona(self,PERSONA_PATH,id_persona):
        listado_personas=self.listar_personas(PERSONA_PATH)
        encontro=-1
        for indice, persona in enumerate(listado_personas):
            if persona.id == id_persona:
                self.id = persona.id
                self.nombre = persona.nombre
                self.apellido = persona.apellido
                self.correo = persona.correo
                self.telefono = persona.telefono
                self.tipo = persona.tipo
                self.estado = persona.estado
                encontro=indice
                break
                
        if encontro != -1:
            return self
        else:
            return None
        
    def listar_personas(self, PERSONA_PATH):
        personas=[]
        with open(PERSONA_PATH, "r", encoding="utf-8") as arcPer:
            lineas=arcPer.readlines()
            for linea in lineas:
                datos=linea.strip().split(";")
                persona=Persona(int(datos[0]),datos[1],datos[2],datos[3],datos[4],datos[5],datos[6])
                personas.append(persona)
        return personas
       
    def grabar_persona(self, PERSONA_PATH):
        self.id=self.determinar_id_persona(PERSONA_PATH)
        with open(PERSONA_PATH, "a", encoding="utf-8") as arcPer:
            arcPer.write(f"{self.id};{self.nombre};{self.apellido};{self.correo};{self.telefono};{self.tipo};{self.estado}\n")

    def modificar_persona(self, PERSONA_PATH):
        personas=self.listar_personas(PERSONA_PATH)
        with open(PERSONA_PATH, "w", encoding="utf-8") as arcPer:
            for persona in personas:
                if persona.id == self.id:
                    arcPer.write(f"{self.id};{self.nombre};{self.apellido};{self.correo};{self.telefono};{self.tipo};{self.estado}\n")
                else:
                    arcPer.write(f"{persona.id};{persona.nombre};{persona.apellido};{persona.correo};{persona.telefono};{persona.tipo};{persona.estado}\n")
