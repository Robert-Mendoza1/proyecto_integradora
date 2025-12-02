# controllers/venta_controller.py
from models.venta import Venta
from models.producto import Producto
from decimal import Decimal, getcontext
getcontext().prec = 10 

class VentaController:
    @staticmethod
    def registrar_venta(id_producto, cantidad, precio_venta):
        """
        Registra una venta y actualiza stock.
        Retorna (éxito, mensaje, total)
        """
        # Validar ID de producto
        try:
            id_producto = int(id_producto)
        except (ValueError, TypeError):
            return False, "❌ ID de producto inválido.", 0

        # Obtener producto
        producto = Producto.get_by_id(id_producto)
        if not producto:
            return False, f"❌ Producto con ID {id_producto} no existe.", 0

        # Validar cantidad
        try:
            cantidad = float(cantidad)
            if cantidad <= 0:
                return False, "❌ La cantidad debe ser mayor a 0.", 0
        except (ValueError, TypeError):
            return False, "❌ Cantidad debe ser un número válido.", 0

        # Validar stock suficiente
        if cantidad > producto['stock']:
            disp = producto['stock']
            unidad = 'kg' if producto['tipo'] == 'granel' else 'uds'
            return False, f"❌ Stock insuficiente. Disponible: {disp:.3f} {unidad}.", 0

        # Validar precio
        try:
            precio_venta = float(precio_venta)
            if precio_venta < 0:
                return False, "❌ El precio de venta no puede ser negativo.", 0
        except (ValueError, TypeError):
            return False, "❌ Precio debe ser un número válido.", 0

        # Calcular total
        total = cantidad * precio_venta

       
            
        try:
            # ✅ Convertir TODO a Decimal
            cantidad = Decimal(str(cantidad))
            precio_venta = Decimal(str(precio_venta))
            total = cantidad * precio_venta

            # Registrar venta
            Venta.create(
                id_producto=id_producto,
                cantidad=float(cantidad),  # MySQL espera float/decimal, pero el conector maneja Decimal
                precio_venta=float(precio_venta),
                total=float(total),
                tipo_venta=producto['tipo']
            )

            # Actualizar stock: nuevo_stock = stock_actual - cantidad
            stock_actual = Decimal(str(producto['stock']))
            nuevo_stock = stock_actual - cantidad
            Producto.actualizar_stock(id_producto, nuevo_stock)  # ← ya acepta Decimal

            return True, "✅ Venta registrada correctamente.", float(total)
        except Exception as e:
            return False, f"❌ Error al registrar venta: {str(e)}", 0

    @staticmethod
    def listar_ventas():
        """Devuelve todas las ventas con detalles."""
        return Venta.get_all()

    @staticmethod
    def obtener_venta(id_venta):
        """Obtiene una venta por ID."""
        try:
            id_venta = int(id_venta)
        except (ValueError, TypeError):
            return None
        return Venta.get_by_id(id_venta)

    @staticmethod
    def ventas_por_fecha(fecha_inicio=None, fecha_fin=None):
        """Obtiene ventas en rango de fechas."""
        return Venta.get_ventas_by_date(fecha_inicio, fecha_fin)

    @staticmethod
    def total_ventas_hoy():
        """Devuelve el total de ventas del día."""
        return Venta.total_ventas_hoy()