# models/proveedor.py
from config.db_config import DB_CONFIG
import mysql.connector

class Proveedor:
    @staticmethod
    def get_all():
        """Obtiene todos los proveedores ordenados por nombre."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
        proveedores = cursor.fetchall()
        cursor.close()
        conn.close()
        return proveedores

    @staticmethod
    def get_by_id(id_proveedor):
        """Obtiene un proveedor por su ID."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proveedores WHERE id = %s", (id_proveedor,))
        proveedor = cursor.fetchone()
        cursor.close()
        conn.close()
        return proveedor

    @staticmethod
    def create(nombre, contacto=None, telefono=None, email=None, direccion=None):
        """Crea un nuevo proveedor. Retorna el ID insertado."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO proveedores (nombre, contacto, telefono, email, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, contacto, telefono, email, direccion))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(id_proveedor, nombre, contacto=None, telefono=None, email=None, direccion=None):
        """Actualiza un proveedor existente."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s, contacto = %s, telefono = %s, email = %s, direccion = %s
            WHERE id = %s
        """, (nombre, contacto, telefono, email, direccion, id_proveedor))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(id_proveedor):
        """Elimina un proveedor. Las referencias en productos/compras se manejan con ON DELETE SET NULL."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id = %s", (id_proveedor,))
        conn.commit()
        cursor.close()
        conn.close()