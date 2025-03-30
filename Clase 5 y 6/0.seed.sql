-- Crea la base de datos si no existe
CREATE DATABASE IF NOT EXISTS fernando_cortes;

-- Usa la base de datos recién creada
USE fernando_cortes;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pedidos (ejemplo de relación)
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    fecha_pedido DATE,
    monto DECIMAL(10, 2),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

-- Insertar datos de ejemplo en la tabla clientes
INSERT INTO clientes (nombre, apellido, email, telefono, direccion) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '123-456-7890', 'Calle 123, Ciudad'),
('María', 'Gómez', 'maria.gomez@example.com', '987-654-3210', 'Avenida 456, Pueblo'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@example.com', '555-123-4567', 'Plaza 789, Villa');

-- Insertar datos de ejemplo en la tabla pedidos
INSERT INTO pedidos (cliente_id, fecha_pedido, monto) VALUES
(1, '2024-01-10', 150.00),
(2, '2024-01-15', 220.50),
(1, '2024-01-20', 75.25),
(3, '2024-01-25', 300.00);

-- Consultas de ejemplo
-- Seleccionar todos los clientes
SELECT * FROM clientes;

-- Seleccionar pedidos de un cliente específico
SELECT * FROM pedidos WHERE cliente_id = 1;

-- Contar el número de clientes
SELECT COUNT(*) FROM clientes;