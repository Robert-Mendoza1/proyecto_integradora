# views/inventario_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.producto_controller import ProductoController
from controllers.proveedor_controller import ProveedorController
from PIL import Image, ImageTk
import os
import csv  # Para exportar a CSV (ligero y universal)

class InventarioView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("📦 Inventario Existente")
        self.window.geometry("1000x650")
        self.window.resizable(False, False)

        self.create_widgets()
        self.cargar_proveedores()
        self.cargar_inventario()

    def create_widgets(self):
        # === LOGO ===
        logo_frame = tk.Frame(self.window, bg="#f0f4f8", height=70)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((100, 50), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo, bg="#f0f4f8").pack(side="left", padx=20)
        except:
            tk.Label(logo_frame, text="📦 INVENTARIO", font=("Arial", 18, "bold"), 
                     fg="#2c3e50", bg="#f0f4f8").pack(side="left", padx=20)

        # === CONTROLES SUPERIORES ===
        top_frame = tk.Frame(self.window, padx=20, pady=10)
        top_frame.pack(fill="x")

        # Búsqueda
        tk.Label(top_frame, text="🔍 Buscar:").pack(side="left")
        self.entry_busqueda = tk.Entry(top_frame, width=30)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_inventario)

        # Filtros
        tk.Label(top_frame, text=" | Tipo:").pack(side="left", padx=(10, 2))
        self.combo_tipo = ttk.Combobox(top_frame, values=["Todos", "Unidad", "Granel"], state="readonly", width=10)
        self.combo_tipo.set("Todos")
        self.combo_tipo.pack(side="left", padx=2)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.filtrar_inventario)

        tk.Label(top_frame, text=" | Proveedor:").pack(side="left", padx=(10, 2))
        self.combo_proveedor = ttk.Combobox(top_frame, values=["Todos"], state="readonly", width=15)
        self.combo_proveedor.set("Todos")
        self.combo_proveedor.pack(side="left", padx=2)
        self.combo_proveedor.bind("<<ComboboxSelected>>", self.filtrar_inventario)

        # Botones
        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side="right")
        ttk.Button(btn_frame, text="📊 Exportar CSV", command=self.exportar_csv).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="↺ Refrescar", command=self.cargar_inventario).pack(side="left", padx=5)

        # === TABLA DE INVENTARIO ===
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columnas
        columns = ("ID", "Código", "Nombre", "Tipo", "Precio Venta", "Stock", "Stock (Texto)", "Proveedor", "Última Compra")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)

        # Encabezados
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo", text="Tipo", anchor="center")
        self.tree.heading("Precio Venta", text="Precio $", anchor="e")
        self.tree.heading("Stock", text="Stock", anchor="e")
        self.tree.heading("Stock (Texto)", text="Stock", anchor="w")  # Para mostrar "5 kg" o "10 uds"
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.heading("Última Compra", text="Última Compra")

        # Anchuras
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Código", width=90)
        self.tree.column("Nombre", width=180)
        self.tree.column("Tipo", width=70, anchor="center")
        self.tree.column("Precio Venta", width=80, anchor="e")
        self.tree.column("Stock", width=80, anchor="e")
        self.tree.column("Stock (Texto)", width=100, anchor="w")
        self.tree.column("Proveedor", width=120)
        self.tree.column("Última Compra", width=100, anchor="center")

        # Scrollbars
        v_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual) # Clic derecho
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # === RESUMEN INFERIOR ===
        summary_frame = tk.Frame(self.window, bg="#f8f9fa", height=50)
        summary_frame.pack(fill="x", side="bottom")
        summary_frame.pack_propagate(False)

        self.lbl_total_productos = tk.Label(summary_frame, text="Total: 0 productos", font=("Arial", 10), bg="#f8f9fa")
        self.lbl_total_productos.pack(side="left", padx=20)

        self.lbl_stock_unidad = tk.Label(summary_frame, text="Unidad: 0", font=("Arial", 10), bg="#f8f9fa")
        self.lbl_stock_unidad.pack(side="left", padx=10)

        self.lbl_stock_granel = tk.Label(summary_frame, text="Granel: 0 kg", font=("Arial", 10), bg="#f8f9fa")
        self.lbl_stock_granel.pack(side="left", padx=10)

        self.lbl_stock_bajo = tk.Label(summary_frame, text="⚠️ Stock bajo: 0", font=("Arial", 10, "bold"), fg="orange", bg="#f8f9fa")
        self.lbl_stock_bajo.pack(side="right", padx=20)

    def cargar_proveedores(self):
        try:
            proveedores = ProveedorController.listar_proveedores()
            nombres = ["Todos"] + [p['nombre'] for p in proveedores]
            self.combo_proveedor['values'] = nombres
            if nombres:
                self.combo_proveedor.set("Todos")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar los proveedores:\n{e}")

    def cargar_inventario(self):
        """Carga todos los productos para el inventario."""
        self.todos_los_productos = ProductoController.listar_productos()
        self.filtrar_inventario()  # Aplica filtros iniciales

    def filtrar_inventario(self, event=None):
        """Filtra la tabla según búsqueda y filtros."""
        termino = self.entry_busqueda.get().strip().lower()
        tipo_filtro = self.combo_tipo.get()
        proveedor_filtro = self.combo_proveedor.get()

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrar
        productos_filtrados = []
        for p in self.todos_los_productos:
            # Búsqueda
            if termino and not (termino in p['nombre'].lower() or termino in p['codigo'].lower()):
                continue
            # Tipo
            if tipo_filtro != "Todos":
                tipo_real = "Unidad" if p['tipo'] == 'unidad' else "Granel"
                if tipo_filtro != tipo_real:
                    continue
            # Proveedor
            if proveedor_filtro != "Todos" and p.get('proveedor', '') != proveedor_filtro:
                continue

            productos_filtrados.append(p)

        # Insertar en tabla
        stock_unidad = 0
        stock_granel = 0.0
        stock_bajo = 0

        for p in productos_filtrados:
            stock = float(p['stock'])
            tipo = p['tipo']
            
            # Acumular resumen
            if tipo == 'unidad':
                stock_unidad += int(stock)
            else:
                stock_granel += stock

            # Alerta de stock bajo (personalizable)
            stock_minimo = 5 if tipo == 'unidad' else 1.000  # 5 uds o 1 kg
            es_bajo = stock < stock_minimo
            if es_bajo:
                stock_bajo += 1

            # Formato de stock para mostrar
            stock_texto = f"{int(stock)} uds" if tipo == 'unidad' else f"{stock:.3f} kg"

            self.tree.insert("", "end", values=(
                p['id'],
                p['codigo'],
                p['nombre'],
                "📦" if tipo == 'unidad' else "⚖️",
                f"${p['precio_unitario']:.2f}",
                f"{stock:.3f}",
                stock_texto,
                p.get('proveedor', '—'),
                "N/A"  # Podrías agregar fecha de última compra si lo deseas
            ), tags=("bajo",) if es_bajo else ())

        # Estilo para stock bajo
        self.tree.tag_configure("bajo", background="#fff3cd", foreground="#856404")

        # Actualizar resumen
        total = len(productos_filtrados)
        self.lbl_total_productos.config(text=f"Total: {total} productos")
        self.lbl_stock_unidad.config(text=f"Unidad: {stock_unidad} uds")
        self.lbl_stock_granel.config(text=f"Granel: {stock_granel:.3f} kg")
        self.lbl_stock_bajo.config(text=f"⚠️ Stock bajo: {stock_bajo}")

    def exportar_csv(self):
        """Exporta el inventario filtrado a CSV."""
        if not self.tree.get_children():
            messagebox.showinfo("ℹ️", "No hay datos para exportar.")
            return

        # Obtener datos filtrados
        datos = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            datos.append({
                "ID": valores[0],
                "Código": valores[1],
                "Nombre": valores[2],
                "Tipo": "Unidad" if valores[3] == "📦" else "Granel",
                "Precio Venta": valores[4],
                "Stock Numérico": valores[5],
                "Stock": valores[6],
                "Proveedor": valores[7]
            })

        # Guardar archivo
        archivo = filedialog.asksaveasfilename(
            title="Guardar Inventario",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
        )
        if not archivo:
            return

        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                if datos:
                    writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                    writer.writeheader()
                    writer.writerows(datos)
            messagebox.showinfo("✅ Éxito", f"Inventario exportado a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar:\n{e}")
            
    def mostrar_menu_contextual(self, event):
        """Muestra un menú contextual al hacer clic derecho sobre una fila."""
        # Identificar la fila bajo el cursor
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return  # No hay fila bajo el cursor

        # Seleccionar la fila
        self.tree.selection_set(row_id)
        values = self.tree.item(row_id, "values")
        if not values or len(values) < 1:
            return

        try:
            id_producto = int(values[0])  # El ID está en la primera columna
        except (ValueError, TypeError):
            return

        # Crear menú contextual
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(
            label="✏️ Editar Producto",
            command=lambda: self.editar_producto(id_producto)
        )
        menu.add_separator()
        menu.add_command(
            label="🗑️ Eliminar Producto",
            command=lambda: self.eliminar_producto(id_producto),
            foreground="red"
        )
        menu.add_separator()
        menu.add_command(label="❌ Cerrar", command=menu.destroy)

        # Mostrar menú en la posición del clic
        menu.tk_popup(event.x_root, event.y_root)

    def editar_producto(self, id_producto):
        """(Opcional) Abre una ventana de edición del producto."""
        messagebox.showinfo("✏️ Editar", f"Editar producto ID {id_producto}.\n(Implementar en producto_view si es necesario)")

    def eliminar_producto(self, id_producto):
        """Elimina un producto después de confirmación."""
        # Obtener el nombre del producto para mostrar en confirmación
        producto = None
        for p in self.todos_los_productos:
            if p['id'] == id_producto:
                producto = p
                break

        if not producto:
            messagebox.showerror("❌ Error", "Producto no encontrado.")
            return

        nombre = producto['nombre']
        codigo = producto['codigo']

        if messagebox.askyesno(
            "🗑️ Confirmar Eliminación",
            f"¿Eliminar el producto?\n\n"
            f"ID: {id_producto}\n"
            f"Código: {codigo}\n"
            f"Nombre: {nombre}\n\n"
            "⚠️ Esta acción no se puede deshacer.\n"
            "Los registros de ventas/compras asociadas se mantendrán, pero sin producto.\n\n"
            "¿Deseas continuar?"
        ):
            try:
                from controllers.producto_controller import ProductoController
                exito, mensaje = ProductoController.eliminar_producto(id_producto)
                if exito:
                    messagebox.showinfo("✅ Éxito", mensaje)
                    # Refrescar inventario
                    self.cargar_inventario()
                else:
                    messagebox.showerror("❌ Error", mensaje)
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo eliminar el producto:\n{e}")
                
                
    def actualizar_tabla(self):
        """Actualiza la tabla de productos en la ventana de inventario."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = ProductoController.listar_productos()
        for p in productos:
            stock = float(p['stock'])
            tipo = p['tipo']
            stock_texto = f"{int(stock)} uds" if tipo == 'unidad' else f"{stock:.3f} kg"

            self.tree.insert("", "end", values=(
                p['id'],
                p['codigo'],
                p['nombre'],
                "📦" if tipo == 'unidad' else "⚖️",
                f"${p['precio_unitario']:.2f}",
                f"{stock:.3f}",
                stock_texto,
                p.get('proveedor', '—'),
                "N/A"  # Podrías agregar fecha de última compra si lo deseas
            ))