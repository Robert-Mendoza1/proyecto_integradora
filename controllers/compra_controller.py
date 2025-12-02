# controllers/compra_controller.py
from models.compra import Compra
from models.producto import Producto
from models.proveedor import Proveedor

class CompraController:
    @staticmethod
    def registrar_compra(id_producto, id_proveedor, cantidad, precio_compra, nota=None):
        """
        Registra una compra y actualiza stock.
        Retorna (éxito, mensaje)
        """
        # Validar IDs
        try:
            id_producto = int(id_producto)
            id_proveedor = int(id_proveedor) if id_proveedor else None
        except (ValueError, TypeError):
            return False, "❌ IDs de producto o proveedor inválidos."

        # Validar existencia de producto
        producto = Producto.get_by_id(id_producto)
        if not producto:
            return False, f"❌ Producto con ID {id_producto} no existe."

        # Validar proveedor (si se proporciona)
        if id_proveedor:
            proveedor = Proveedor.get_by_id(id_proveedor)
            if not proveedor:
                return False, f"❌ Proveedor con ID {id_proveedor} no existe."

        # Validar cantidad y precio
        try:
            cantidad = float(cantidad)
            precio_compra = float(precio_compra)
            if cantidad <= 0:
                return False, "❌ La cantidad debe ser mayor a 0."
            if precio_compra < 0:
                return False, "❌ El precio de compra no puede ser negativo."
        except (ValueError, TypeError):
            return False, "❌ Cantidad y precio deben ser números válidos."

        try:
            Compra.create(
                id_producto=id_producto,
                id_proveedor=id_proveedor,
                cantidad=cantidad,
                precio_compra=precio_compra,
                nota=nota
            )
            return True, f"✅ Compra registrada. +{cantidad:.3f} {producto['tipo']}(s) añadidos al stock."
        except Exception as e:
            return False, f"❌ Error al registrar compra: {str(e)}"

    @staticmethod
    def listar_compras():
        """Devuelve todas las compras con detalles."""
        return Compra.get_all()

    @staticmethod
    def obtener_compra(id_compra):
        """Obtiene una compra por ID."""
        try:
            id_compra = int(id_compra)
        except (ValueError, TypeError):
            return None
        return Compra.get_by_id(id_compra)

    @staticmethod
    def compras_por_proveedor(id_proveedor):
        """Obtiene todas las compras de un proveedor."""
        try:
            id_proveedor = int(id_proveedor)
        except (ValueError, TypeError):
            return []
        return Compra.get_compras_by_proveedor(id_proveedor)