# CODIGO MODIFICADO DEL ANTERIOR (18/06 HORA ( 9:27 AM ) ESTA FUNCIONAL SIN ERRORES 
import tkinter as tk
from Controllers.ClienteFuncion import ClienteFunciones

class ClienteVista:
    def __init__(self, ventana, sistema):
        self.ventana = ventana
        self.sistema = sistema
        self.funciones = ClienteFunciones(self, sistema)

        self.ventana.title("Cliente - Estado de Mi Comanda")
        self.ventana.geometry("500x400")

        frame = tk.Frame(self.ventana)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        label = tk.Label(frame, text=f"Hola {self.sistema.actualUsuario.nombre}", font=("Helvetica", 16))
        label.place(relx=0.5, y=30, anchor="center")

        self.text = tk.Text(frame, height=15, state="disabled", font=("Courier", 10))
        self.text.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.5, anchor="n")

        btns = tk.Frame(frame, width=200, height=40)
        btns.place(relx=0.5, rely=0.82, anchor="n")

        btn_actualizar = tk.Button(btns, text="Actualizar")
        btn_actualizar.place(x=0, y=0)
        btn_actualizar.bind("<Button-1>", self.funciones.actualizar)

        btn_salir = tk.Button(btns, text="Salir")
        btn_salir.place(x=100, y=0)
        btn_salir.bind("<Button-1>", self.funciones.salir)

        btn_ayuda = tk.Button(frame, text="Ayuda")
        btn_ayuda.place(relx=1.0, y=5, anchor="ne")
        btn_ayuda.bind("<Button-1>", self.funciones.mostrar_ayuda)

        self.funciones.actualizar()
