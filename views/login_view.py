# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController
from PIL import Image, ImageTk
import os

class LoginView:
    def __init__(self, parent):
        self.window = parent
        self.window.title("🔒 Iniciar Sesión")
        self.window.geometry("400x600")
        self.window.resizable(False, False)

        # Centrar ventana
        self.window.eval('tk::PlaceWindow . center')

        self.usuario_actual = None
        self.create_widgets()

    def create_widgets(self):
        # Logo
        try:
            logo_path = os.path.join("assets", "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((100, 100), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self.window, image=self.logo).pack(pady=20)
        except (FileNotFoundError, OSError) as e:
            print(f"⚠️ No se pudo cargar el logo: {e}")
            tk.Label(self.window, text="🔒", font=("Arial", 30)).pack(pady=20)

        # Título
        tk.Label(self.window, text="Sistema de Tienda", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(self.window, text="Iniciar Sesión", font=("Arial", 12)).pack(pady=5)

        # Formulario
        form_frame = tk.Frame(self.window, padx=50, pady=20)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Usuario:", anchor="w").pack(fill="x", pady=5)
        self.entry_usuario = tk.Entry(form_frame, font=("Arial", 12))
        self.entry_usuario.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Contraseña:", anchor="w").pack(fill="x", pady=5)
        self.entry_contrasena = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.entry_contrasena.pack(fill="x", pady=5)

        # Botones
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="🔐 Iniciar Sesión", command=self.login).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="📝 Registrarse", command=self.registrarse).pack(fill="x", pady=5)

        # Enlace para recuperar contraseña (futuro)
        tk.Label(self.window, text="¿Olvidaste tu contraseña?", fg="blue", cursor="hand2").pack(pady=10)

    def login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get()

        exito, mensaje, datos = UsuarioController.validar_login(usuario, contrasena)

        if exito:
            self.usuario_actual = datos
            messagebox.showinfo("✅ Éxito", f"Bienvenido, {datos['nombre_completo']} ({datos['rol']})")
            # Cerrar login y abrir app principal
            self.window.destroy()
            from views.main_view import MainView
            root = tk.Tk()
            MainView(root, usuario_datos=datos)
            root.mainloop()
        else:
            messagebox.showerror("❌ Error", mensaje)

    def registrarse(self):
        from views.registro_view import RegistroView
        # Cerrar login
        self.window.destroy()
        # Abrir registro
        registro_window = tk.Tk()
        RegistroView(registro_window)
        registro_window.mainloop()