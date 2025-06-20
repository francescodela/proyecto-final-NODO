import tkinter as tk
from tkinter import messagebox


class ClienteFunciones:
    def __init__(self, vista, sistema):
        self.vista = vista
        self.sistema = sistema

    def actualizar(self,event=None):
        self.vista.text.configure(state="normal")
        self.vista.text.delete("1.0", tk.END)

        obtener = self.sistema.actualUsuario.ver_comanda(self.sistema.db)
        if not obtener:
            self.vista.text.insert(tk.END, "No tienes ninguna comanda activa.\n")
        else:
            self.vista.text.insert(tk.END, f" Comanda Numero: {obtener['comanda_id']}\n")
            self.vista.text.insert(tk.END, f" Mesa: {obtener['mesa']}\n")
            self.vista.text.insert(tk.END, f" Estado: {obtener['estado'].capitalize()}\n\n")

            self.vista.text.insert(tk.END, " Platos:\n")
            total = 0
            for p in obtener["platos"]:
                resultado = self.sistema.db.execute_query(
                    "SELECT precio FROM plato WHERE nombre = ?",
                    (p["nombre"],),
                    resultado=True
                )
                precio_unitario = resultado[0][0] if resultado else 0
                subtotal = precio_unitario * p["cantidad"]
                total += subtotal
                self.vista.text.insert(tk.END, f"  • {p['nombre']} x {p['cantidad']}  -  ${subtotal:,.2f}\n")

            self.vista.text.insert(tk.END, f"\n Total: ${total:,.2f}\n")
            if obtener["estado"] == "servido":
                self.vista.text.insert(tk.END, "\n Gracias por su compra. ¡Buen provecho!\n")

        self.vista.text.configure(state="disabled")

    def mostrar_ayuda(self, event=None):
        messagebox.showinfo(
            "Ayuda",
            
            "* Presiona 'Actualizar' para obtener el estado .\n"
            "* Presiona 'Salir' para cerrar la ventana.\n")

    def salir(self, event=None):
        self.vista.ventana.quit()