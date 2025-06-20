import tkinter as tk
from Controllers.LogginFuncion import FuncionesLogin

class Login:
    def __init__(self, ventana, sistema):
        self.ventana = ventana
        self.sistema = sistema
        self.ventana.title("Sistema de Comandas ")
        self.ventana.geometry("600x500")
        self.ventana.resizable(False, False)

        # Instancia de funciones
        self.funciones = FuncionesLogin(self, sistema)

        # Título
        self.lbltitulo = tk.Label(self.ventana, text="Inicio de Sesion", font=("Helvetica", 16))
        self.lbltitulo.place(x=220, y=30)

        # Cédula
        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(x=150, y=100)
        self.entradaCedula = tk.Entry(self.ventana)
        self.entradaCedula.place(x=250, y=100, width=200)

        # Contraseña
        self.lblContrseña = tk.Label(self.ventana, text="Contraseña:")
        self.lblContrseña.place(x=150, y=150)
        self.entradaContraseña = tk.Entry(self.ventana, show="*")
        self.entradaContraseña.place(x=250, y=150, width=200)

        # Rol
        self.lblRol = tk.Label(self.ventana, text="Rol:")
        self.lblRol.place(x=150, y=200)
        self.lista = tk.StringVar(self.ventana)
        self.lista.set("administrador")
        self.menu = tk.OptionMenu(self.ventana, self.lista, "administrador", "mesero", "cliente")
        self.menu.place(x=250, y=200, width=200)

        # Botón Ingresar (redirigido)
        self.btnLogin = tk.Button(self.ventana, text="Ingresar", command=self.funciones.login)
        self.btnLogin.place(x=250, y=250, width=100)

        # Botón Ver/Ocultar contraseña (redirigido)
        self.btnVer = tk.Button(self.ventana, text="Ver")
        self.btnVer.place(x=460, y=150, width=40, height=25)
        self.btnVer.bind("<Button-1>", self.funciones.verCaracteres)
        self.btnVer.bind("<Leave>", self.funciones.verCaracteres)

        # Botón Limpiar (redirigido)
        self.btnLimpiar = tk.Button(self.ventana, text="Limpiar")
        self.btnLimpiar.place(x=250, y=290, width=100)
        self.btnLimpiar.bind("<Button-1>", self.funciones.limpiarCampos)

        # Botón Ayuda (redirigido)
        self.btnAyuda = tk.Button(self.ventana, text="Ayuda")
        self.btnAyuda.place(x=500, y=30)
        self.btnAyuda.bind("<Button-1>", self.funciones.mostrarAyuda)
