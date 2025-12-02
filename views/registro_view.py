# views/registro_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class RegistroView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("📝 Registrar Usuario")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        # Centrar ventana
        self.window.eval('tk::PlaceWindow . center')

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="📝 Registrar Nuevo Usuario", font=("Arial", 14, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.window, padx=30, pady=10)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Nombre de Usuario:", anchor="w").pack(fill="x", pady=5)
        self.entry_usuario = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_usuario.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Nombre Completo:", anchor="w").pack(fill="x", pady=5)
        self.entry_nombre = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_nombre.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Contraseña:", anchor="w").pack(fill="x", pady=5)
        self.entry_contrasena = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.entry_contrasena.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Confirmar Contraseña:", anchor="w").pack(fill="x", pady=5)
        self.entry_contrasena_conf = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.entry_contrasena_conf.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Rol:", anchor="w").pack(fill="x", pady=5)
        self.combo_rol = ttk.Combobox(form_frame, values=["vendedor", "admin"], state="readonly", width=20)
        self.combo_rol.set("vendedor")
        self.combo_rol.pack(fill="x", pady=5)

        # Botones
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="💾 Registrar", command=self.registrar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.volver_al_login).pack(side="left", padx=5)

    def registrar(self):
        usuario = self.entry_usuario.get().strip()
        nombre = self.entry_nombre.get().strip()
        contrasena = self.entry_contrasena.get()
        contrasena_conf = self.entry_contrasena_conf.get()
        rol = self.combo_rol.get()

        if contrasena != contrasena_conf:
            messagebox.showerror("❌ Error", "Las contraseñas no coinciden.", parent=self.window)
            return

        exito, mensaje, _ = UsuarioController.crear_usuario(usuario, nombre, contrasena, rol)

        if exito:
            messagebox.showinfo("✅ Éxito", mensaje, parent=self.window)
            # Cerrar registro y volver al login
            self.window.destroy()
            from views.login_view import LoginView
            login_window = tk.Tk()
            LoginView(login_window)
            login_window.mainloop()
        else:
            messagebox.showerror("❌ Error", mensaje, parent=self.window)

    def volver_al_login(self):
        """Cerrar ventana actual y abrir login."""
        self.window.destroy()
        from views.login_view import LoginView
        login_window = tk.Tk()
        LoginView(login_window)
        login_window.mainloop()