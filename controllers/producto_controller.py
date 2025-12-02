# controllers/producto_controller.py
from models.producto import Producto
from models.proveedor import Proveedor

class ProductoController:
    @staticmethod
    def listar_productos():
        """Devuelve lista de productos con nombre de proveedor."""
        return Producto.get_all()

    @staticmethod
    def crear_producto(codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor):
        """
        Crea un nuevo producto. Valida datos.
        Retorna (éxito: bool, mensaje: str, id_producto: int|None)
        """
        if not nombre or not nombre.strip():
            return False, "❌ El nombre del producto es obligatorio.", None

        try:
            precio_unitario = float(precio_unitario)
            stock = float(stock)
            if precio_unitario < 0:
                return False, "❌ El precio no puede ser negativo.", None
            if stock < 0:
                return False, "❌ El stock no puede ser negativo.", None
        except (ValueError, TypeError):
            return False, "❌ Precio y stock deben ser números válidos.", None

        if tipo not in ['unidad', 'granel']:
            return False, "❌ Tipo debe ser 'unidad' o 'granel'.", None

        # Validar proveedor (si se proporciona)
        if id_proveedor:
            try:
                id_proveedor = int(id_proveedor)
                proveedor = Proveedor.get_by_id(id_proveedor)
                if not proveedor:
                    return False, f"❌ Proveedor con ID {id_proveedor} no existe.", None
            except (ValueError, TypeError):
                return False, "❌ ID de proveedor inválido.", None

        try:
            id_producto = Producto.create(codigo, nombre.strip(), descripcion.strip(), tipo, precio_unitario, stock, id_proveedor)
            return True, "✅ Producto creado correctamente.", id_producto
        except Exception as e:
            return False, f"❌ Error al crear producto: {str(e)}", None

    @staticmethod
    def actualizar_producto(id_producto, codigo, nombre, descripcion, tipo, precio_unitario, stock, id_proveedor):
        """Actualiza un producto existente."""
        if not nombre or not nombre.strip():
            return False, "❌ El nombre es obligatorio.", None

        try:
            id_producto = int(id_producto)
            precio_unitario = float(precio_unitario)
            stock = float(stock)
            if precio_unitario < 0 or stock < 0:
                return False, "❌ Precio y stock no pueden ser negativos.", None
        except (ValueError, TypeError):
            return False, "❌ Datos numéricos inválidos.", None

        if tipo not in ['unidad', 'granel']:
            return False, "❌ Tipo debe ser 'unidad' o 'granel'.", None

        # Validar proveedor
        if id_proveedor:
            try:
                id_proveedor = int(id_proveedor)
                if not Proveedor.get_by_id(id_proveedor):
                    return False, f"❌ Proveedor con ID {id_proveedor} no existe.", None
            except (ValueError, TypeError):
                return False, "❌ ID de proveedor inválido.", None

        try:
            Producto.update(id_producto, codigo, nombre.strip(), descripcion.strip(), tipo, precio_unitario, stock, id_proveedor)
            return True, "✅ Producto actualizado correctamente.", id_producto
        except Exception as e:
            return False, f"❌ Error al actualizar: {str(e)}", None

    @staticmethod
    def eliminar_producto(id_producto):
        """Elimina un producto (con validación de existencia)."""
        try:
            id_producto = int(id_producto)
        except (ValueError, TypeError):
            return False, "❌ ID de producto inválido."

        prod = Producto.get_by_id(id_producto)
        if not prod:
            return False, f"❌ Producto con ID {id_producto} no existe."

        try:
            Producto.delete(id_producto)
            return True, "✅ Producto eliminado correctamente."
        except Exception as e:
            return False, f"❌ Error al eliminar: {str(e)}"

    @staticmethod
    def buscar_producto(id_producto=None, codigo=None, nombre=None):
        """Búsqueda flexible. Devuelve lista de coincidencias."""
        productos = Producto.get_all()
        resultado = []
        for p in productos:
            coincide = True
            if id_producto and str(p['id']) != str(id_producto):
                coincide = False
            if codigo and codigo.lower() not in p['codigo'].lower():
                coincide = False
            if nombre and nombre.lower() not in p['nombre'].lower():
                coincide = False
            if coincide:
                resultado.append(p)
        return resultado