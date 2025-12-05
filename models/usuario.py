# models/usuario.py
from config.db_config import DB_CONFIG
import mysql.connector
import hashlib

class Usuario:
    @staticmethod
    def hash_contrasena(contrasena):
        """Hashea la contraseña con SHA-256."""
        return hashlib.sha256(contrasena.encode()).hexdigest()

    @staticmethod
    def crear_usuario(nombre_usuario, nombre_completo, contrasena, rol='vendedor'):
        """Crea un nuevo usuario con estatus 'pendiente'."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            contrasena_hash = Usuario.hash_contrasena(contrasena)
            cursor.execute("""
                INSERT INTO usuarios (nombre_usuario, nombre_completo, contrasena_hash, rol, estatus)
                VALUES (%s, %s, %s, %s, 'pendiente')
            """, (nombre_usuario, nombre_completo, contrasena_hash, rol))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def validar_credenciales(nombre_usuario, contrasena):
        """Valida credenciales y devuelve info del usuario o None."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        contrasena_hash = Usuario.hash_contrasena(contrasena)
        cursor.execute("""
            SELECT id, nombre_usuario, nombre_completo, rol
            FROM usuarios
            WHERE nombre_usuario = %s AND contrasena_hash = %s AND estatus = 'activo' AND activo = TRUE
        """, (nombre_usuario, contrasena_hash))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios (solo para admins)."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre_usuario, nombre_completo, rol, estatus, activo FROM usuarios ORDER BY estatus, rol, nombre_completo")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios

    @staticmethod
    def eliminar_usuario(id_usuario):
        """Elimina un usuario (soft delete)."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # ✅ Cambiar estatus a 'inactivo' en lugar de solo cambiar 'activo'
        cursor.execute("UPDATE usuarios SET activo = FALSE, estatus = 'inactivo' WHERE id = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()

    # ✅ Nuevos métodos para manejar estatus
    @staticmethod
    def aprobar_usuario(id_usuario):
        """Aprobar usuario (cambiar estatus a 'activo')."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET estatus = 'activo' WHERE id = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def rechazar_usuario(id_usuario):
        """Rechazar usuario (cambiar estatus a 'inactivo')."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET estatus = 'inactivo' WHERE id = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def reactivar_usuario(id_usuario):
        """Reactivar usuario (cambiar estatus a 'activo')."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET estatus = 'activo' WHERE id = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_usuarios_pendientes():
        """Obtiene usuarios con estatus 'pendiente'."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre_usuario, nombre_completo, rol, fecha_registro FROM usuarios WHERE estatus = 'pendiente' ORDER BY fecha_registro")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    
    @staticmethod
    def actualizar_usuario(id_usuario, nombre_usuario=None, nombre_completo=None, rol=None):
        """Actualizar datos de un usuario (menos contraseña)."""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        updates = []
        params = []

        if nombre_usuario is not None:
            updates.append("nombre_usuario = %s")
            params.append(nombre_usuario)
        if nombre_completo is not None:
            updates.append("nombre_completo = %s")
            params.append(nombre_completo)
        if rol is not None:
            updates.append("rol = %s")
            params.append(rol)

        if updates:
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s"
            params.append(id_usuario)
            cursor.execute(query, params)
            conn.commit()

        cursor.close()
        conn.close()