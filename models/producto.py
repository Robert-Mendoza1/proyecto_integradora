# models/producto.py
from config.db_config import DB_CONFIG
import mysql.connector
from decimal import Decimal

class Producto:
    @staticmethod
    def get_all():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, pr.nombre AS proveedor 
            FROM productos p 
            LEFT JOIN proveedores pr ON p.id_proveedor = pr.id
            ORDER BY p.nombre
        """)
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return productos

    @staticmethod
    def create(codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO productos (codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(id, codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos 
            SET codigo=%s, nombre=%s, descripcion=%s, tipo=%s, 
                precio_unitario=%s, stock=%s, id_proveedor=%s
            WHERE id=%s
        """, (codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor, id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_id(id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
        return producto

    @staticmethod
    def actualizar_stock(id_producto, nueva_cantidad):
        """Actualiza el stock. Acepta int, float o Decimal."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        try:
            # Convertir a Decimal para evitar errores
            if not isinstance(nueva_cantidad, Decimal):
                nueva_cantidad = Decimal(str(nueva_cantidad))
            
            cursor.execute(
                "UPDATE productos SET stock = %s WHERE id = %s", 
                (nueva_cantidad, id_producto)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()