

from tkinter import ttk, messagebox, Toplevel
from Models.models import Mesero
import tkinter as tk

class FuncionesAdmin:
    def __init__(self, vista, sistema):
        self.vista = vista  # referencia a AdminView
        self.sistema = sistema

    def guardar_mesero(self):
        datos = {key: entry.get() for key, entry in self.vista.entries.items()}
        if not datos['cedula'] or not datos['nombre'] or not datos['email'] or not datos['password']:
            messagebox.showerror("Error", "Cédula, nombre, email y contraseña son obligatorios")
            return
        mesero = Mesero(
            cedula=datos['cedula'],
            nombre=datos['nombre'],
            telefono=datos['telefono'],
            direccion=datos['direccion'],
            email=datos['email']
        )
        password = datos['password']
        if self.sistema.db.hacerConsultas(
            "INSERT INTO mesero (cedula, nombre, telefono, direccion, email, password) VALUES (?, ?, ?, ?, ?, ?)",
            (mesero.cedula, mesero.nombre, mesero.telefono, mesero.direccion, mesero.email, password)
        ):
            messagebox.showinfo("Éxito", "Mesero registrado correctamente")
            self.vista.registro_window.destroy()
            self.cargar_meseros()
        else:
            messagebox.showerror("Error", "No se pudo registrar el mesero")

    def eliminar_mesero(self):
        selected = self.vista.meseros_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Seleccione un mesero para eliminar")
            return
        datos = self.vista.meseros_tree.item(selected, 'values')
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar mesero {datos[1]}?")
        if confirmar and self.sistema.db.hacerConsultas("DELETE FROM mesero WHERE cedula = ?", (datos[0],)):
            messagebox.showinfo("Éxito", "Mesero eliminado correctamente")
            self.cargar_meseros()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el mesero")

    def generar_informe(self):
        informe = self.sistema.generarInformeAdministrador()
        if not informe:
            messagebox.showerror("Error", "No se pudo generar el informe")
            return
        informe_window = Toplevel(self.vista.root)
        informe_window.title("Informe Diario")
        informe_window.geometry("300x250")
        frame = ttk.Frame(informe_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Informe Diario", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)
        ttk.Label(frame, text=f"Fecha: {informe['fecha']}").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=f"Comandas: {informe['cantidad']}").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=f"Total: ${informe['total']:,.2f}").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=f"Promedio: ${informe['promedio']:,.2f}").grid(row=4, column=0, sticky=tk.W)
        ttk.Button(frame, text="Cerrar", command=informe_window.destroy).grid(row=5, column=0, pady=10)

    def cargar_meseros(self):
        for widget in self.vista.meseros_frame.winfo_children():
            widget.destroy()
        meseros = self.sistema.obtenerMeseros()
        columns = ("Cédula", "Nombre", "Teléfono", "Dirección", "Email")
        self.vista.meseros_tree = ttk.Treeview(self.vista.meseros_frame, columns=columns, show="headings")
        for col in columns:
            self.vista.meseros_tree.heading(col, text=col)
            self.vista.meseros_tree.column(col, width=120)
        for mesero in meseros:
            self.vista.meseros_tree.insert("", tk.END, values=(
                mesero.cedula, mesero.nombre, mesero.telefono, mesero.direccion, mesero.email
            ))
        self.vista.meseros_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_comandas(self):
        for widget in self.vista.comandas_frame.winfo_children():
            widget.destroy()
        comandas = self.sistema.obtenerComandas()
        columns = ("ID", "Cliente", "Mesa", "Total", "Estado")
        self.vista.comandas_tree = ttk.Treeview(self.vista.comandas_frame, columns=columns, show="headings")
        for col in columns:
            self.vista.comandas_tree.heading(col, text=col)
            self.vista.comandas_tree.column(col, width=120)
        for comanda in comandas:
            if comanda is None:
                continue
            self.vista.comandas_tree.insert("", tk.END, values=(
                comanda.id, comanda.cedula_cliente, comanda.numero_mesa,
                f"${comanda.precio_total:,.2f}", comanda.estado
            ))
        self.vista.comandas_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def registrar_mesero(self):
        self.vista.registro_window = tk.Toplevel(self.vista.root)
        self.vista.registro_window.title("Registrar Mesero")
        self.vista.registro_window.geometry("400x300")
        frame = ttk.Frame(self.vista.registro_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Registrar Mesero", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        fields = ["cedula", "nombre", "telefono", "direccion", "email", "password"]
        self.vista.entries = {}
        for i, field in enumerate(fields, start=1):
            ttk.Label(frame, text=field.capitalize() + ":").grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame, show="*" if field == "password" else None)
            entry.grid(row=i, column=1, sticky=tk.EW, pady=5)
            self.vista.entries[field] = entry

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_mesero).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.vista.registro_window.destroy).pack(side=tk.LEFT, padx=5)
        frame.columnconfigure(1, weight=1)

    def mostrar_meseros(self):
        self.vista.meseros_frame.lift()

    def mostrar_comandas(self):
        self.vista.comandas_frame.lift()

    def mostrar_ayuda(self, event=None):
        ventana_ayuda = tk.Toplevel(self.vista.root)
        ventana_ayuda.title("Ayuda - Meseros")
        ventana_ayuda.geometry("400x250")

        mensaje = (
            "* Para registrar un mesero, haz clic en 'Registrar'.\n"
            "* Para eliminar   selecciona un mesero en la lista y presiona 'Eliminar'.\n"
            "* Podes ver la lista completa de meseros en el panel.\n"
            "* Asegúrate de llenar todos los campos correctamente.\n"
        )

        label = tk.Label(ventana_ayuda, text=mensaje, justify="left", wraplength=380, padx=10, pady=10)
        label.pack(fill="both", expand=True)

        cerrar_btn = tk.Button(ventana_ayuda, text="Cerrar", command=ventana_ayuda.destroy)
        cerrar_btn.pack(pady=10)
