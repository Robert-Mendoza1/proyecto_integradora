# views/venta_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from PIL import Image, ImageTk
import os

class VentaView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("🛒 Registrar Venta")
        self.window.geometry("1000x650")
        self.window.resizable(False, False)

        # Carrito: lista de dicts {'id': int, 'nombre': str, 'cantidad': float, 'precio': float, 'total': float, 'tipo': str}
        self.carrito = []

        self.create_widgets()
        self.cargar_productos()

    def create_widgets(self):
        # === LOGO ===
        logo_frame = tk.Frame(self.window, bg="#f8f9fa", height=80)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((60, 60), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo, bg="#f8f9fa").pack(side="left", padx=20)
        except Exception as e:
            tk.Label(logo_frame, text="🛒 TIENDA A GRANEL", font=("Arial", 20, "bold"), 
                     fg="#2c3e50", bg="#f8f9fa").pack(side="left", padx=20)

        # === BÚSQUEDA ===
        search_frame = tk.Frame(self.window, padx=20, pady=10)
        search_frame.pack(fill="x")
        
        tk.Label(search_frame, text="🔍 Buscar producto (nombre o código):", font=("Arial", 10)).pack(anchor="w")
        self.entry_busqueda = tk.Entry(search_frame, font=("Arial", 12), width=50)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_productos)
        
        ttk.Button(search_frame, text="↺ Limpiar", command=self.cargar_productos).pack(side="left")

        # === ESCANEAR CÓDIGO ===
        scan_frame = tk.Frame(self.window, padx=20, pady=5)
        scan_frame.pack(fill="x")

        tk.Label(scan_frame, text="📱 Escanear Producto (Código de Barras):", font=("Arial", 10)).pack(anchor="w")
        self.entry_codigo_barras = tk.Entry(scan_frame, font=("Arial", 14), width=30)
        self.entry_codigo_barras.pack(side="left", padx=(0, 10))
        self.entry_codigo_barras.bind("<Return>", self.agregar_producto_por_codigo)
        self.entry_codigo_barras.focus()  # Para que esté listo para escanear

        ttk.Button(scan_frame, text="➕ Agregar", command=self.agregar_producto_por_codigo).pack(side="left")
        self.agregar_producto_por_codigo = self.agregar_producto_por_codigo
        # === DIVISIÓN: productos + carrito ===
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Panel izquierdo: productos ---
        left_frame = tk.LabelFrame(main_frame, text="📦 Productos Disponibles", font=("Arial", 11, "bold"))
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Tabla de productos
        self.tree_productos = ttk.Treeview(left_frame, columns=("ID", "Código", "Nombre", "Tipo", "Precio", "Stock"), show="headings", height=10)
        self.tree_productos.heading("ID", text="ID", anchor="center")
        self.tree_productos.heading("Código", text="Código")
        self.tree_productos.heading("Nombre", text="Nombre")
        self.tree_productos.heading("Tipo", text="Tipo")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Stock", text="Stock")
        
        self.tree_productos.column("ID", width=40, anchor="center")
        self.tree_productos.column("Código", width=80)
        self.tree_productos.column("Nombre", width=150)
        self.tree_productos.column("Tipo", width=70, anchor="center")
        self.tree_productos.column("Precio", width=80, anchor="e")
        self.tree_productos.column("Stock", width=80, anchor="e")

        scrollbar_prod = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscroll=scrollbar_prod.set)
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_prod.pack(side="right", fill="y")

        # ✅ Vincular doble clic para agregar al carrito
        self.tree_productos.bind("<Double-1>", self.agregar_producto_desde_tabla)

        # --- Panel derecho: carrito ---
        right_frame = tk.LabelFrame(main_frame, text="🛒 Carrito de Compras", font=("Arial", 11, "bold"))
        right_frame.pack(side="right", fill="both", expand=True)

        # Tabla del carrito
        self.tree_carrito = ttk.Treeview(right_frame, columns=("ID", "Producto", "Cantidad", "Precio", "Total"), show="headings", height=8)
        self.tree_carrito.heading("ID", text="ID", anchor="center")
        self.tree_carrito.heading("Producto", text="Producto")
        self.tree_carrito.heading("Cantidad", text="Cantidad")
        self.tree_carrito.heading("Precio", text="Precio")
        self.tree_carrito.heading("Total", text="Total")
        
        self.tree_carrito.column("ID", width=40, anchor="center")
        self.tree_carrito.column("Producto", width=150)
        self.tree_carrito.column("Cantidad", width=80, anchor="e")
        self.tree_carrito.column("Precio", width=80, anchor="e")
        self.tree_carrito.column("Total", width=80, anchor="e")

        scrollbar_cart = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscroll=scrollbar_cart.set)
        self.tree_carrito.pack(side="top", fill="both", expand=True)
        scrollbar_cart.pack(side="right", fill="y")

        # ✅ Editar cantidad en el carrito (doble clic)
        self.tree_carrito.bind("<Double-1>", self.editar_cantidad_carrito)

        # Resumen y botones
        bottom_frame = tk.Frame(right_frame)
        bottom_frame.pack(fill="x", pady=10)

        # Total
        tk.Label(bottom_frame, text="TOTAL:", font=("Arial", 12, "bold")).pack(side="left")
        self.lbl_total = tk.Label(bottom_frame, text="$0.00", font=("Arial", 16, "bold"), fg="green")
        self.lbl_total.pack(side="left", padx=10)

        # Botones
        btn_frame_cart = tk.Frame(bottom_frame)
        btn_frame_cart.pack(side="right")

        ttk.Button(btn_frame_cart, text="🧹 Limpiar Carrito", command=self.limpiar_carrito).pack(side="left", padx=5)
        ttk.Button(btn_frame_cart, text="✅ Confirmar Venta", command=self.confirmar_venta).pack(side="left", padx=5)

        # Total ventas del día
        total_hoy = VentaController.total_ventas_hoy()
        tk.Label(self.window, text=f"💰 Ventas hoy: ${total_hoy:.2f}", 
                 font=("Arial", 10, "bold"), fg="darkgreen").pack(side="bottom", pady=5)

    def cargar_productos(self):
        """Carga todos los productos en la tabla."""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        try:
            productos = ProductoController.listar_productos()
            for p in productos:
                self.tree_productos.insert("", "end", values=(
                    p['id'],
                    p['codigo'],
                    p['nombre'],
                    "⚖️ Granel" if p['tipo'] == 'granel' else "📦 Unidad",
                    f"${p['precio_unitario']:.2f}",
                    f"{p['stock']:.3f}"
                ))
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar los productos:\n{e}")

    def buscar_productos(self, event=None):
        """Filtra productos por nombre o código."""
        termino = self.entry_busqueda.get().strip().lower()
        if not termino:
            self.cargar_productos()
            return

        try:
            productos = ProductoController.listar_productos()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Fallo al buscar:\n{e}")
            return

        # Filtrar
        resultados = []
        for p in productos:
            if (termino in p['nombre'].lower()) or (termino in p['codigo'].lower()):
                resultados.append(p)

        # Actualizar tabla
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in resultados:
            self.tree_productos.insert("", "end", values=(
                p['id'],
                p['codigo'],
                p['nombre'],
                "⚖️ Granel" if p['tipo'] == 'granel' else "📦 Unidad",
                f"${p['precio_unitario']:.2f}",
                f"{p['stock']:.3f}"
            ))


    def agregar_producto_desde_tabla(self, event):
        """Agrega un producto al carrito con cantidad predeterminada al hacer doble clic en la tabla."""
        selected = self.tree_productos.focus()
        if not selected:
            return

        values = self.tree_productos.item(selected, "values")
        if not values:
            return

        try:
            id_prod = int(values[0])
            nombre = values[2]
            tipo = "granel" if "Granel" in values[3] else "unidad"
            precio = float(values[4].replace("$", ""))
            stock_actual = float(values[5])

            # ✅ Cantidad predeterminada
            cantidad_predeterminada = 0.500 if tipo == "granel" else 1  # 500g o 1 unidad

            # Validar stock
            if cantidad_predeterminada > stock_actual:
                unidad = "kg" if tipo == "granel" else "uds"
                messagebox.showerror("❌ Stock insuficiente", 
                                f"Disponible: {stock_actual:.3f} {unidad}")
                return

            # Verificar si ya está en el carrito
            for item in self.carrito:
                if item['id'] == id_prod:
                    item['cantidad'] += cantidad_predeterminada
                    item['total'] = item['cantidad'] * item['precio']
                    self.actualizar_carrito()
                    return

            # Añadir nuevo
            self.carrito.append({
                'id': id_prod,
                'nombre': nombre,
                'cantidad': cantidad_predeterminada,
                'precio': precio,
                'total': cantidad_predeterminada * precio,
                'tipo': tipo
            })
            self.actualizar_carrito()

        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo agregar el producto:\n{e}")



    def editar_cantidad_carrito(self, event):
        """Permite editar la cantidad con doble clic."""
        item_id = self.tree_carrito.identify_row(event.y)
        if not item_id:
            return

        # Obtener índice en el carrito
        item = None
        for i, carrito_item in enumerate(self.carrito):
            if str(carrito_item['id']) in self.tree_carrito.item(item_id, "values")[0]:
                item = carrito_item
                break

        if not item:
            return

        nueva_cantidad = simpledialog.askfloat(
            "Editar Cantidad",
            f"Nueva cantidad para '{item['nombre']}':",
            initialvalue=item['cantidad'],
            minvalue=0.001 if item['tipo'] == 'granel' else 1,
            parent=self.window
        )

        if nueva_cantidad is not None:
            if nueva_cantidad <= 0:
                # Eliminar si es 0
                self.carrito.remove(item)
            else:
                # Actualizar
                item['cantidad'] = nueva_cantidad
                item['total'] = nueva_cantidad * item['precio']
            self.actualizar_carrito()

    def actualizar_carrito(self):
        """Actualiza la tabla del carrito y el total."""
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        total = 0.0
        for item in self.carrito:
            self.tree_carrito.insert("", "end", values=(
                item['id'],
                item['nombre'],
                f"{item['cantidad']:.3f}",
                f"${item['precio']:.2f}",
                f"${item['total']:.2f}"
            ))
            total += item['total']

        self.lbl_total.config(text=f"${total:.2f}")

    def limpiar_carrito(self):
        """Vacía el carrito."""
        if self.carrito and messagebox.askyesno("🧹 Limpiar carrito", "¿Vaciar todo el carrito?"):
            self.carrito.clear()
            self.actualizar_carrito()

    def agregar_producto_por_codigo(self, event=None):
        """Agrega un producto al carrito usando su código de barras."""
        codigo = self.entry_codigo_barras.get().strip()
        if not codigo:
            messagebox.showwarning("⚠️", "Escribe o escanea un código de producto.")
            return

        # Buscar producto por código
        try:
            productos = ProductoController.buscar_producto(codigo=codigo)
            if not productos:
                messagebox.showerror("❌", f"No se encontró un producto con código: {codigo}")
                self.entry_codigo_barras.delete(0, tk.END)
                return

            producto = productos[0]  # Tomar el primero si hay más de uno
            id_prod = producto['id']
            nombre = producto['nombre']
            tipo = producto['tipo']
            precio = producto['precio_unitario']  # Esto es Decimal
            stock_actual = producto['stock']      # Esto es Decimal

            # Pedir cantidad
            cantidad_inicial = "0.500" if tipo == "granel" else "1"
            cantidad = simpledialog.askfloat(
                "Cantidad", 
                f"Ingrese cantidad a vender ({'kg' if tipo=='granel' else 'unidades'}):\n"
                f"Producto: {nombre}\n"
                f"Precio: ${precio:.2f}",
                initialvalue=cantidad_inicial,
                minvalue=0.001 if tipo == "granel" else 1,
                parent=self.window
            )
            if cantidad is None:
                self.entry_codigo_barras.delete(0, tk.END)
                return  # Canceló

            if cantidad <= 0:
                messagebox.showwarning("⚠️", "La cantidad debe ser mayor a 0.")
                self.entry_codigo_barras.delete(0, tk.END)
                return

            # ✅ Convertir cantidad a Decimal para evitar errores
            from decimal import Decimal, getcontext
            getcontext().prec = 10
            cantidad_decimal = Decimal(str(cantidad))  # Convertir a Decimal

            if cantidad_decimal > stock_actual:
                unidad = "kg" if tipo == "granel" else "uds"
                messagebox.showerror("❌ Stock insuficiente", 
                                f"Disponible: {stock_actual:.3f} {unidad}")
                self.entry_codigo_barras.delete(0, tk.END)
                return

            # Verificar si ya está en el carrito
            for item in self.carrito:
                if item['id'] == id_prod:
                    item['cantidad'] += cantidad_decimal
                    item['total'] = item['cantidad'] * item['precio']
                    self.actualizar_carrito()
                    self.entry_codigo_barras.delete(0, tk.END)  # Limpiar campo
                    return

            # Añadir nuevo
            self.carrito.append({
                'id': id_prod,
                'nombre': nombre,
                'cantidad': cantidad_decimal,
                'precio': float(precio),  # Convertir a float para evitar errores en la tabla
                'total': float(cantidad_decimal * precio),  # Calcular total como float
                'tipo': tipo
            })
            self.actualizar_carrito()
            self.entry_codigo_barras.delete(0, tk.END)  # Limpiar campo

        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo agregar el producto:\n{e}")
            self.entry_codigo_barras.delete(0, tk.END)

    def confirmar_venta(self):
        """Inicia el proceso de venta con pantalla de pago."""
        if not self.carrito:
            messagebox.showwarning("⚠️", "El carrito está vacío.")
            return

        total_venta = float(self.lbl_total.cget("text")[1:])  # Extraer $12.50 → 12.50

        # === Pantalla 1: Ingresar cantidad recibida ===
        pago_recibido = simpledialog.askfloat(
            "💰 Pago",
            f"Total a pagar: ${total_venta:.2f}\n\nIngrese la cantidad recibida:",
            initialvalue=total_venta,
            minvalue=0.01,
            parent=self.window
        )

        if pago_recibido is None:
            return  # Canceló

        if pago_recibido < total_venta:
            messagebox.showerror(
                "❌ Pago insuficiente",
                f"Faltan ${total_venta - pago_recibido:.2f} para cubrir la venta.\n"
                f"Total: ${total_venta:.2f} | Recibido: ${pago_recibido:.2f}"
            )
            return

        # === Pantalla 2: Mostrar cambio y confirmar ===
        cambio = pago_recibido - total_venta

        # Crear ventana modal de confirmación
        confirm_window = tk.Toplevel(self.window)
        confirm_window.title("✅ Confirmar Venta")
        confirm_window.geometry("400x300")
        confirm_window.resizable(False, False)
        confirm_window.transient(self.window)
        confirm_window.grab_set()  # Modal

        # Estilo
        tk.Label(confirm_window, text="🧾 RESUMEN DE VENTA", font=("Arial", 14, "bold")).pack(pady=15)

        frame = tk.Frame(confirm_window, padx=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Total: ", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(frame, text=f"${total_venta:.2f}", font=("Arial", 12, "bold"), fg="green").grid(row=0, column=1, sticky="e", pady=5)

        tk.Label(frame, text="Recibido: ", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(frame, text=f"${pago_recibido:.2f}", font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="e", pady=5)

        tk.Label(frame, text="Cambio: ", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(frame, text=f"${cambio:.2f}", font=("Arial", 14, "bold"), fg="blue").grid(row=2, column=1, sticky="e", pady=5)

        # Separador
        ttk.Separator(frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        # Lista de productos
        tk.Label(frame, text="Productos:", font=("Arial", 10, "underline")).grid(row=4, column=0, sticky="w")
        for i, item in enumerate(self.carrito[:5]):  # Mostrar hasta 5 productos
            tk.Label(frame, text=f"• {item['cantidad']:.3f} × {item['nombre']}", font=("Arial", 9)).grid(
                row=5+i, column=0, columnspan=2, sticky="w"
            )
        if len(self.carrito) > 5:
            tk.Label(frame, text=f"... y {len(self.carrito)-5} más", font=("Arial", 9, "italic")).grid(
                row=10, column=0, columnspan=2, sticky="w"
            )

        # Botones
        btn_frame = tk.Frame(confirm_window)
        btn_frame.pack(pady=15)

        def registrar_venta():
            # Registrar cada producto
            errores = []
            for item in self.carrito:
                exito, mensaje, _ = VentaController.registrar_venta(
                    id_producto=item['id'],
                    cantidad=item['cantidad'],
                    precio_venta=item['precio']
                )
                if not exito:
                    errores.append(f"{item['nombre']}: {mensaje}")

            if errores:
                messagebox.showerror("❌ Errores", "No se pudieron registrar algunos productos:\n" + "\n".join(errores), parent=confirm_window)
                confirm_window.destroy()
            else:
                messagebox.showinfo("✅ Éxito", f"Venta registrada por ${total_venta:.2f}\nCambio: ${cambio:.2f}", parent=confirm_window)
                confirm_window.destroy()

                # Refrescar
                self.carrito.clear()
                self.actualizar_carrito()
                self.cargar_productos()  # actualizar stock
                # Actualizar total del día
                total_hoy = VentaController.total_ventas_hoy()
                for widget in self.window.winfo_children():
                    if isinstance(widget, tk.Label) and "Ventas hoy" in widget.cget("text"):
                        widget.config(text=f"💰 Ventas hoy: ${total_hoy:.2f}")
                        break

        ttk.Button(btn_frame, text="✅ Confirmar Venta", command=registrar_venta).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=confirm_window.destroy).pack(side="left", padx=5)

        # Centrar ventana
        confirm_window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (confirm_window.winfo_width() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (confirm_window.winfo_height() // 2)
        confirm_window.geometry(f"+{x}+{y}")