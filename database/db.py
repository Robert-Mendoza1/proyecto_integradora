import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # 👈 Añadir esta línea

import mysql.connector
from mysql.connector import Error
from models.usuario import Usuario  



DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123580',  # 👈 Cambia por la tuya
    'database': 'tienda_granel'
}

def create_database():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS tienda_granel")
        print("✅ Base de datos 'tienda_granel' creada o ya existe.")
    except Error as e:
        print(f"❌ Error al crear DB: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_tables():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Tabla proveedores
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            contacto VARCHAR(50),
            telefono VARCHAR(20),
            email VARCHAR(50),
            direccion TEXT,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tabla productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(50) UNIQUE,
            nombre VARCHAR(50) NOT NULL,
            descripcion TEXT,
            tipo ENUM('unidad', 'granel') NOT NULL DEFAULT 'unidad',
            precio_unitario DECIMAL(10,2) NOT NULL,
            stock DECIMAL(10,3) NOT NULL DEFAULT 0.000,
            stock_bajo DECIMAL(10,3) NOT NULL DEFAULT 5.000,  -- ✅ Nuevo campo
            id_proveedor INT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id) ON DELETE SET NULL
        )
        """)

        # Tabla compras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_producto INT NOT NULL,
            id_proveedor INT,
            cantidad DECIMAL(10,3) NOT NULL,
            precio_compra DECIMAL(10,2) NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            nota TEXT,
            FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id) ON DELETE SET NULL
        )
        """)

        # Tabla ventas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_producto INT NOT NULL,
            cantidad DECIMAL(10,3) NOT NULL,
            precio_venta DECIMAL(10,2) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            tipo_venta ENUM('unidad', 'granel') NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
        )
        """)

        # Tabla usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(10) UNIQUE NOT NULL,
            nombre_completo VARCHAR(50) NOT NULL,
            contrasena_hash VARCHAR(255) NOT NULL,
            rol ENUM('admin', 'vendedor') NOT NULL DEFAULT 'vendedor',
            estatus ENUM('activo', 'inactivo', 'pendiente') NOT NULL DEFAULT 'pendiente',
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            activo BOOLEAN DEFAULT TRUE
        )
        """)

        connection.commit()
        print("✅ Tablas creadas correctamente.")

    except Error as e:
        print(f"❌ Error al crear tablas: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def crear_usuario_admin():
    """Crea un usuario admin por defecto si no existe."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Verificar si ya existe un usuario admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'admin'")
        count = cursor.fetchone()[0]

        if count == 0:
            # Crear usuario admin por defecto
            nombre_usuario = "admin"
            nombre_completo = "Administrador del Sistema"
            contrasena = "admin123"  # 👈 Contraseña por defecto
            rol = "admin"
            
            contrasena_hash = Usuario.hash_contrasena(contrasena)
            
            cursor.execute("""
                INSERT INTO usuarios (nombre_usuario, nombre_completo, contrasena_hash, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre_usuario, nombre_completo, contrasena_hash, rol))
            
            connection.commit()
            print(f"✅ Usuario admin creado: {nombre_usuario} / {contrasena}")
        else:
            print("ℹ️ Ya existe al menos un usuario admin. No se creó ninguno nuevo.")

    except Error as e:
        print(f"❌ Error al crear usuario admin: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    crear_usuario_admin()  # 👈 Nueva función
    
    
## Consulta para activar un usuario existente    
#""" UPDATE usuarios 
#SET estatus = 'activo' 
#WHERE nombre_usuario = 'admin';
#"""