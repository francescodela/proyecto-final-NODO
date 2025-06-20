import mariadb
import sys
from datetime import datetime # borrar 

class ConexionBD:
    def __init__(self):
        try:
            self.conector = mariadb.connect(
                user="restaurante_user",
                password="restaurante_pass",
                host="localhost",
                port=3307,
                database="sistema_comandas"
            )
            self.comando = self.conector.cursor()
            self.crearTablas()
        except mariadb.Error as e:
            print(f"Error de conexion a  MariaDB: {e}")
            sys.exit(1)

    def crearTablas(self):
        try:
            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS administrador (
                    cedula VARCHAR(20) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    direccion VARCHAR(200),
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL DEFAULT 'admin123'
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS mesero (
                    cedula VARCHAR(20) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    direccion VARCHAR(200),
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL DEFAULT 'mesero123'
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    cedula VARCHAR(20) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    direccion VARCHAR(200),
                    email VARCHAR(100),
                    password VARCHAR(100) NOT NULL DEFAULT 'cliente123'
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS mesa (
                    numero INT PRIMARY KEY,
                    estado ENUM('libre', 'ocupada') DEFAULT 'libre'
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS plato (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    precio DECIMAL(10, 2) NOT NULL
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS comanda (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cedula_cliente VARCHAR(20) NOT NULL,
                    numero_mesa INT NOT NULL,
                    precio_total DECIMAL(10, 2) NOT NULL,
                    estado ENUM('pendiente', 'en preparacion', 'servido') DEFAULT 'pendiente',
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cedula_cliente) REFERENCES cliente(cedula),
                    FOREIGN KEY (numero_mesa) REFERENCES mesa(numero)
                )
            """)

            self.comando.execute("""
                CREATE TABLE IF NOT EXISTS comanda_plato (
                    comanda_id INT,
                    plato_id INT,
                    cantidad INT DEFAULT 1,
                    PRIMARY KEY (comanda_id, plato_id),
                    FOREIGN KEY (comanda_id) REFERENCES comanda(id),
                    FOREIGN KEY (plato_id) REFERENCES plato(id)
                )
            """)

            self.conector.commit()
        except mariadb.Error as error :
            print(f"Error al crera las tablas en MariaDB: {error }")

    def hacerConsultas(self, consulta, parametro =None, resultado=False):
        try:
            if parametro :
                self.comando.execute(consulta, parametro )
            else:
                self.comando.execute(consulta)

            if resultado:
                return self.comando.fetchall()
            self.conector.commit()
            return True
        except mariadb.Error as error :
            print(f"Error en la BD: {error}")
            return False

    def cerrarConexion(self):
        if hasattr(self, 'conector'):
            self.conector.close()
