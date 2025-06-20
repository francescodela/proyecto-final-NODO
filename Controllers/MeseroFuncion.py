import tkinter as tk
from tkinter import messagebox
from Models.models import Cliente

class MeseroFunciones:
    def __init__(self, vista, sistema):
        self.vista = vista
        self.sistema = sistema
    
    def cargarClientesdeBD(self):
        clientes = self.sistema.obtenerClientes()
        self.vista.mostrarClientesPanel(clientes)
    
    def cargarComandas(self):
        comandas = self.sistema.obtenerComandas()
        self.vista.mostrarComandasTabla(comandas)

    def registrarClientes(self):
        self.vista.ventanaRegitroClientes (self.guardarCliente)

    
    def hacerComandas(self):
        clientes = self.sistema.obtenerClientes()
        mesas = self.sistema.obtenerMesas(estado='libre')
        platos = self.sistema.obtenerPlatos()
        self.vista.ventanaComanda(clientes, mesas, platos, self.guardarComandaBD)

    def eliminarCliente(self):
        cedula, nombre = self.vista.obtenerCliente()
        
        if not cedula:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar cliente {nombre}?")

        if confirmar:
            if self.sistema.db.hacerConsultas("DELETE FROM cliente WHERE cedula = ?", (cedula,)):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargarClientesdeBD()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")

    def obtenerMesasLibres(self):
        mesas = self.sistema.obtenerMesas(estado='libre')
        self.vista.MostrarMesasLibres(mesas)
    
    def guardarCliente(self):
        datos = {key: entry.get() for key, entry in self.vista.entries.items()}

        if not datos.get('cedula') or not datos.get('nombre') or not datos.get('contraseña'):
            messagebox.showerror("Error", "Cedula, nombre y contraseña son obligatorios")
            return

        cliente = Cliente(
            cedula=datos['cedula'],
            nombre=datos['nombre'],
            telefono=datos.get('telefono', ''),
            direccion=datos.get('dirección', ''),
            email=datos.get('email', '')
        )
        password = datos['contraseña']

        if self.sistema.db.hacerConsultas(
            "INSERT INTO cliente (cedula, nombre, telefono, direccion, email, password) VALUES (?, ?, ?, ?, ?, ?)",
            (cliente.cedula, cliente.nombre, cliente.telefono, cliente.direccion, cliente.email, password)
        ):
            messagebox.showinfo( "Cliente registrado correctamente")
            self.vista.ventanaRegistro.destroy()
            self.cargarClientesdeBD()
        else:
            messagebox.showerror("Error", "No se pudo registrar el cliente")

    def tomar_comanda(self):
        clientes = self.sistema.obtenerClientes()
        mesas = self.sistema.obtenerMesas(estado='libre')
        platos = self.sistema.obtenerPlatos()
        
        self.vista.ventanaComanda(clientes, mesas, platos, self.guardarComanda)

    def cambiarEstadoComanda(self):
        selected = self.vista.celdasComandas .focus()
        if not selected:
            messagebox.showerror("Error", "Seleccione una comanda para cambiar estado")
            return

        datos = self.vista.celdasComandas .item(selected, 'values')
        comanda_id = datos[0]
        numero_mesa = datos[2]
        estadoActualizado = datos[4]

        estados_posibles = ["pendiente", "En preparación", "servido"]

        # Llama a la vista para mostrar la ventana y pasar el callback
        self.vista.ventanaCambiarEstado(
            comanda_id=comanda_id,
            estadoActualizado=estadoActualizado,
            estados=estados_posibles,
            llamado=lambda nuevo_estado: self.guaradarEstadoComanda(comanda_id, numero_mesa, estadoActualizado, nuevo_estado)
        )


    def guaradarEstadoComanda(self, comanda_id, numero_mesa, estadoActualizado, nuevo_estado):
        if nuevo_estado == estadoActualizado:
            messagebox.showinfo("Info", "No se cambió el estado")
            self.vista.ventanaEstado.destroy()
            return

        try:
            cur = self.sistema.db.conector.cursor()
            cur.execute("UPDATE comanda SET estado = ? WHERE id = ?", (nuevo_estado, comanda_id))
            if nuevo_estado == "servido":
                cur.execute("UPDATE mesa SET estado = ? WHERE numero = ?", ("libre", numero_mesa))

            self.sistema.db.conector.commit()
            messagebox.showinfo("Éxito", "Estado actualizado")
            self.vista.ventanaEstado.destroy()
            self.cargarComandas()
        except Exception as e:
            self.sistema.db.conector.rollback()
            messagebox.showerror("Error", f"No se pudo actualizar el estado\n{e}")

    def guardarComandaBD(self):
        cliente_str = self.vista.ingresoCliente.get()
        cedula_cliente = cliente_str.split(" - ")[0] if cliente_str else None
        mesa = self.vista.datoMesa.get()

        if not mesa:
            messagebox.showerror("Error", "Seleccione una mesa")
            return

        mesa = int(mesa)

        platos = []
        for plato_id, var in self.vista.datosPlatos.items():
            if var.get():
                spin = self.vista.platosEleccion.get(plato_id)
                if spin:
                    cantidad = int(spin.get())
                    platos.append({"id": plato_id, "cantidad": cantidad})

        if not platos:
            messagebox.showerror("Error", "Seleccione al menos un plato")
            return

        platos_con_precio = []
        for plato in platos:
            resultado = self.sistema.db.hacerConsultas(
                "SELECT precio FROM plato WHERE id = ?",
                (plato['id'],),
                resultado=True
            )
            if resultado:
                precio = resultado[0][0]
                platos_con_precio.append((plato['id'], plato['cantidad'], precio))

        precio_total = sum(cantidad * precio for _, cantidad, precio in platos_con_precio)

        try:
            cur = self.sistema.db.conector.cursor()
            cur.execute(
                "INSERT INTO comanda (cedula_cliente, numero_mesa, precio_total, estado) VALUES (?, ?, ?, ?)",
                (cedula_cliente, mesa, precio_total, "pendiente")
            )
            comanda_id = cur.lastrowid

            for plato_id, cantidad, _ in platos_con_precio:
                cur.execute(
                    "INSERT INTO comanda_plato (comanda_id, plato_id, cantidad) VALUES (?, ?, ?)",
                    (comanda_id, plato_id, cantidad)
                )

            cur.execute("UPDATE mesa SET estado = ? WHERE numero = ?", ("ocupada", mesa))

            self.sistema.db.conector.commit()
            messagebox.showinfo("Éxito", "Comanda guardada correctamente")
            self.vista.GuiComanda.destroy()
            self.cargarComandas()

        except Exception as e:
            self.sistema.db.conector.rollback()
            messagebox.showerror("Error", f"No se pudo guardar la comanda\n{e}")


    def mostrarAyuda(self):
        # Opción 1: ventana emergente con messagebox
        message = (
            "Sistema de Comandas para Meseros.\n\n"
            "Usted puede :\n"
            "* Registrar y eliminar clientes.\n"
            "* Ver mesas libres.\n"
            "* Tomar y gestionar comandas.\n"
            "* Cambiar estado de comandas.\n\n")
        messagebox.showinfo("Ayuda ", message)

