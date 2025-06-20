# Controllers/LogginFuncion.py

from tkinter import messagebox
from Views.VistaAdmin import AdminVista
from Views.VistaMesero import MeseroVista
from Views.VistaCliente import ClienteVista
import tkinter as tk

class FuncionesLogin:
    def __init__(self, interfaz, sistema):
        self.interfaz = interfaz  # Referencia a la clase de la vista (visual)
        self.sistema = sistema
        self.bandera = False

    def verCaracteres(self, event):
        if self.bandera:
            self.interfaz.entradaContraseña.config(show='*')
            self.interfaz.btnVer.config(text="Ver")
            self.bandera = False
        else:
            self.interfaz.entradaContraseña.config(show='')
            self.interfaz.btnVer.config(text="Ocultar")
            self.bandera = True

    def limpiarCampos(self, event=None):
        self.interfaz.entradaCedula.delete(0, tk.END)
        self.interfaz.entradaContraseña.delete(0, tk.END)

    def login(self):
        cedulaLoggin = self.interfaz.entradaCedula.get()
        contraseñaLoggin = self.interfaz.entradaContraseña.get()
        rolLoggin = self.interfaz.lista.get()

        if not cedulaLoggin or not contraseñaLoggin:
            messagebox.showerror("Error", " son obligatorios todos los camps")
            return

        if self.sistema.autenticar(cedulaLoggin, contraseñaLoggin, rolLoggin):
            self.interfaz.ventana.destroy()
            ventLoggin = tk.Tk()
            if rolLoggin == "administrador":
                AdminVista(ventLoggin, self.sistema)
            elif rolLoggin == "mesero":
                MeseroVista(ventLoggin, self.sistema)
            elif rolLoggin == "cliente":
                ClienteVista(ventLoggin, self.sistema)
            ventLoggin.mainloop()
        else:
            messagebox.showerror("Error datos  incorrectas")

    def mostrarAyuda(self, event):
        mensaje = (
            " INICIO DE SESION\n\n"
            "* Ingrese su numero de cedula en el primer campo.\n"
            "* Escriba su contraseña en el  segundo campo de.\n"
            "* Seleccione su rol (administrador/ mesero / cliente).\n\n"
            "* De forma opcional puede mantener el cursor sobre el botón (Ver) para mostrar la contraseña.\n"
            "* haga clic en el boton (Limpiar) Si desea borrar los campos ingresados.\n"
            "* Cuando haya ingresado todos los datos, presione 'Ingresar' para acceder al sistema.\n\n"
            "*Si tiene problemas con su acceso, verifique sus credenciales."
        )
        messagebox.showinfo("Ayuda", mensaje)
