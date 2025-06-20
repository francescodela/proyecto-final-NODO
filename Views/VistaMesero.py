
import tkinter as tk
from Models.models import Cliente
from Controllers.MeseroFuncion import MeseroFunciones
from tkinter import ttk
from tkinter import PhotoImage
from Views.tooltip  import Tooltip

class MeseroVista:

    def mostrarPanel(self, fame):
        try:
            self.PanelCliente.place_forget()
            self.PanelComanda.place_forget()
            fame.place(relx=0.05, rely=0.2, width=720, height=420)
        except Exception as e:
            print(f"Error al mostrar panel: {str(e)}")

    def eventMostrarPanelCliente(self, event):
        try:
            self.mostrarPanel(self.PanelCliente)
        except Exception as e:
            print(f"Error al mostrar panel de cliente: {str(e)}")

    def eventMostrarPanelComanda(self, event):
        try:
            self.mostrarPanel(self.PanelComanda)
        except Exception as e:
            print(f"Error al mostrar panel de comanda: {str(e)}")

    def mostrarClientesPanel(self, clientes):
        try:
            for celda in self.PanelCliente.winfo_children():
                celda.destroy()

            columnasDatos = ("Cedula", "Nombre", "Telefono", "Direccion", "Email")
            self.celddasCliente = ttk.Treeview(self.PanelCliente, columns=columnasDatos, show="headings")

            estiloEncabezado = ttk.Style()
            estiloEncabezado.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

            for columna in columnasDatos:
                self.celddasCliente.heading(columna, text=columna)
                self.celddasCliente.column(columna, anchor="center", width=120)

            self.celddasCliente.place(relx=0.5, rely=0.02, anchor="n", width=580, height=300)

            for cliente in clientes:
                self.celddasCliente.insert("", tk.END, values=(
                    cliente.cedula, cliente.nombre, cliente.telefono, cliente.direccion, cliente.email
                ))
        except Exception as e:
            print(f"Error al mostrar clientes: {str(e)}")

    def mostrarComandasTabla(self, comandas):
        try:
            for celda in self.PanelComanda.winfo_children():
                celda.destroy()

            encabezadoComandas = ("Id", "Cliente", "Mesa", "Precio Total", "Estado")
            self.celdasComandas = ttk.Treeview(self.PanelComanda, columns=encabezadoComandas, show="headings")

            estiloEncabezado = ttk.Style()
            estiloEncabezado.configure("Treeview.Heading", font=('arial', 10, 'bold'))

            for columnas in encabezadoComandas:
                self.celdasComandas.heading(columnas, text=columnas)
                self.celdasComandas.column(columnas, anchor="center", width=120)

            self.celdasComandas.place(relx=0.5, rely=0.02, anchor="n", width=580, height=300)

            for comanda in comandas:
                if not comanda:
                    continue
                self.celdasComandas.insert("", tk.END, values=(comanda.id, comanda.cedula_cliente, comanda.numero_mesa, f"${comanda.precio_total:2f}", comanda.estado))
        except Exception as e:
            print(f"Error al mostrar comandas: {str(e)}")
    
    def ventanaRegitroClientes(self, guardarClienteLlamdo):
        try:
            self.ventanaRegistro = tk.Toplevel(self.ventana)
            self.ventanaRegistro.title("registrar cliente")
            self.ventanaRegistro.geometry("400x300")

            self.fVentanaRegistro = tk.Frame(self.ventanaRegistro)
            self.fVentanaRegistro.place(relx=0, rely=0, width=400, height=300)

            self.lblTituloRegistro = tk.Label(self.fVentanaRegistro, text="Registrar Cliente", font=("Helvetica", 14))
            self.lblTituloRegistro.place(relx=0.3, rely=0.03)

            datosRegistro = ["Cedula", "Nombre", "Telefono", "Direccion", "Email", "Contraseña"]
            self.entries = {}
            alineacionEntrys = 50

            for campos in datosRegistro:
                self.lblCampo = tk.Label(self.fVentanaRegistro, text=campos)
                self.lblCampo.place(relx=0.05, rely=alineacionEntrys/300)
                
                mostrarContraseña = "*" if "Contraseña" in campos else None
                self.entrada = tk.Entry(self.fVentanaRegistro, show=mostrarContraseña)
                self.entrada.place(relx=0.3, rely=alineacionEntrys/300, width=200)
                self.entries[campos.lower()] = self.entrada
                alineacionEntrys += 30

            self.btnGuardarCliente = tk.Button(self.fVentanaRegistro, image=self.iconGuardar, command=guardarClienteLlamdo)
            self.btnGuardarCliente.place(relx=0.2, rely=0.8)
            ToolTip(self.btnGuardarCliente, "Guardar cliente (Ctrl+S)")
            
            self.btnCancelarRegistro = tk.Button(self.fVentanaRegistro, image=self.iconCancelar, command=self.ventanaRegistro.destroy)
            self.btnCancelarRegistro.place(relx=0.5, rely=0.8)
            ToolTip(self.btnCancelarRegistro, "Cancelar registro (Esc)")
        except Exception as e:
            print(f"Error al crear ventana de registro: {str(e)}")
     
    def ventanaComanda(self, clientes, mesas, platos, guardarCom):
        try:
            self.GuiComanda = tk.Toplevel(self.ventana)
            self.GuiComanda.title("Tomar Comanda")
            self.GuiComanda.geometry("600x500")

            self.frameComanda = tk.Frame(self.GuiComanda)
            self.frameComanda.place(relx=0, rely=0, width=600, height=500)

            self.lblTituloComanda = tk.Label(self.frameComanda, text="Tomar Comanda", font=("Helvetica", 14))
            self.lblTituloComanda.place(relx=0.3, rely=0.2)

            self.lblCliente = tk.Label(self.frameComanda, text="Cliente:")
            self.lblCliente.place(relx=0.3, rely=0.2)
            
            self.ingresoCliente = tk.StringVar()
            self.clienteMeun = tk.OptionMenu(self.frameComanda, self.ingresoCliente, "")
            self.clienteMeun.place(relx=0.2, rely=0.12, width=200)
            
            if clientes:
                self.ingresoCliente.set(f"{clientes[0].cedula} - {clientes[0].nombre}")
            menu = self.clienteMeun["menu"]
            menu.delete(0, "end")
            for c in clientes:
                menu.add_command(label=f"{c.cedula} - {c.nombre}",
                                 command=tk._setit(self.ingresoCliente, f"{c.cedula} - {c.nombre}"))

            self.lblMesa = tk.Label(self.frameComanda, text="Mesa:")
            self.lblMesa.place(relx=0.3, rely=0.2)
            
            self.datoMesa = tk.StringVar()
            self.mesaMenu = tk.OptionMenu(self.frameComanda, self.datoMesa, "")
            self.mesaMenu.place(relx=0.2, rely=0.2, width=200)
            
            if mesas:
                self.datoMesa.set(str(mesas[0].numero))
            menu = self.mesaMenu["menu"]
            menu.delete(0, "end")
            for m in mesas:
                menu.add_command(label=str(m.numero),
                                 command=tk._setit(self.datoMesa, str(m.numero)))

            self.lblPlatos = tk.Label(self.frameComanda, text="Platos:")
            self.lblPlatos.place(relx=0.033, rely=0.28)
            
            self.framePlatos = tk.Frame(self.frameComanda)
            self.framePlatos.place(relx=0.2, rely=0.28, width=400, height=200)
            self.datosPlatos = {}
            self.platosEleccion = {}

            for i, plato in enumerate(platos):
                dato = tk.IntVar(value=0)

                self.datosPlatos[plato.id] = dato
                var1 = i * 30
                self.selecMultiplePlatos = tk.Checkbutton(self.framePlatos, text=f"{plato.nombre} (${plato.precio:.2f})", variable=dato)
                                   
                self.selecMultiplePlatos.place(relx=0, rely=var1/200)

                self.elecVariosPlatos = tk.Spinbox(self.framePlatos, from_=1, to=10, width=3)
                self.elecVariosPlatos.place(relx=0.625, rely=var1/200)
                self.platosEleccion[plato.id] = self.elecVariosPlatos

            self.btnGuardarComanda = tk.Button(self.frameComanda, image=self.iconGuardar, command=guardarCom)
            self.btnGuardarComanda.place(relx=0.3, rely=0.8)
            ToolTip(self.btnGuardarComanda, "Guardar comanda")
            
            self.btnCancelarComanda = tk.Button(self.frameComanda, image=self.iconCancelar, command=self.GuiComanda.destroy)
            self.btnCancelarComanda.place(relx=0.5, rely=0.8)
            ToolTip(self.btnCancelarComanda, "Cancelar comanda")
        except Exception as e:
            print(f"Error al crear ventana de comanda: {str(e)}")

    def ventanaCambiarEstado(self, comanda_id, estadoActualizado, estados, llamado):
        try:
            self.ventanaEstado = tk.Toplevel(self.ventana)
            self.ventanaEstado.title("Cambiar Estado de Comanda")
            self.ventanaEstado.geometry("300x200")

            self.frameEstado = tk.Frame(self.ventanaEstado)
            self.frameEstado.place(width=300, height=200)

            self.lblComandaId = tk.Label(self.frameEstado, text=f"Comanda ID: {comanda_id}", font=("Helvetica", 14))
            self.lblComandaId.place(relx=0.25, rely=0.1)

            self.datosEstado = tk.StringVar(value=estadoActualizado)
            self.EstadoMenu = tk.OptionMenu(self.frameEstado, self.datosEstado, *estados)
            self.EstadoMenu.place(relx=0.266, rely=0.35, width=140)

            def cambios():
                try:
                    estadoActualizado = self.datosEstado.get()
                    llamado(estadoActualizado)
                except Exception as e:
                    print(f"Error al cambiar estado: {str(e)}")

            self.btnGuardarEstado = tk.Button(self.frameEstado, image=self.iconGuardar, command=cambios)
            self.btnGuardarEstado.place(relx=0.2, rely=0.7)
            ToolTip(self.btnGuardarEstado, "Guardar estado")
            
            self.btnCancelarEstado = tk.Button(self.frameEstado, image=self.iconCancelar, command=self.ventanaEstado.destroy)
            self.btnCancelarEstado.place(relx=0.5, rely=0.7)
            ToolTip(self.btnCancelarEstado, "Cancelar cambio")
        except Exception as e:
            print(f"Error al crear ventana de estado: {str(e)}")

    def obtenerCliente(self):
        try:
            obtener = self.celddasCliente.focus()

            if not obtener:
                return None, None
            datos = self.celddasCliente.item(obtener, 'values')

            return datos[0], datos[1]
        except Exception as e:
            print(f"Error al obtener cliente: {str(e)}")
            return None, None
    

    def MostrarMesasLibres(self, mesas):
        try:
            self.ventanaMesas = tk.Toplevel(self.ventana)
            self.ventanaMesas.title("mesas disponibles")
            self.ventanaMesas.geometry("300x400")

            self.frameMesas = tk.Frame(self.ventanaMesas)
            self.frameMesas.place(relx=0, rely=0, width=300, height=400)

            self.lblTituloMesas = tk.Label(self.frameMesas, text="Mesas disponibles", font=("Helvetica", 14))
            self.lblTituloMesas.place(relx=0.3, rely=0.025)

            if not mesas:
                self.lblNoMesas = tk.Label(self.frameMesas, text="No hay mesas disponibles")
                self.lblNoMesas.place(relx=0.3, rely=0.125)
                return

            organizador = 50
            for mesa in mesas:
                self.lblMesa = tk.Label(self.frameMesas, text=f"Mesa {mesa.numero}")
                self.lblMesa.place(relx=0.333, rely=organizador/400)
                organizador += 30
        except Exception as e:
            print(f"Error al mostrar mesas: {str(e)}")

    def hotkeys(self):
        try:
            # Hotkey para mostrar el panel de clientes (Ctrl + C)
            self.ventana.bind_all("<Control-c>", lambda event: self.eventMostrarPanelCliente(event))
            ToolTip(self.btnClientes, "Mostrar clientes (Ctrl+C)")

            # Hotkey para mostrar el panel de comandas (Ctrl + O)
            self.ventana.bind_all("<Control-o>", lambda event: self.eventMostrarPanelComanda(event))
            ToolTip(self.btnComandas, "Mostrar comandas (Ctrl+O)")

            # Hotkey para guardar cliente (Ctrl + S)
            self.ventana.bind_all("<Control-s>", lambda event: self.funciones.registrarClientes())

            # Hotkey para cancelar el registro de cliente (Esc)
            self.ventana.bind_all("<Escape>", lambda event: self.ventanaRegistro.destroy())

            # Hotkey para salir (Ctrl + Q)
            self.ventana.bind_all("<Control-q>", lambda event: self.ventana.quit())

            # Hotkey para cambiar estado de la comanda (Ctrl + E)
            self.ventana.bind_all("<Control-e>", lambda event: self.funciones.cambiarEstadoComanda())
        except Exception as e:
            print(f"Error al configurar hotkeys: {str(e)}")

    def __init__(self, ventana, sistema):
        try:
            self.ventana = ventana
            self.sistema = sistema
            self.ventana.title("Sistema de Comandas de Mesero")
            self.ventana.geometry("800x600")

            # Cargar íconos
            try:
                self.iconCliente = PhotoImage(file=r"cod moduladp2\src\icons\audiencia.png")
                self.iconComandas = PhotoImage(file=r"cod moduladp2\src\icons\ordenar-comida (1).png")
                self.iconGuardar = PhotoImage(file=r"cod moduladp2\src\icons\disk.png")
                self.iconCancelar = PhotoImage(file=r"cod moduladp2\src\icons\cancelar.png")
                self.iconMesa = PhotoImage(file=r"cod moduladp2\src\icons\cena.png")
                self.iconEstado = PhotoImage(file=r"cod moduladp2\src\icons\cambio.png")
                self.iconAyuda = PhotoImage(file=r"cod moduladp2\src\icons\informacion.png")
                self.iconComandaN = PhotoImage(file=r"cod moduladp2\src\icons\ordenar-comida.png")
                self.iconAgregarUsuario = PhotoImage(file=r"cod moduladp2\src\icons\user_add.png")
                self.iconEliminarUsuario = PhotoImage(file=r"cod moduladp2\src\icons\user_delete.png")
            except Exception as e:
                print(f"Error al cargar íconos: {str(e)}")

            self.funciones = MeseroFunciones(self, sistema)

            self.barraMenu = tk.Menu(self.ventana)

            self.menuClientes = tk.Menu(self.barraMenu, tearoff=0)
            self.menuClientes.add_command(image=self.iconAgregarUsuario, command=self.funciones.registrarClientes)
            self.menuClientes.add_command(image=self.iconEliminarUsuario, command=self.funciones.eliminarCliente)
            self.barraMenu.add_cascade(label="Clientes", menu=self.menuClientes)

            self.menuMesas = tk.Menu(self.barraMenu, tearoff=0)
            self.menuMesas.add_command(image=self.iconMesa, command=self.funciones.obtenerMesasLibres)
            self.barraMenu.add_cascade(label="Mesas", menu=self.menuMesas)

            self.menuComandas = tk.Menu(self.barraMenu, tearoff=0)
            self.menuComandas.add_command(image=self.iconComandaN, command=self.funciones.hacerComandas)
            self.menuComandas.add_command(image=self.iconEstado, command=self.funciones.cambiarEstadoComanda)
            self.barraMenu.add_cascade(label="Comandas", menu=self.menuComandas)

            self.barraMenu.add_command(label="ayuda", command=self.funciones.mostrarAyuda)
            self.barraMenu.add_command(label="Salir", command=self.ventana.quit)
            self.ventana.config(menu=self.barraMenu)

            self.framePrincipal = tk.Frame(self.ventana, bg="#f0f0f0")
            self.framePrincipal.place(relx=0, rely=0, width=800, height=600)

            self.titulo = tk.Label(self.framePrincipal, text="Mesero", font=("Helvetica", 16), bg="#f0f0f0")
            self.titulo.place(relx=0.5, rely=0.033, anchor="n")

            self.PanelCliente = tk.Frame(self.framePrincipal, bd=2, relief="groove")
            self.PanelComanda = tk.Frame(self.framePrincipal, bd=2, relief="groove")

            self.btnClientes = tk.Button(self.framePrincipal, image=self.iconCliente, width=60)
            self.btnClientes.place(relx=0.25, rely=0.1)
            self.btnClientes.bind("<Button-1>", self.eventMostrarPanelCliente)

            self.btnComandas = tk.Button(self.framePrincipal, image=self.iconComandas, width=60)
            self.btnComandas.place(relx=0.5, rely=0.1)
            self.btnComandas.bind("<Button-1>", self.eventMostrarPanelComanda)

            self.PanelCliente.place(relx=0.05, rely=0.18, width=720, height=420)
            self.PanelComanda.place(relx=0.05, rely=0.18, width=720, height=420)

            self.funciones.cargarClientesdeBD()
            self.funciones.cargarComandas()

            self.mostrarPanel(self.PanelCliente)
            self.hotkeys()
        except Exception as e:
            print(f"Error al inicializar la vista: {str(e)}")