# views/producto_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController
from controllers.proveedor_controller import ProveedorController

class ProductoView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("📦 Gestión de Productos")
        self.window.geometry("1150x600")

        self.producto_seleccionado_id = None
        # ✅ Inicializamos la lista vacía desde el inicio
        self.lista_proveedores = {}
        
        self.create_widgets()
        self.cargar_proveedores()
        self.cargar_productos()

    def create_widgets(self):
        frame_form = tk.Frame(self.window, padx=15, pady=15)
        frame_form.pack(side="left", fill="y")

        tk.Label(frame_form, text="➕/✏️ Producto", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame_form, text="Código:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_codigo = tk.Entry(frame_form, width=25)
        self.entry_codigo.grid(row=1, column=1, pady=5)

        tk.Label(frame_form, text="Nombre *:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_nombre = tk.Entry(frame_form, width=25)
        self.entry_nombre.grid(row=2, column=1, pady=5)

        tk.Label(frame_form, text="Descripción:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_desc = tk.Entry(frame_form, width=25)
        self.entry_desc.grid(row=3, column=1, pady=5)

        tk.Label(frame_form, text="Tipo *:").grid(row=4, column=0, sticky="e", pady=5)
        self.combo_tipo = ttk.Combobox(frame_form, values=["unidad", "granel"], state="readonly", width=22)
        self.combo_tipo.set("unidad")
        self.combo_tipo.grid(row=4, column=1, pady=5)

        tk.Label(frame_form, text="Precio Unitario ($):").grid(row=5, column=0, sticky="e", pady=5)
        # ✅ Validar que solo se acepten números (con decimales)
        vcmd = (self.window.register(self.validar_numero), '%P')
        self.entry_precio = tk.Entry(frame_form, width=25, validate='key', validatecommand=vcmd)
        self.entry_precio.grid(row=5, column=1, pady=5)

        tk.Label(frame_form, text="Stock Inicial:").grid(row=6, column=0, sticky="e", pady=5)
        # ✅ Validar también el stock
        vcmd_stock = (self.window.register(self.validar_numero), '%P')
        self.entry_stock = tk.Entry(frame_form, width=25, validate='key', validatecommand=vcmd_stock)
        self.entry_stock.grid(row=6, column=1, pady=5)
        self.entry_stock.insert(0, "0.000")

        tk.Label(frame_form, text="Proveedor:").grid(row=7, column=0, sticky="e", pady=5)
        self.combo_proveedor = ttk.Combobox(frame_form, state="readonly", width=22)
        self.combo_proveedor.grid(row=7, column=1, pady=5)
        
        # Botones
        btn_frame = tk.Frame(frame_form)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15)

        self.btn_guardar = ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar)
        self.btn_guardar.pack(side="left", padx=5)

        ttk.Button(btn_frame, text="↻ Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # Frame derecho: tabla
        frame_tabla = tk.Frame(self.window)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10)

        columns = ("ID", "Código", "Nombre", "Tipo", "Precio", "Stock", "Proveedor")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=85)

        # Ajustar anchos específicos
        self.tree.column("Nombre", width=150)
        self.tree.column("Código", width=80)
        self.tree.column("Proveedor", width=120)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ✅ Vincular clic derecho al árbol
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

    def validar_numero(self, valor):
        """Valida que el campo solo acepte números (enteros o decimales)."""
        if valor == "":
            return True  # Permitir campo vacío
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def cargar_proveedores(self):
        """Carga proveedores y los guarda en self.lista_proveedores"""
        print("🔄 Iniciando carga de proveedores...")

        try:
            proveedores = ProveedorController.listar_proveedores()
            print(f"✅ Proveedores obtenidos: {len(proveedores)}")

            # Limpiar combo
            self.combo_proveedor['values'] = []
            self.combo_proveedor.set("")  # Limpiar selección

            if not proveedores:
                print("⚠️ No hay proveedores registrados.")
                self.lista_proveedores = {}
                self.combo_proveedor['values'] = ["— Sin proveedores —"]
                self.combo_proveedor.set("")  # Dejar vacío
                return

            # Crear diccionario: {id: nombre}
            self.lista_proveedores = {p['id']: p['nombre'] for p in proveedores}
            nombres = list(self.lista_proveedores.values())

            # Actualizar combo
            self.combo_proveedor['values'] = nombres
            # self.combo_proveedor.set(nombres[0])  # ✅ Comentamos esta línea
            self.combo_proveedor.set("")  # ✅ Dejar vacío por defecto

            print(f"✅ Combo actualizado con {len(nombres)} proveedores: {nombres}")

            # Forzar actualización visual del combo
            self.combo_proveedor.update_idletasks()

        except Exception as e:
            print(f"❌ Error al cargar proveedores: {e}")
            messagebox.showerror("❌ Error", f"No se pudieron cargar los proveedores:\n{e}", parent=self.window)
            self.lista_proveedores = {}
            self.combo_proveedor['values'] = ["— Error al cargar —"]
            self.combo_proveedor.set("— Error al cargar —")

        print("🔍 self.lista_proveedores:", self.lista_proveedores)
        print("📋 self.combo_proveedor['values']:", self.combo_proveedor['values'])

    def cargar_productos(self):
        for item in self.tree.get_children():
           self.tree.delete(item)

        try:
            productos = ProductoController.listar_productos()
            for p in productos:
                proveedor = p.get('proveedor', '—')
                self.tree.insert("", "end", values=(
                    p['id'], p['codigo'], p['nombre'], p['tipo'],
                    f"${p['precio_unitario']:.2f}", f"{p['stock']:.3f}", proveedor
                ))
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar los productos:\n{e}", parent=self.window)
            print(f"Error en cargar_productos: {e}")

    def guardar(self):
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        desc = self.entry_desc.get().strip()
        tipo = self.combo_tipo.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        
        # ✅ Obtener proveedor seleccionado (puede ser None)
        proveedor_nombre = self.combo_proveedor.get()
        id_proveedor = None
        if proveedor_nombre and proveedor_nombre in self.lista_proveedores.values():
            # Buscar ID del proveedor
            for pid, pnombre in self.lista_proveedores.items():
                if pnombre == proveedor_nombre:
                    id_proveedor = pid
                    break

        # Llamar al controlador
        if self.producto_seleccionado_id is None:
            exito, mensaje, _ = ProductoController.crear_producto(
                codigo=codigo, nombre=nombre, descripcion=desc, tipo=tipo,
                precio_unitario=precio, stock=stock, id_proveedor=id_proveedor
            )
        else:
            exito, mensaje, _ = ProductoController.actualizar_producto(
                id_producto=self.producto_seleccionado_id, codigo=codigo, nombre=nombre,
                descripcion=desc, tipo=tipo, precio_unitario=precio, stock=stock,
                id_proveedor=id_proveedor
            )

        if exito:
            messagebox.showinfo("✅ Éxito", mensaje, parent=self.window)
            self.limpiar()
            self.cargar_productos()
        else:
            messagebox.showerror("❌ Error", mensaje, parent=self.window)

    def limpiar(self):
        self.producto_seleccionado_id = None
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, "0.000")
        self.combo_tipo.set("unidad")
        self.combo_proveedor.set("")
        self.btn_guardar.config(text="💾 Guardar")

    def mostrar_menu_contextual(self, event):
        """Muestra menú contextual al hacer clic derecho sobre una fila."""
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
            id_producto = int(values[0])
        except (ValueError, IndexError):
            return

        # Crear menú contextual
        menu = tk.Menu(self.window, tearoff=0)

        menu.add_command(
            label="✏️ Editar Producto",
            command=lambda: self.editar_producto_directo(id_producto),
            foreground="blue"
        )
        menu.add_command(
            label="🗑️ Eliminar Producto",
            command=lambda: self.eliminar_producto_directo(id_producto),
            foreground="red"
        )

        menu.add_separator()
        menu.add_command(label="❌ Cerrar", command=menu.destroy)

        # Mostrar menú en la posición del clic
        menu.tk_popup(event.x_root, event.y_root)

    def editar_producto_directo(self, id_producto):
        """Editar producto directamente."""
        # Cargar datos del producto
        productos = ProductoController.listar_productos()
        producto = None
        for p in productos:
            if p['id'] == id_producto:
                producto = p
                break

        if not producto:
            messagebox.showerror("❌ Error", "Producto no encontrado.", parent=self.window)
            return

        # Cargar datos en el formulario
        self.limpiar()
        self.producto_seleccionado_id = id_producto
        self.entry_codigo.insert(0, producto['codigo'])
        self.entry_nombre.insert(0, producto['nombre'])
        self.entry_desc.insert(0, producto['descripcion'] or "")
        self.combo_tipo.set(producto['tipo'])
        self.entry_precio.insert(0, str(producto['precio_unitario']))
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, str(producto['stock']))

        # Cargar proveedor
        if producto['id_proveedor'] and producto['id_proveedor'] in self.lista_proveedores:
            self.combo_proveedor.set(self.lista_proveedores[producto['id_proveedor']])

        # Cambiar texto del botón de guardar
        self.btn_guardar.config(text="💾 Actualizar")

    def eliminar_producto_directo(self, id_producto):
        """Eliminar producto directamente."""
        if messagebox.askyesno(
            "🗑️ Confirmar eliminación",
            "¿Eliminar este producto?\n¡Esta acción no se puede deshacer!",
            parent=self.window
        ):
            exito, mensaje = ProductoController.eliminar_producto(id_producto)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=self.window)
                self.limpiar()
                self.cargar_productos()
            else:
                messagebox.showerror("❌ Error", mensaje, parent=self.window)

    # ✅ Eliminar los métodos editar() y eliminar() antiguos
    # ✅ Eliminar el método forzar_seleccion() si ya no lo necesitas