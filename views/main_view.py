# views/main_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class MainView:
    def __init__(self, root, usuario_datos):
        self.root = root
        self.usuario_datos = usuario_datos  # {'id': 1, 'nombre_completo': 'Juan', 'rol': 'admin'}
        self.root.title(f"🛒 Tienda a Granel - Bienvenido, {usuario_datos['nombre_completo']}")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # ✅ Inicializar inventario_window como None
        self.inventario_window = None

        self.create_widgets()

    def create_widgets(self):
        # Barra superior con usuario y logout
        top_bar = tk.Frame(self.root, bg="#2c3e50", height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Label(top_bar, text=f"👤 {self.usuario_datos['nombre_completo']} ({self.usuario_datos['rol']})",
                 fg="white", bg="#2c3e50", font=("Arial", 10)).pack(side="left", padx=20, pady=15)
        ttk.Button(top_bar, text="🚪 Cerrar Sesión", command=self.logout).pack(side="right", padx=20, pady=10)

        # Logo
        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((240, 120), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self.root, image=self.logo).pack(pady=10)
        except (FileNotFoundError, OSError) as e:
            print(f"⚠️ No se pudo cargar el logo: {e}")
            tk.Label(self.root, text="🛒", font=("Arial", 30)).pack(pady=10)

        # Título
        tk.Label(self.root, text="Sistema de Gestión de Tienda", 
                 font=("Arial", 20, "bold"), fg="#2c3e50").pack(pady=10)

        # Botones (con control de roles)
        frame_btns = tk.Frame(self.root)
        frame_btns.pack(pady=20)

        # Botones comunes
        ttk.Button(frame_btns, text="📦 Productos", command=self.abrir_productos,
                   width=20).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(frame_btns, text="👥 Proveedores", command=self.abrir_proveedores,
                   width=20).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(frame_btns, text="📥 Compras", command=self.abrir_compras,
                   width=20).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(frame_btns, text="🛒 Ventas", command=self.abrir_ventas,
                   width=20).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(frame_btns, text="📦 Inventario", command=self.abrir_inventario,
                   width=20).grid(row=2, column=0, padx=10, pady=10)

        # Botones solo para admin
        if self.usuario_datos['rol'] == 'admin':
            ttk.Button(frame_btns, text="📊 Reportes", command=self.abrir_reportes,
                    width=20).grid(row=2, column=1, padx=10, pady=10)
            ttk.Button(frame_btns, text="👥 Usuarios", command=self.abrir_usuarios,
                    width=20).grid(row=3, column=0, padx=10, pady=10)
            # ✅ Nuevo botón para usuarios pendientes
            ttk.Button(frame_btns, text="⏳ Pendientes", command=self.abrir_pendientes,
                    width=20).grid(row=3, column=1, padx=10, pady=10)
        else:
            # Botón deshabilitado para vendedores
            ttk.Button(frame_btns, text="📊 Reportes", state="disabled",
                    width=20).grid(row=2, column=1, padx=10, pady=10)
            ttk.Button(frame_btns, text="👥 Usuarios", state="disabled",
                    width=20).grid(row=3, column=0, padx=10, pady=10)
            ttk.Button(frame_btns, text="⏳ Pendientes", state="disabled",
                    width=20).grid(row=3, column=1, padx=10, pady=10)

        # Pie de página
        tk.Label(self.root, text="© 2025 Tienda a Granel | Proyecto Educativo",
                 font=("Arial", 10), fg="gray").pack(side="bottom", pady=10)

    def logout(self):
        if messagebox.askyesno("🚪 Cerrar Sesión", "¿Cerrar sesión?"):
            self.root.destroy()
            # Abrir login nuevamente
            from views.login_view import LoginView
            login_root = tk.Tk()
            LoginView(login_root)
            login_root.mainloop()

    # Métodos de apertura de vistas
    def abrir_productos(self):
        from views.producto_view import ProductoView
        ProductoView(tk.Toplevel(self.root))

    def abrir_proveedores(self):
        from views.proveedor_view import ProveedorView
        ProveedorView(tk.Toplevel(self.root))

    def abrir_compras(self):
        from views.compra_view import CompraView
        # Pasar la referencia de la ventana de inventario (puede ser None)
        CompraView(tk.Toplevel(self.root), inventario_window=self.inventario_window)
    
    
    def abrir_ventas(self):
        from views.venta_view import VentaView
        VentaView(tk.Toplevel(self.root))

    def abrir_inventario(self):
        from views.inventario_view import InventarioView
        # Cerrar ventana anterior si existe
        if self.inventario_window and self.inventario_window.winfo_exists():
            self.inventario_window.destroy()
        # Crear nueva ventana
        self.inventario_window = tk.Toplevel(self.root)
        InventarioView(self.inventario_window)

    def abrir_reportes(self):
        from views.reporte_view import ReporteView
        ReporteView(tk.Toplevel(self.root))

    def abrir_usuarios(self):
        from views.usuario_admin_view import UsuarioAdminView
        UsuarioAdminView(tk.Toplevel(self.root), self.usuario_datos)

    def abrir_pendientes(self):
        from views.pendientes_view import PendientesView
        PendientesView(tk.Toplevel(self.root), self.usuario_datos)