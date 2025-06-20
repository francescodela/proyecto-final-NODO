from datetime import datetime

class Persona:
    def __init__(self, cedula, nombre, telefono=None, direccion=None, email=None):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

class Administrador(Persona):
    def __init__(self, cedula, nombre, telefono=None, direccion=None, email=None):
        super().__init__(cedula, nombre, telefono, direccion, email)

    def gestionar_meseros(self, db, accion, mesero=None):
        if accion == "agregar":
            query = "INSERT INTO mesero (cedula, nombre, telefono, direccion, email) VALUES (?, ?, ?, ?, ?)"
            params = (mesero.cedula, mesero.nombre, mesero.telefono, mesero.direccion, mesero.email)
            return db.hacerConsultas(query, params)
        elif accion == "eliminar":
            query = "DELETE FROM mesero WHERE cedula = ?"
            return db.hacerConsultas(query, (mesero.cedula,))
        return False

    def generar_informe(self, db, fecha=None):
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")

        inicio_dia = f"{fecha} 00:00:00"
        fin_dia = f"{fecha} 23:59:59"

        query = """
            SELECT COUNT(*) as cantidad, SUM(precio_total) as total 
            FROM comanda 
            WHERE fecha BETWEEN ? AND ?
        """
        db.hacerConsultas(query, (inicio_dia, fin_dia))
        resultado = db.comando.fetchone()
        if resultado:
            cantidad, total = resultado
            cantidad = cantidad or 0
            total = total or 0
            promedio = total / cantidad if cantidad > 0 else 0
            return {
                "fecha": fecha,
                "cantidad": cantidad,
                "total": total,
                "promedio": promedio
            }
        return None

class Mesero(Persona):
    def __init__(self, cedula, nombre, telefono=None, direccion=None, email=None):
        super().__init__(cedula, nombre, telefono, direccion, email)

    def guardarComanda(self, db, cedulaCliente, numeroMesa, platos):
        try:
            totalPrecio = sum(plato['precio'] * plato['cantidad'] for plato in platos)
            db.hacerConsultas(
                "INSERT INTO comanda (cedula_cliente, numero_mesa, precio_total) VALUES (?, ?, ?)",
                (cedulaCliente, numeroMesa, totalPrecio)
            )
            idComanda = db.cursor.lastrowid
            for insertPlatos in platos:
                db.hacerConsultas(
                    "INSERT INTO comanda_plato (comanda_id, plato_id, cantidad) VALUES (?, ?, ?)",
                    (idComanda, insertPlatos['id'], insertPlatos['cantidad'])
                )
            db.hacerConsultas(
                "UPDATE mesa SET estado = 'ocupada' WHERE numero = ?",
                (numeroMesa,)
            )
            return True
        except Exception as error:
            print(f"ERROR Al registrar la comanda: {error}")
            return False

    def camEstadoComanda (self, db, comandaid, nuevoeEstado):
        try:
            db.hacerConsultas(
                "UPDATE comanda SET estado = ? WHERE id = ?",
                (nuevoeEstado, comandaid)
            )
            if nuevoeEstado == 'servido':
                resultado = db.hacerConsultas(
                    "SELECT numero_mesa FROM comanda WHERE id = ?",
                    (comandaid,), resultado=True
                )
                if resultado:
                    numero_mesa = resultado[0][0]
                    db.hacerConsultas("UPDATE mesa SET estado = 'libre' WHERE numero = ?", (numero_mesa,))
            return True
        except Exception as error:
            print(f"ERROR Al cambiar estado de comanda {comandaid}: {error}")
            return False

class Cliente(Persona):
    def __init__(self, cedula, nombre, telefono=None, direccion=None, email=None, password=None):
        super().__init__(cedula, nombre, telefono, direccion, email)
        self.password = password

    def ver_comanda(self, db):
        guardar = """
            SELECT comanda1.id, comanda1.numero_mesa, comanda1.estado, plato.nombre, comPlato.cantidad
            FROM comanda comanda1
            JOIN comanda_plato comPlato ON comanda1.id = comPlato.comanda_id
            JOIN plato plato ON comPlato.plato_id = plato.id
            WHERE comanda1.cedula_cliente = ? AND comanda1.estado != 'servido'
        """
        resultados = db.hacerConsultas(guardar, (self.cedula,), resultado=True)
        if not resultados:
            return None
        idComanda, mesa, estado = resultados[0][:3]
        platos = [{"nombre": r[3], "cantidad": r[4]} for r in resultados]
        return {"comanda_id": idComanda, "mesa": mesa, "estado": estado, "platos": platos}

class Sistema:
    def __init__(self, db):
        self.db = db
        self.actualUsuario = None


class Mesa:
    def __init__(self, numero, estado):
        self.numero = numero
        self.estado = estado

class Plato:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

class Comanda:
    def __init__(self, id, cedula_cliente, numero_mesa, platos, precio_total, estado):
        self.id = id
        self.cedula_cliente = cedula_cliente
        self.numero_mesa = numero_mesa
        self.platos = platos
        self.precio_total = precio_total
        self.estado = estado

    @classmethod
    def obtener_por_id(objectFinal, db, comanda_id):
        consulta = """
            SELECT comanda1.cedula_cliente, comanda1.numero_mesa, comanda1.estado, platos.nombre, comanplato.cantidad, platos.precio
            FROM comanda comanda1
            JOIN comanda_plato comanplato ON comanda1.id = comanplato.comanda_id
            JOIN plato platos ON comanplato.plato_id = platos.id
            WHERE comanda1.id = ?
        """
        resultados = db.hacerConsultas(consulta, (comanda_id,), resultado=True)
        if not resultados:
            return None

        cedula_cliente, numero_mesa, estado = resultados[0][:3]
        platos = []
        for fila in resultados:
            platos.append({
                "nombre": fila[3],
                "cantidad": fila[4],
                "precio": fila[5]
            })

        total = sum(plato["cantidad"] * plato["precio"] for plato in platos)

        return objectFinal(
            id=comanda_id,
            cedula_cliente=cedula_cliente,
            numero_mesa=numero_mesa,
            platos=platos,
            precio_total=total,
            estado=estado
        )
