import tkinter as tk
from Models.datosbase import ConexionBD
from Controllers.controllers import SistemaRestaurante
from Views.Loggin import Login

def main():
    # Inicializar base de datos
    db = ConexionBD()

    # Inicializar sistema
    sistema = SistemaRestaurante(db)

    # Mostrar login
    root = tk.Tk()
    Login(root, sistema)
    root.mainloop()

    # Cerrar conexión al salir
    db.cerrarConexion()

if __name__ == "__main__":
    main()
