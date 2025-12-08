# views/proveedor_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedor_controller import ProveedorController

class ProveedorView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("👥 Gestión de Proveedores")
        self.window.geometry("900x550")
        self.window.resizable(False, False)

        self.proveedor_seleccionado_id = None
        self.create_widgets()
        self.cargar_proveedores()

    def create_widgets(self):
        # Frame superior: título y botón nuevo
        top_frame = tk.Frame(self.window)
        top_frame.pack(fill="x", padx=15, pady=10)
        tk.Label(top_frame, text="👥 Proveedores", font=("Arial", 16, "bold")).pack(side="left")
        
        ttk.Button(top_frame, text="➕ Nuevo Proveedor", command=self.abrir_formulario).pack(side="right")

        # Frame central: tabla
        frame_tabla = tk.Frame(self.window)
        frame_tabla.pack(fill="both", expand=True, padx=15)

        # Tabla con columnas
        columns = ("ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w" if col != "ID" else "center")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=180)
        self.tree.column("Dirección", width=200)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ✅ Vincular clic derecho al árbol
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

        self.cargar_proveedores()

    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        proveedores = ProveedorController.listar_proveedores()
        for p in proveedores:
            self.tree.insert("", "end", values=(
                p['id'], p['nombre'], p['contacto'] or "—", p['telefono'] or "—", p['email'] or "—", p['direccion'] or "—"
            ))

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
            id_prov = int(values[0])
        except (ValueError, IndexError):
            return

        # Crear menú contextual
        menu = tk.Menu(self.window, tearoff=0)

        menu.add_command(
            label="✏️ Editar Proveedor",
            command=lambda: self.editar_proveedor_directo(id_prov),
            foreground="blue"
        )
        menu.add_command(
            label="🗑️ Eliminar Proveedor",
            command=lambda: self.eliminar_proveedor_directo(id_prov),
            foreground="red"
        )

        menu.add_separator()
        menu.add_command(label="❌ Cerrar", command=menu.destroy)

        # Mostrar menú en la posición del clic
        menu.tk_popup(event.x_root, event.y_root)

    def editar_proveedor_directo(self, id_proveedor):
        """Editar proveedor directamente."""
        from views.proveedor_form import ProveedorForm
        ProveedorForm(self.window, proveedor_id=id_proveedor, callback=self.cargar_proveedores)

    def eliminar_proveedor_directo(self, id_proveedor):
        """Eliminar proveedor directamente."""
        if messagebox.askyesno(
            "🗑️ Confirmar eliminación",
            f"¿Eliminar proveedor ID {id_proveedor}?\nLos productos asociados quedarán sin proveedor.",
            parent=self.window
        ):
            exito, mensaje = ProveedorController.eliminar_proveedor(id_proveedor)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=self.window)
                self.cargar_proveedores()
            else:
                messagebox.showerror("❌ Error", mensaje, parent=self.window)

    def abrir_formulario(self):
        """Abre formulario para crear nuevo proveedor."""
        from views.proveedor_form import ProveedorForm
        ProveedorForm(self.window, callback=self.cargar_proveedores)