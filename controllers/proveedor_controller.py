# controllers/proveedor_controller.py
from models.proveedor import Proveedor
import mysql.connector
from config.db_config import DB_CONFIG

class ProveedorController:
    @staticmethod
    def listar_proveedores():
        return Proveedor.get_all()

    @staticmethod
    def crear_proveedor(nombre, contacto=None, telefono=None, email=None, direccion=None):
        if not nombre or not nombre.strip():
            return False, "❌ El nombre del proveedor es obligatorio.", None

        try:
            id_prov = Proveedor.create(
                nombre=nombre.strip(),
                contacto=contacto.strip() if contacto else None,
                telefono=telefono.strip() if telefono else None,
                email=email.strip() if email else None,
                direccion=direccion.strip() if direccion else None
            )
            return True, "✅ Proveedor creado correctamente.", id_prov
        except Exception as e:
            return False, f"❌ Error al crear proveedor: {str(e)}", None

    @staticmethod
    def actualizar_proveedor(id_proveedor, nombre, contacto=None, telefono=None, email=None, direccion=None):
        try:
            id_proveedor = int(id_proveedor)
        except (ValueError, TypeError):
            return False, "❌ ID de proveedor inválido.", None

        if not nombre or not nombre.strip():
            return False, "❌ El nombre es obligatorio.", None

        try:
            Proveedor.update(
                id_proveedor=id_proveedor,
                nombre=nombre.strip(),
                contacto=contacto.strip() if contacto else None,
                telefono=telefono.strip() if telefono else None,
                email=email.strip() if email else None,
                direccion=direccion.strip() if direccion else None
            )
            return True, "✅ Proveedor actualizado correctamente.", id_proveedor
        except Exception as e:
            return False, f"❌ Error al actualizar: {str(e)}", None

    @staticmethod
    def eliminar_proveedor(id_proveedor):
        """Elimina un proveedor. Maneja errores de integridad referencial."""
        try:
            id_proveedor = int(id_proveedor)
        except (ValueError, TypeError):
            return False, "❌ ID de proveedor inválido."

        prov = Proveedor.get_by_id(id_proveedor)
        if not prov:
            return False, f"❌ Proveedor con ID {id_proveedor} no existe."

        try:
            # Conexión directa para mayor control
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # 1. Desvincular de productos (seguridad extra)
            cursor.execute("UPDATE productos SET id_proveedor = NULL WHERE id_proveedor = %s", (id_proveedor,))
            # 2. Desvincular de compras (seguridad extra)
            cursor.execute("UPDATE compras SET id_proveedor = NULL WHERE id_proveedor = %s", (id_proveedor,))
            # 3. Eliminar proveedor
            cursor.execute("DELETE FROM proveedores WHERE id = %s", (id_proveedor,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True, (
                "✅ Proveedor eliminado correctamente.\n"
                "ℹ️ Los productos y compras asociadas ahora muestran 'Sin proveedor'."
            )
        except mysql.connector.Error as e:
            return False, f"❌ Error MySQL [{e.errno}]: {e.msg}"
        except Exception as e:
            return False, f"❌ Error inesperado: {str(e)}"