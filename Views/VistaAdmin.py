import tkinter as tk
from tkinter import messagebox
from Controllers.AdminFuncion import FuncionesAdmin

class AdminVista:
    def __init__(self, root, sistema):
        # Configuración principal
        self.main_window = root
        self.sistema_restaurante = sistema
        self.controlador_funciones = FuncionesAdmin(self, sistema)

        self.main_window.title("Sistema de Comandas - Administrador")
        self.main_window.geometry("800x600")

        # Barra de menú superior
        self.menu_principal = tk.Menu(self.main_window)

        # Menú de gestión de meseros
        self.submenu_meseros = tk.Menu(self.menu_principal, tearoff=0)
        self.submenu_meseros.add_command(label="Registrar Mesero")
        self.submenu_meseros.add_command(label="Eliminar Mesero")
        self.menu_principal.add_cascade(label="Gestionar Meseros", menu=self.submenu_meseros)

        # Menú de informes
        self.submenu_informes = tk.Menu(self.menu_principal, tearoff=0)
        self.submenu_informes.add_command(label="Informe Diario")
        self.menu_principal.add_cascade(label="Informes", menu=self.submenu_informes)

        self.menu_principal.add_command(label="Salir")
        self.main_window.config(menu=self.menu_principal)

        # Frame contenedor principal
        self.contenedor_principal = tk.Frame(self.main_window, bd=2, relief=tk.GROOVE)
        self.contenedor_principal.place(x=20, y=20, width=760, height=560)

        # Etiqueta de título
        self.etiqueta_titulo = tk.Label(self.contenedor_principal, 
                                      text="Panel de Administración", 
                                      font=("Helvetica", 16))
        self.etiqueta_titulo.place(x=250, y=10)

        # Botones de navegación por pestañas
        self.boton_ver_meseros = tk.Button(self.contenedor_principal, text="Meseros")
        self.boton_ver_meseros.place(x=10, y=50, width=100, height=30)
        
        self.boton_ver_comandas = tk.Button(self.contenedor_principal, text="Comandas")
        self.boton_ver_comandas.place(x=120, y=50, width=100, height=30)

        # Frames de contenido
        self.frame_meseros = tk.Frame(self.contenedor_principal, bd=1, relief=tk.SUNKEN)
        self.frame_meseros.place(x=10, y=90, width=740, height=460)

        self.frame_comandas = tk.Frame(self.contenedor_principal, bd=1, relief=tk.SUNKEN)
        self.frame_comandas.place(x=10, y=90, width=740, height=460)

        # Botón de ayuda
        self.boton_ayuda = tk.Button(self.contenedor_principal, text="Ayuda")
        self.boton_ayuda.place(x=700, y=10, width=70, height=30)

        # Configuración de eventos
        self._configurar_eventos()

        # Mostrar vista inicial
        self.controlador_funciones.mostrar_meseros()
        self.controlador_funciones.cargar_meseros()
        self.controlador_funciones.cargar_comandas()

    def _configurar_eventos(self):
        """Configura todos los eventos de la interfaz"""
        # Eventos de menú
        self.submenu_meseros.entryconfig("Registrar Mesero", command=self.controlador_funciones.registrar_mesero)

        self.submenu_meseros.entryconfig("Eliminar Mesero",  command=self.controlador_funciones.eliminar_mesero)

        self.submenu_informes.entryconfig("Informe Diario", command=self.controlador_funciones.generar_informe)

        self.menu_principal.entryconfig("Salir", command=self.main_window.quit)

        # Eventos de botones
        self.boton_ver_meseros.bind("<Button-1>", lambda e: self.controlador_funciones.mostrar_meseros())

        self.boton_ver_comandas.bind("<Button-1>", lambda e: self.controlador_funciones.mostrar_comandas())
        
        self.boton_ayuda.bind("<Button-1>",  lambda e: self.controlador_funciones.mostrar_ayuda())