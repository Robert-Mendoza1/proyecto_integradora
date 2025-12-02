# views/pendientes_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class PendientesView:
    def __init__(self, parent, usuario_datos):
        self.window = parent
        self.usuario_datos = usuario_datos
        self.window.title("⏳ Usuarios Pendientes")
        self.window.geometry("800x500")

        # ✅ Verificar si el usuario tiene permiso
        if self.usuario_datos['rol'] != 'admin':
            messagebox.showerror("❌ Acceso denegado", "Solo los administradores pueden gestionar usuarios pendientes.")
            self.window.destroy()
            return

        self.create_widgets()
        self.cargar_usuarios_pendientes()

    def create_widgets(self):
        tk.Label(self.window, text="⏳ Usuarios Pendientes de Aprobación", font=("Arial", 14, "bold")).pack(pady=10)

        # Tabla
        columns = ("ID", "Usuario", "Nombre", "Rol", "Fecha Registro")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Usuario", width=120, anchor="w")
        self.tree.column("Nombre", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # ✅ Vincular clic derecho al árbol
        self.tree.bind("<Button-3>", self.mostrar_menu_acciones)

        # Botón de refrescar
        ttk.Button(self.window, text="🔄 Refrescar", command=self.cargar_usuarios_pendientes).pack(pady=10)

    def cargar_usuarios_pendientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuarios = UsuarioController.obtener_usuarios_pendientes()
        for u in usuarios:
            self.tree.insert("", "end", values=(
                u['id'],
                u['nombre_usuario'],
                u['nombre_completo'],
                u['rol'],
                u['fecha_registro'].strftime("%Y-%m-%d %H:%M") if u['fecha_registro'] else "N/A"
            ))

    def mostrar_menu_acciones(self, event):
        """Muestra menú contextual con acciones para usuarios pendientes."""
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
            id_usuario = int(values[0])
        except (ValueError, IndexError):
            return

        # Crear menú contextual
        menu = tk.Menu(self.window, tearoff=0)

        menu.add_command(
            label="✅ Aprobar Usuario",
            command=lambda: self.aprobar_usuario(id_usuario),
            foreground="green"
        )
        menu.add_command(
            label="❌ Rechazar Usuario",
            command=lambda: self.rechazar_usuario(id_usuario),
            foreground="red"
        )

        menu.add_separator()
        menu.add_command(label="❌ Cerrar", command=menu.destroy)

        # Mostrar menú en la posición del clic
        menu.tk_popup(event.x_root, event.y_root)

    def aprobar_usuario(self, id_usuario):
        if messagebox.askyesno("✅ Confirmar", f"¿Aprobar usuario ID {id_usuario}?"):
            exito, mensaje = UsuarioController.aprobar_usuario(id_usuario)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                self.cargar_usuarios_pendientes()
            else:
                messagebox.showerror("❌ Error", mensaje)

    def rechazar_usuario(self, id_usuario):
        if messagebox.askyesno("❌ Confirmar", f"¿Rechazar usuario ID {id_usuario}?"):
            exito, mensaje = UsuarioController.rechazar_usuario(id_usuario)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                self.cargar_usuarios_pendientes()
            else:
                messagebox.showerror("❌ Error", mensaje)