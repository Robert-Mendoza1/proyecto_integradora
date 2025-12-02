# models/compra.py
from config.db_config import DB_CONFIG
import mysql.connector
from models.producto import Producto

class Compra:
    @staticmethod
    def create(id_producto, id_proveedor, cantidad, precio_compra, nota=None):
        """
        Registra una compra (entrada de inventario).
        Actualiza automáticamente el stock del producto.
        """
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            # Registrar la compra
            cursor.execute("""
                INSERT INTO compras (id_producto, id_proveedor, cantidad, precio_compra, nota)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_producto, id_proveedor, cantidad, precio_compra, nota))
            
            # Actualizar stock del producto
            cursor.execute("""
                UPDATE productos 
                SET stock = stock + %s 
                WHERE id = %s
            """, (cantidad, id_producto))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        """Obtiene todas las compras con info de producto y proveedor."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, 
                   p.nombre AS producto, 
                   pr.nombre AS proveedor
            FROM compras c
            LEFT JOIN productos p ON c.id_producto = p.id
            LEFT JOIN proveedores pr ON c.id_proveedor = pr.id
            ORDER BY c.fecha DESC
        """)
        compras = cursor.fetchall()
        cursor.close()
        conn.close()
        return compras

    @staticmethod
    def get_by_id(id_compra):
        """Obtiene una compra específica."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, 
                   p.nombre AS producto, 
                   pr.nombre AS proveedor
            FROM compras c
            LEFT JOIN productos p ON c.id_producto = p.id
            LEFT JOIN proveedores pr ON c.id_proveedor = pr.id
            WHERE c.id = %s
        """, (id_compra,))
        compra = cursor.fetchone()
        cursor.close()
        conn.close()
        return compra

    @staticmethod
    def get_compras_by_proveedor(id_proveedor):
        """Obtiene todas las compras de un proveedor específico."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, p.nombre AS producto
            FROM compras c
            JOIN productos p ON c.id_producto = p.id
            WHERE c.id_proveedor = %s
            ORDER BY c.fecha DESC
        """, (id_proveedor,))
        compras = cursor.fetchall()
        cursor.close()
        conn.close()
        return compras