# models/venta.py
from config.db_config import DB_CONFIG
import mysql.connector
from datetime import datetime

class Venta:
    @staticmethod
    def create(id_producto, cantidad, precio_venta, total, tipo_venta):
        """
        Registra una nueva venta.
        :param id_producto: ID del producto vendido
        :param cantidad: cantidad vendida (puede ser decimal para granel)
        :param precio_venta: precio unitario aplicado
        :param total: cantidad * precio_venta
        :param tipo_venta: 'unidad' o 'granel'
        """
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ventas (id_producto, cantidad, precio_venta, total, tipo_venta)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_producto, cantidad, precio_venta, total, tipo_venta))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        """Obtiene todas las ventas con información del producto."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, p.nombre AS producto, p.tipo 
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id
            ORDER BY v.fecha DESC
        """)
        ventas = cursor.fetchall()
        cursor.close()
        conn.close()
        return ventas

    @staticmethod
    def get_by_id(id_venta):
        """Obtiene una venta específica."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, p.nombre AS producto 
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id
            WHERE v.id = %s
        """, (id_venta,))
        venta = cursor.fetchone()
        cursor.close()
        conn.close()
        return venta

    @staticmethod
    def get_ventas_by_date(fecha_inicio=None, fecha_fin=None):
        """
        Obtiene ventas en un rango de fechas (formato: 'YYYY-MM-DD').
        Si no se pasan fechas, devuelve todas.
        """
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT v.*, p.nombre AS producto 
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id
            WHERE 1=1
        """
        params = []
        if fecha_inicio:
            query += " AND DATE(v.fecha) >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND DATE(v.fecha) <= %s"
            params.append(fecha_fin)
        query += " ORDER BY v.fecha DESC"

        cursor.execute(query, params)
        ventas = cursor.fetchall()
        cursor.close()
        conn.close()
        return ventas

    @staticmethod
    def total_ventas_hoy():
        """Devuelve la suma total de ventas del día actual."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas WHERE DATE(fecha) = CURDATE()")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return float(total)