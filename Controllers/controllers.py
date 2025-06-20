from Models.models import Administrador, Mesero, Cliente, Mesa, Plato, Comanda

class SistemaRestaurante:
    def __init__(self, db):
        self.db = db
        self.actualUsuario = None
        self.actualRol = None

    def autenticar(self, cedula, password, rol):
        if rol == "administrador":
            query = "SELECT cedula, nombre, telefono, direccion, email FROM administrador WHERE cedula = ? AND password = ?"
            tipoUsuario = Administrador
        elif rol == "mesero":
            query = "SELECT cedula, nombre, telefono, direccion, email FROM mesero WHERE cedula = ? AND password = ?"
            tipoUsuario = Mesero
        elif rol == "cliente":
            query = "SELECT cedula, nombre, telefono, direccion, email FROM cliente WHERE cedula = ? AND password = ?"
            tipoUsuario = Cliente
        else:
            return False

        resultados = self.db.hacerConsultas(query, (cedula, password), resultado=True)
        if resultados:
            datos = resultados[0]
            self.actualUsuario = tipoUsuario(*datos)
            self.actualRol = rol
            return True
        return False

    def generarInformeAdministrador(self, fecha=None):
        if isinstance(self.actualUsuario, Administrador):
            return self.actualUsuario.generar_informe(self.db, fecha)
        else:
            print(" el Usuario actual no es un administrador  .")
            return None

    def obtenerMesas(self, estado=None):
        try:
            if estado:
                consultaMesa = "SELECT * FROM mesa WHERE estado = ?"
                resultados = self.db.hacerConsultas(consultaMesa, (estado,), resultado=True)
            else:
                consultaMesa = "SELECT * FROM mesa"
                resultados = self.db.hacerConsultas(consultaMesa, resultado=True)

            if resultados:
                return [Mesa(fila[0], fila[1]) for fila in resultados]
            return []
        except Exception as error:
            print(f"Error al obtener mesas: {error}")
            return []

    def obtenerPlatos(self):
        try:
            resultados = self.db.hacerConsultas("SELECT * FROM plato", resultado=True)
            if resultados:
                return [Plato(fila[0], fila[1], fila[2]) for fila in resultados]
            return []
        except Exception as error:
            print(f"Error al obtener platos: {error}")
            return []

    def obtenerComandas(self, estado=None):
        try:
            if estado:
                consultaComanda = "SELECT id FROM comanda WHERE estado = ?"
                resultados = self.db.hacerConsultas(consultaComanda, (estado,), resultado=True)
            else:
                consultaComanda = "SELECT id FROM comanda"
                resultados = self.db.hacerConsultas(consultaComanda, resultado=True)

            if resultados:
                return [Comanda.obtener_por_id(self.db, fila[0]) for fila in resultados]
            return []
        except Exception as error:
            print(f"Error al obtener comandas: {error}")
            return []

    def obtenerMeseros(self):
        resultados = self.db.hacerConsultas("SELECT * FROM mesero", resultado=True)
        if resultados:
            return [Mesero(fila[0], fila[1], fila[2], fila[3], fila[4]) for fila in resultados]
        return []

    def obtenerClientes(self):
        try:
            resultados = self.db.hacerConsultas("SELECT * FROM cliente", resultado=True)
            if resultados:
                return [Cliente(fila[0], fila[1], fila[2], fila[3], fila[4]) for fila in resultados]
            return []
        except Exception as error:
            print(f"Error al obtener clientes: {error}")
            return []
