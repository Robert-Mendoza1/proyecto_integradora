from controllers.proveedor_controller import ProveedorController

proveedores = ProveedorController.listar_proveedores()
print(f"Proveedores encontrados: {len(proveedores)}")
for p in proveedores:
    print(f"ID: {p['id']}, Nombre: {p['nombre']}")