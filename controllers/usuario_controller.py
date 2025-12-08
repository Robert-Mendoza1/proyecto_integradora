# controllers/usuario_controller.py
from models.usuario import Usuario
from config.db_config import DB_CONFIG
import mysql.connector

class UsuarioController:
    @staticmethod
    def crear_usuario(nombre_usuario, nombre_completo, contrasena, rol='vendedor'):
        """Crea un nuevo usuario con validaciones."""
        if not nombre_usuario or len(nombre_usuario) < 3:
            return False, "❌ Nombre de usuario debe tener al menos 3 caracteres.", None
        if not nombre_completo or len(nombre_completo) < 3:
            return False, "❌ Nombre completo es obligatorio.", None
        if not contrasena or len(contrasena) < 4:
            return False, "❌ Contraseña debe tener al menos 4 caracteres.", None
        if rol not in ['admin', 'vendedor']:
            return False, "❌ Rol inválido.", None

        try:
            id_usuario = Usuario.crear_usuario(nombre_usuario, nombre_completo, contrasena, rol)
            return True, "✅ Usuario registrado. Esperando aprobación del administrador.", id_usuario
        except Exception as e:
            return False, f"❌ Error al crear usuario: {str(e)}", None

    @staticmethod
    def validar_login(nombre_usuario, contrasena):
        """Valida login y devuelve datos del usuario."""
        if not nombre_usuario or not contrasena:
            return False, "❌ Usuario y contraseña son obligatorios.", None

        usuario = Usuario.validar_credenciales(nombre_usuario, contrasena)
        if usuario:
            return True, "✅ Login exitoso.", usuario
        else:
            # Verificar si el usuario existe pero está pendiente
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT estatus FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                if resultado['estatus'] == 'pendiente':
                    return False, "⚠️ Tu cuenta está pendiente de aprobación por el administrador.", None
                elif resultado['estatus'] == 'inactivo':
                    return False, "❌ Tu cuenta ha sido rechazada.", None
                else:
                    return False, "❌ Usuario o contraseña incorrectos.", None
            else:
                return False, "❌ Usuario o contraseña incorrectos.", None

    @staticmethod
    def listar_usuarios():
        """Obtiene todos los usuarios."""
        try:
            return Usuario.obtener_todos()  # Asegúrate de que obtener_todos() incluya el campo 'estatus'
        except Exception as e:
            print(f"⚠️ Error al listar usuarios: {e}")
            return []

    @staticmethod
    def eliminar_usuario(id_usuario):
        """Elimina un usuario."""
        try:
            Usuario.eliminar_usuario(id_usuario)
            return True, "✅ Usuario desactivado correctamente."
        except Exception as e:
            return False, f"❌ Error al eliminar usuario: {str(e)}"

    # ✅ Nuevos métodos para manejar estatus
    @staticmethod
    def aprobar_usuario(id_usuario):
        """Aprobar usuario pendiente."""
        try:
            Usuario.aprobar_usuario(id_usuario)
            return True, "✅ Usuario aprobado correctamente."
        except Exception as e:
            return False, f"❌ Error al aprobar usuario: {str(e)}"

    @staticmethod
    def rechazar_usuario(id_usuario):
        """Rechazar usuario pendiente."""
        try:
            Usuario.rechazar_usuario(id_usuario)
            return True, "✅ Usuario rechazado correctamente."
        except Exception as e:
            return False, f"❌ Error al rechazar usuario: {str(e)}"

    @staticmethod
    def obtener_usuarios_pendientes():
        """Obtiene usuarios pendientes de aprobación."""
        try:
            return Usuario.obtener_usuarios_pendientes()
        except Exception as e:
            print(f"⚠️ Error al obtener usuarios pendientes: {e}")
            return []
        
    @staticmethod
    def actualizar_usuario(id_usuario, nombre_usuario=None, nombre_completo=None, rol=None):
        """Actualizar datos de un usuario."""
        try:
            from models.usuario import Usuario
            Usuario.actualizar_usuario(id_usuario, nombre_usuario, nombre_completo, rol)
            return True, "✅ Usuario actualizado correctamente."
        except Exception as e:
            return False, f"❌ Error al actualizar usuario: {str(e)}"
        
    @staticmethod
    def reactivar_usuario(id_usuario):
        """Reactiva un usuario."""
        try:
            from models.usuario import Usuario
            Usuario.reactivar_usuario(id_usuario)  # ✅ Llama al método correcto
            return True, "✅ Usuario reactivado correctamente."
        except Exception as e:
            return False, f"❌ Error al reactivar usuario: {str(e)}"
        
        
    @staticmethod
    def eliminar_usuario_fisico(id_usuario):
        """Eliminar un usuario físicamente de la base de datos."""
        try:
            from models.usuario import Usuario
            Usuario.eliminar_usuario_fisico(id_usuario)
            return True, "✅ Usuario eliminado físicamente correctamente."
        except Exception as e:
            return False, f"❌ Error al eliminar usuario: {str(e)}"