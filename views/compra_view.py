# views/compra_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedor_controller import ProveedorController
from controllers.producto_controller import ProductoController
from controllers.compra_controller import CompraController

class CompraView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("📥 Registrar Compra a Proveedor")
        self.window.geometry("750x550")
        self.window.resizable(False, False)

        self.create_widgets()
        self.cargar_proveedores()
        self.cargar_productos()

    def create_widgets(self):
        tk.Label(self.window, text="➕ Nueva Compra", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        frame_form = tk.Frame(self.window, padx=20, pady=10)
        frame_form.pack(fill="x")

        # Proveedor
        tk.Label(frame_form, text="Proveedor *:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_proveedor = ttk.Combobox(frame_form, state="readonly", width=40)
        self.combo_proveedor.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Producto
        tk.Label(frame_form, text="Producto *:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_producto = ttk.Combobox(frame_form, state="readonly", width=40)
        self.combo_producto.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.combo_producto.bind("<<ComboboxSelected>>", self.actualizar_info_producto)

        # Info producto
        self.frame_info = tk.Frame(frame_form)
        self.frame_info.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")
        self.lbl_info = tk.Label(self.frame_info, text="—", fg="gray")
        self.lbl_info.pack()

        # Cantidad y precio
        tk.Label(frame_form, text="Cantidad *:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_cantidad = tk.Entry(frame_form, width=15)
        self.entry_cantidad.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.entry_cantidad.insert(0, "1.000")
        

        tk.Label(frame_form, text="Precio Compra ($/u) *:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_precio = tk.Entry(frame_form, width=15)
        self.entry_precio.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.entry_precio.insert(0, "0.00")


        # Nota
        tk.Label(frame_form, text="Nota:").grid(row=6, column=0, sticky="nw", pady=5)
        self.text_nota = tk.Text(frame_form, height=3, width=40)
        self.text_nota.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Botones
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="💾 Registrar Compra", command=self.guardar_compra).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy).pack(side="left", padx=10)

        # Últimas compras
        tk.Label(self.window, text="Últimas 10 Compras", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        frame_tabla = tk.Frame(self.window)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        columns = ("ID", "Producto", "Proveedor", "Cantidad", "Precio", "Total", "Fecha")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=6)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=85, anchor="center")
        self.tree.column("Producto", width=150, anchor="w")
        self.tree.column("Proveedor", width=120, anchor="w")
        self.tree.column("Fecha", width=130)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_ultimas_compras()
        
    def calcular_total_compra(self, event=None):
        """Calcula y muestra el total estimado = cantidad × precio_compra."""
        try:
            # Obtener valores
            cantidad_str = self.entry_cantidad.get().strip()
            precio_str = self.entry_precio.get().strip()

            # Si están vacíos, mostrar $0.00
            if not cantidad_str or not precio_str:
                self.lbl_total.config(text="$0.00")
                return

            # Convertir a números
            cantidad = float(cantidad_str)
            precio = float(precio_str)

            # Validar positivos
            if cantidad < 0 or precio < 0:
                self.lbl_total.config(text="$0.00", fg="red")
                return

            # Calcular total
            total = cantidad * precio

            # Mostrar con 2 decimales y color según el valor
            if total == 0:
                self.lbl_total.config(text="$0.00", fg="gray")
            else:
                self.lbl_total.config(text=f"${total:.2f}", fg="green")

        except ValueError:
            # Si no son números válidos
            self.lbl_total.config(text="$ — ", fg="orange")

    def cargar_proveedores(self):
        proveedores = ProveedorController.listar_proveedores()
        self.proveedores_dict = {p['id']: p['nombre'] for p in proveedores}
        self.combo_proveedor['values'] = list(self.proveedores_dict.values())
        if proveedores:
            self.combo_proveedor.set(proveedores[0]['nombre'])

    def cargar_productos(self):
        productos = ProductoController.listar_productos()
        self.productos_dict = {f"{p['codigo']} - {p['nombre']}": p for p in productos}
        self.combo_producto['values'] = list(self.productos_dict.keys())

    def cargar_ultimas_compras(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        compras = CompraController.listar_compras()[:10]
        for c in compras:
            total = c['cantidad'] * c['precio_compra']
            fecha = c['fecha'].strftime("%Y-%m-%d %H:%M") if c['fecha'] else ""
            self.tree.insert("", "end", values=(
                c['id'], c['producto'] or "—", c['proveedor'] or "—",
                f"{c['cantidad']:.3f}", f"${c['precio_compra']:.2f}",
                f"${total:.2f}", fecha
            ))

    def actualizar_info_producto(self, event=None):
        nombre_selec = self.combo_producto.get()
        producto = self.productos_dict.get(nombre_selec)
        if producto:
            tipo = "⚖️ Granel" if producto['tipo'] == 'granel' else "📦 Unidad"
            stock = f"{producto['stock']:.3f} {'kg' if producto['tipo']=='granel' else 'uds'}"
            self.lbl_info.config(text=f"{tipo} | Precio Venta: ${producto['precio_unitario']:.2f} | Stock: {stock}")

    def guardar_compra(self):
        # Obtener datos
        proveedor_nombre = self.combo_proveedor.get()
        id_proveedor = next((pid for pid, n in self.proveedores_dict.items() if n == proveedor_nombre), None)
        
        producto_nombre = self.combo_producto.get()
        producto = self.productos_dict.get(producto_nombre)
        if not producto:
            messagebox.showwarning("⚠️", "Selecciona un producto.")
            return
        id_producto = producto['id']

        try:
            cantidad = float(self.entry_cantidad.get())
            precio = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("❌", "Cantidad y precio deben ser números.")
            return

        nota = self.text_nota.get("1.0", "end-1c").strip()

        # ✅ USAR CONTROLADOR
        exito, mensaje = CompraController.registrar_compra(
            id_producto=id_producto,
            id_proveedor=id_proveedor,
            cantidad=cantidad,
            precio_compra=precio,
            nota=nota
        )

        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, "1.000")
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, "0.00")
            self.text_nota.delete("1.0", tk.END)
            self.lbl_info.config(text="—")
            self.cargar_productos()  # stock actualizado
            self.cargar_ultimas_compras()
        else:
            messagebox.showerror("❌ Error", mensaje)