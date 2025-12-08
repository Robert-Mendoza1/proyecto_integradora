# views/reporte_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController
from controllers.compra_controller import CompraController
from PIL import Image, ImageTk
import os
import csv
from datetime import datetime, timedelta

class ReporteView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("📊 Reportes del Sistema")
        self.window.geometry("1000x650")
        self.window.resizable(False, False)

        self.create_widgets()
        self.cargar_datos_iniciales()

    def create_widgets(self):
        # === LOGO ===
        logo_frame = tk.Frame(self.window, bg="#f0f4f8", height=70)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((50, 50), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo, bg="#f0f4f8").pack(side="left", padx=20)
        except:
            tk.Label(logo_frame, text="📊 REPORTES", font=("Arial", 18, "bold"), 
                     fg="#2c3e50", bg="#f0f4f8").pack(side="left", padx=20)

        # === PESTAÑAS ===
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Pestaña 1: Resumen del Día
        self.tab_resumen = tk.Frame(self.notebook)
        self.notebook.add(self.tab_resumen, text="📅 Resumen del Día")
        self.crear_tab_resumen()

        # Pestaña 2: Reporte de Ventas
        self.tab_ventas = tk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="💰 Ventas por Fecha")
        self.crear_tab_ventas()

        # Pestaña 3: Inventario
        self.tab_inventario = tk.Frame(self.notebook)
        self.notebook.add(self.tab_inventario, text="📦 Inventario")
        self.crear_tab_inventario()

        # Pestaña 4: Exportar
        self.tab_exportar = tk.Frame(self.notebook)
        self.notebook.add(self.tab_exportar, text="📥 Exportar Datos")
        self.crear_tab_exportar()

    def crear_tab_resumen(self):
        """Pestaña de resumen del día."""
        frame = tk.Frame(self.tab_resumen, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Título
        tk.Label(frame, text="Resumen del Día", font=("Arial", 16, "bold")).pack(pady=10)

        # Cards de resumen
        card_frame = tk.Frame(frame)
        card_frame.pack(fill="x", pady=10)

        # Ventas del día
        card1 = tk.LabelFrame(card_frame, text="Ventas Hoy", font=("Arial", 12, "bold"))
        card1.pack(side="left", fill="y", padx=10)
        self.lbl_ventas_hoy = tk.Label(card1, text="$0.00", font=("Arial", 20, "bold"), fg="green")
        self.lbl_ventas_hoy.pack(pady=10)
        tk.Label(card1, text="Total vendido hoy", font=("Arial", 9)).pack()

        # Ventas totales
        card2 = tk.LabelFrame(card_frame, text="Ventas Totales", font=("Arial", 12, "bold"))
        card2.pack(side="left", fill="y", padx=10)
        self.lbl_ventas_totales = tk.Label(card2, text="0", font=("Arial", 20, "bold"), fg="blue")
        self.lbl_ventas_totales.pack(pady=10)
        tk.Label(card2, text="Productos vendidos", font=("Arial", 9)).pack()

        # Productos vendidos
        card3 = tk.LabelFrame(card_frame, text="Productos", font=("Arial", 12, "bold"))
        card3.pack(side="left", fill="y", padx=10)
        self.lbl_productos_vendidos = tk.Label(card3, text="0", font=("Arial", 20, "bold"), fg="purple")
        self.lbl_productos_vendidos.pack(pady=10)
        tk.Label(card3, text="Diferentes productos", font=("Arial", 9)).pack()

        # Últimas ventas
        tk.Label(frame, text="Últimas Ventas", font=("Arial", 12, "bold")).pack(pady=(20, 10))
        columns = ("ID", "Producto", "Cantidad", "Precio", "Total", "Fecha")
        self.tree_ultimas_ventas = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        for col in columns:
            self.tree_ultimas_ventas.heading(col, text=col)
            self.tree_ultimas_ventas.column(col, width=100, anchor="center")
        self.tree_ultimas_ventas.column("Producto", width=150, anchor="w")
        self.tree_ultimas_ventas.pack(fill="x", pady=10)

    def crear_tab_ventas(self):
        """Pestaña de reporte de ventas por rango de fechas."""
        frame = tk.Frame(self.tab_ventas, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Filtros
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=10)

        tk.Label(filter_frame, text="Fecha Inicio:").pack(side="left", padx=(0, 5))
        self.entry_fecha_inicio = tk.Entry(filter_frame, width=15)
        self.entry_fecha_inicio.pack(side="left", padx=5)
        self.entry_fecha_inicio.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))

        tk.Label(filter_frame, text="Fecha Fin:").pack(side="left", padx=(10, 5))
        self.entry_fecha_fin = tk.Entry(filter_frame, width=15)
        self.entry_fecha_fin.pack(side="left", padx=5)
        self.entry_fecha_fin.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Button(filter_frame, text="🔍 Filtrar", command=self.cargar_ventas_por_fecha).pack(side="left", padx=10)
        ttk.Button(filter_frame, text="↺ Hoy", command=self.filtrar_hoy).pack(side="left")

        # Tabla de ventas
        columns = ("ID", "Producto", "Cantidad", "Precio", "Total", "Fecha")
        self.tree_ventas_fecha = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree_ventas_fecha.heading(col, text=col)
            self.tree_ventas_fecha.column(col, width=100, anchor="center")
        self.tree_ventas_fecha.column("Producto", width=150, anchor="w")
        self.tree_ventas_fecha.pack(fill="both", expand=True, pady=10)

        # Scrollbars
        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree_ventas_fecha.yview)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree_ventas_fecha.xview)
        self.tree_ventas_fecha.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def crear_tab_inventario(self):
        """Pestaña de reporte de inventario."""
        frame = tk.Frame(self.tab_inventario, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Filtros
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=10)

        tk.Label(filter_frame, text="Filtrar por:").pack(side="left", padx=(0, 10))
        self.combo_filtro_stock = ttk.Combobox(filter_frame, values=["Todos", "Bajo Stock", "Sin Stock"], state="readonly", width=15)
        self.combo_filtro_stock.set("Todos")
        self.combo_filtro_stock.pack(side="left", padx=5)
        self.combo_filtro_stock.bind("<<ComboboxSelected>>", self.cargar_inventario_reporte)

        ttk.Button(filter_frame, text="🔄 Refrescar", command=self.cargar_inventario_reporte).pack(side="right")

        # Tabla de inventario
        columns = ("ID", "Código", "Nombre", "Tipo", "Precio", "Stock", "Proveedor", "Fecha Creación")
        self.tree_inventario = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree_inventario.heading(col, text=col)
            self.tree_inventario.column(col, width=100, anchor="center")
        self.tree_inventario.column("Nombre", width=150, anchor="w")
        self.tree_inventario.pack(fill="both", expand=True, pady=10)

        # Scrollbars
        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree_inventario.yview)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree_inventario.xview)
        self.tree_inventario.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def crear_tab_exportar(self):
        """Pestaña de exportación de datos."""
        frame = tk.Frame(self.tab_exportar, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Exportar Datos", font=("Arial", 16, "bold")).pack(pady=20)

        # Botones de exportación
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="📥 Ventas (CSV)", command=self.exportar_ventas_csv).pack(pady=5)
        ttk.Button(btn_frame, text="📥 Inventario (CSV)", command=self.exportar_inventario_csv).pack(pady=5)
        ttk.Button(btn_frame, text="📥 Compras (CSV)", command=self.exportar_compras_csv).pack(pady=5)
        ttk.Button(btn_frame, text="📥 Proveedores (CSV)", command=self.exportar_proveedores_csv).pack(pady=5)

        # Nota
        tk.Label(frame, text="Los archivos se guardarán en formato CSV,\ncompatible con Excel y Google Sheets.", 
                 font=("Arial", 10), fg="gray").pack(pady=20)

    def cargar_datos_iniciales(self):
        """Carga los datos iniciales para el resumen."""
        try:
            # Ventas del día
            total_hoy = VentaController.total_ventas_hoy()
            self.lbl_ventas_hoy.config(text=f"${total_hoy:.2f}")

            # Últimas ventas
            ventas = VentaController.listar_ventas()[:10]  # últimas 10
            for item in self.tree_ultimas_ventas.get_children():
                self.tree_ultimas_ventas.delete(item)
            for v in ventas:
                self.tree_ultimas_ventas.insert("", "end", values=(
                    v['id'],
                    v['producto'],
                    f"{v['cantidad']:.3f}",
                    f"${v['precio_venta']:.2f}",
                    f"${v['total']:.2f}",
                    v['fecha'].strftime("%Y-%m-%d %H:%M") if v['fecha'] else "N/A"
                ))

            # Contadores
            self.lbl_ventas_totales.config(text=len(ventas))
            productos_vendidos = len(set(v['producto'] for v in ventas if v['producto']))
            self.lbl_productos_vendidos.config(text=productos_vendidos)

        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar los datos iniciales:\n{e}")

    def cargar_ventas_por_fecha(self):
        """Carga ventas en un rango de fechas."""
        try:
            fecha_inicio = self.entry_fecha_inicio.get().strip()
            fecha_fin = self.entry_fecha_fin.get().strip()

            ventas = VentaController.ventas_por_fecha(fecha_inicio, fecha_fin)

            for item in self.tree_ventas_fecha.get_children():
                self.tree_ventas_fecha.delete(item)

            for v in ventas:
                self.tree_ventas_fecha.insert("", "end", values=(
                    v['id'],
                    v['producto'],
                    f"{v['cantidad']:.3f}",
                    f"${v['precio_venta']:.2f}",
                    f"${v['total']:.2f}",
                    v['fecha'].strftime("%Y-%m-%d %H:%M") if v['fecha'] else "N/A"
                ))

        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudieron cargar las ventas:\n{e}")

    def filtrar_hoy(self):
        """Filtra ventas del día actual."""
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_inicio.insert(0, hoy)
        self.entry_fecha_fin.delete(0, tk.END)
        self.entry_fecha_fin.insert(0, hoy)
        self.cargar_ventas_por_fecha()

    def cargar_inventario_reporte(self, event=None):
        """Carga inventario con filtros."""
        try:
            productos = ProductoController.listar_productos()
            filtro = self.combo_filtro_stock.get()

            # ✅ Filtrar según opción seleccionada
            if filtro == "Bajo Stock":
                # ✅ Filtrar por stock actual < stock_bajo Y stock > 0
                productos = [p for p in productos if p['stock'] < p.get('stock_bajo', 5.0) and p['stock'] > 0]
            elif filtro == "Sin Stock":
                productos = [p for p in productos if p['stock'] <= 0]

            # Actualizar tabla
            for item in self.tree_inventario.get_children():
                self.tree_inventario.delete(item)

            for p in productos:
                self.tree_inventario.insert("", "end", values=(
                    p['id'],
                    p['codigo'],
                    p['nombre'],
                    "📦" if p['tipo'] == 'unidad' else "⚖️",
                    f"${p['precio_unitario']:.2f}",
                    f"{p['stock']:.3f}",
                    p.get('proveedor', '—'),
                    p['fecha_creacion'].strftime("%Y-%m-%d") if p['fecha_creacion'] else "N/A"
                ))

        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo cargar el inventario:\n{e}", parent=self.window)

    def exportar_ventas_csv(self):
        """Exporta ventas a CSV."""
        try:
            ventas = VentaController.listar_ventas()
            if not ventas:
                messagebox.showinfo("ℹ️", "No hay ventas para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                title="Guardar Ventas",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
            )
            if not archivo:
                return

            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=ventas[0].keys())
                writer.writeheader()
                writer.writerows(ventas)

            messagebox.showinfo("✅ Éxito", f"Ventas exportadas a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar:\n{e}")

    def exportar_inventario_csv(self):
        """Exporta inventario a CSV."""
        try:
            productos = ProductoController.listar_productos()
            if not productos:
                messagebox.showinfo("ℹ️", "No hay productos para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                title="Guardar Inventario",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
            )
            if not archivo:
                return

            # Adaptar productos para exportar
            datos = []
            for p in productos:
                datos.append({
                    "ID": p['id'],
                    "Código": p['codigo'],
                    "Nombre": p['nombre'],
                    "Tipo": p['tipo'],
                    "Precio Venta": p['precio_unitario'],
                    "Stock": p['stock'],
                    "Proveedor": p.get('proveedor', '—'),
                    "Fecha Creación": p['fecha_creacion'].strftime("%Y-%m-%d") if p['fecha_creacion'] else "N/A"
                })

            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                writer.writeheader()
                writer.writerows(datos)

            messagebox.showinfo("✅ Éxito", f"Inventario exportado a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar:\n{e}")

    def exportar_compras_csv(self):
        """Exporta compras a CSV."""
        try:
            from controllers.compra_controller import CompraController
            compras = CompraController.listar_compras()
            if not compras:
                messagebox.showinfo("ℹ️", "No hay compras para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                title="Guardar Compras",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
            )
            if not archivo:
                return

            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=compras[0].keys())
                writer.writeheader()
                writer.writerows(compras)

            messagebox.showinfo("✅ Éxito", f"Compras exportadas a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar:\n{e}")

    def exportar_proveedores_csv(self):
        """Exporta proveedores a CSV."""
        try:
            from controllers.proveedor_controller import ProveedorController
            proveedores = ProveedorController.listar_proveedores()
            if not proveedores:
                messagebox.showinfo("ℹ️", "No hay proveedores para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                title="Guardar Proveedores",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
            )
            if not archivo:
                return

            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=proveedores[0].keys())
                writer.writeheader()
                writer.writerows(proveedores)

            messagebox.showinfo("✅ Éxito", f"Proveedores exportados a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo exportar:\n{e}")