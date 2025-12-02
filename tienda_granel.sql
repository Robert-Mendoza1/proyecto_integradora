CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo ENUM('unidad', 'granel') NOT NULL DEFAULT 'unidad',
    precio_unitario DECIMAL(10,2) NOT NULL,
    stock DECIMAL(10,3) NOT NULL DEFAULT 0.000,  -- permite decimales (para gramos)
    id_proveedor INT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id) ON DELETE SET NULL
);
CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_proveedor INT,
    cantidad DECIMAL(10,3) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    nota TEXT,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id) ON DELETE SET NULL
);
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    tipo_venta ENUM('unidad', 'granel') NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);