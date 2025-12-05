# views/editar_usuario_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class EditarUsuarioView:
    def __init__(self, parent, usuario_datos, callback=None):
        self.window = parent
        self.usuario_datos = usuario_datos  # Datos del usuario a editar
        self.callback = callback
        self.window.title("✏️ Editar Usuario")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        # Centrar ventana manualmente
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (self.window.winfo_reqwidth() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (self.window.winfo_reqheight() // 2)
        self.window.geometry(f"+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="✏️ Editar Usuario", font=("Arial", 14, "bold")).pack(pady=15)

        form_frame = tk.Frame(self.window, padx=30, pady=10)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Nombre de Usuario:", anchor="w").pack(fill="x", pady=5)
        self.entry_usuario = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_usuario.pack(fill="x", pady=5)
        self.entry_usuario.insert(0, self.usuario_datos['nombre_usuario'])
        self.entry_usuario.config(state="readonly")  # No permitir cambiar nombre de usuario

        tk.Label(form_frame, text="Nombre Completo:", anchor="w").pack(fill="x", pady=5)
        self.entry_nombre = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_nombre.pack(fill="x", pady=5)
        self.entry_nombre.insert(0, self.usuario_datos['nombre_completo'])

        tk.Label(form_frame, text="Rol:", anchor="w").pack(fill="x", pady=5)
        self.combo_rol = ttk.Combobox(form_frame, values=["vendedor", "admin"], state="readonly", width=20)
        self.combo_rol.pack(fill="x", pady=5)
        self.combo_rol.set(self.usuario_datos['rol'])

        # Botones
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy).pack(side="left", padx=5)

    def guardar(self):
        nombre_completo = self.entry_nombre.get().strip()
        rol = self.combo_rol.get()

        if not nombre_completo:
            messagebox.showwarning("⚠️", "El nombre completo es obligatorio.")
            return

        if rol not in ["admin", "vendedor"]:
            messagebox.showerror("❌", "Rol inválido.")
            return

        exito, mensaje = UsuarioController.actualizar_usuario(
            id_usuario=self.usuario_datos['id'],
            nombre_completo=nombre_completo,
            rol=rol
        )

        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            if self.callback:
                self.callback()  # Refrescar tabla
            self.window.destroy()
        else:
            messagebox.showerror("❌ Error", mensaje)