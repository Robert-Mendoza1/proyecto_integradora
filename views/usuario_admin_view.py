# views/usuario_admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController
from views.editar_usuario_view import EditarUsuarioView

class UsuarioAdminView:
    def __init__(self, parent, usuario_datos):
        self.window = parent
        self.usuario_datos = usuario_datos  # {'id': 1, 'nombre_completo': 'Juan', 'rol': 'admin'}
        self.window.title("👥 Administración de Usuarios")
        self.window.geometry("900x500")

        # ✅ Verificar si el usuario tiene permiso
        if self.usuario_datos['rol'] != 'admin':
            messagebox.showerror("❌ Acceso denegado", "Solo los administradores pueden gestionar usuarios.")
            self.window.destroy()
            return

        self.create_widgets()
        self.cargar_usuarios()

    def create_widgets(self):
        tk.Label(self.window, text="👥 Usuarios del Sistema", font=("Arial", 14, "bold")).pack(pady=10)

        # Tabla
        columns = ("ID", "Usuario", "Nombre", "Rol", "Estado")
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
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

    def cargar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuarios = UsuarioController.listar_usuarios()
        for u in usuarios:
            estado = "✅ Activo" if u['activo'] else "❌ Inactivo"
            self.tree.insert("", "end", values=(
                u['id'],
                u['nombre_usuario'],
                u['nombre_completo'],
                u['rol'],
                estado
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
            id_usuario = int(values[0])
            rol_usuario = values[3]  # Rol está en la columna 3
            estado = values[4]  # Estado está en la columna 4
        except (ValueError, IndexError):
            return

        # ✅ No permitir que un admin se elimine a sí mismo
        if id_usuario == self.usuario_datos['id']:
            messagebox.showwarning("⚠️ Acción no permitida", "No puedes modificarte a ti mismo.")
            return

        # Crear menú contextual
        menu = tk.Menu(self.window, tearoff=0)

        # ✅ Opción para editar usuario
        menu.add_command(
            label="✏️ Editar Usuario",
            command=lambda: self.editar_usuario_directo(id_usuario),
            foreground="blue"
        )

        if "Activo" in estado:
            # Si está activo, mostrar opción para desactivar
            menu.add_command(
                label="🗑️ Desactivar Usuario",
                command=lambda: self.desactivar_usuario_directo(id_usuario),
                foreground="red"
            )
        else:
            # Si está inactivo, mostrar opción para reactivar
            menu.add_command(
                label="✅ Reactivar Usuario",
                command=lambda: self.reactivar_usuario_directo(id_usuario),
                foreground="green"
            )

        menu.add_separator()
        menu.add_command(label="❌ Cerrar", command=menu.destroy)

        # Mostrar menú en la posición del clic
        menu.tk_popup(event.x_root, event.y_root)

    def editar_usuario_directo(self, id_usuario):
        """Abrir ventana para editar usuario."""
        # Obtener datos del usuario
        usuarios = UsuarioController.listar_usuarios()
        usuario = None
        for u in usuarios:
            if u['id'] == id_usuario:
                usuario = u
                break

        if not usuario:
            messagebox.showerror("❌ Error", "Usuario no encontrado.")
            return

        # Abrir ventana de edición
        editar_window = tk.Toplevel(self.window)
        EditarUsuarioView(editar_window, usuario, callback=self.cargar_usuarios)

    def desactivar_usuario_directo(self, id_usuario):
        # ✅ No permitir que un admin se elimine a sí mismo
        if id_usuario == self.usuario_datos['id']:
            messagebox.showwarning("⚠️ Acción no permitida", "No puedes desactivarte a ti mismo.")
            return

        if messagebox.askyesno("🗑️ Confirmar", f"¿Desactivar usuario ID {id_usuario}?"):
            exito, mensaje = UsuarioController.eliminar_usuario(id_usuario)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                self.cargar_usuarios()
            else:
                messagebox.showerror("❌ Error", mensaje)

    def reactivar_usuario_directo(self, id_usuario):
        if messagebox.askyesno("✅ Confirmar", f"¿Reactivar usuario ID {id_usuario}?"):
            exito, mensaje = UsuarioController.reactivar_usuario(id_usuario)
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                self.cargar_usuarios()
            else:
                messagebox.showerror("❌ Error", mensaje)