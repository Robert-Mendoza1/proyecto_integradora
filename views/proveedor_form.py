# views/proveedor_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedor_controller import ProveedorController

class ProveedorForm:
    def __init__(self, parent, proveedor_id=None, callback=None):
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Nuevo Proveedor" if not proveedor_id else "✏️ Editar Proveedor")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()  # Modal

        self.proveedor_id = proveedor_id
        self.callback = callback

        self.create_widgets()
        if proveedor_id:
            self.cargar_datos()

    def create_widgets(self):
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        fields = [
            ("Nombre *", "nombre", 30),
            ("Contacto", "contacto", 30),
            ("Teléfono", "telefono", 20),  # 👈 Campo de teléfono
            ("Email", "email", 30),
            ("Dirección", "direccion", 30)
        ]
        self.entries = {}
        for i, (label, key, width) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            if key == "telefono":
                # ✅ Validar que solo se acepten números
                vcmd = (self.window.register(self.validar_numero), '%P')
                entry = tk.Entry(frame, width=width, validate='key', validatecommand=vcmd)
            else:
                entry = tk.Entry(frame, width=width)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = entry

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy).pack(side="left", padx=5)

    def validar_numero(self, valor):
        """Valida que el campo solo acepte números (enteros)."""
        if valor == "":
            return True  # Permitir campo vacío
        try:
            int(valor)
            return True
        except ValueError:
            return False

    def cargar_datos(self):
        prov = ProveedorController.buscar_proveedor(id_proveedor=self.proveedor_id)
        if prov and len(prov) > 0:
            p = prov[0]
            self.entries['nombre'].insert(0, p['nombre'])
            self.entries['contacto'].insert(0, p['contacto'] or "")
            self.entries['telefono'].insert(0, p['telefono'] or "")
            self.entries['email'].insert(0, p['email'] or "")
            self.entries['direccion'].insert(0, p['direccion'] or "")

    def guardar(self):
        nombre = self.entries['nombre'].get().strip()
        if not nombre:
            messagebox.showwarning("⚠️", "El nombre es obligatorio.", parent=self.window)
            return

        contacto = self.entries['contacto'].get().strip() or None
        telefono = self.entries['telefono'].get().strip() or None
        email = self.entries['email'].get().strip() or None
        direccion = self.entries['direccion'].get().strip() or None

        # ✅ Validar que el teléfono contenga solo números (si no está vacío)
        if telefono and not telefono.isdigit():
            messagebox.showerror("❌ Error", "El teléfono debe contener solo números.", parent=self.window)
            return

        if self.proveedor_id:
            exito, mensaje, _ = ProveedorController.actualizar_proveedor(
                self.proveedor_id, nombre, contacto, telefono, email, direccion
            )
        else:
            exito, mensaje, _ = ProveedorController.crear_proveedor(
                nombre, contacto, telefono, email, direccion
            )

        if exito:
            messagebox.showinfo("✅ Éxito", mensaje, parent=self.window)
            if self.callback:
                self.callback()  # refrescar tabla
            self.window.destroy()
        else:
            messagebox.showerror("❌ Error", mensaje, parent=self.window)