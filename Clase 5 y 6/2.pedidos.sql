ALTER TABLE pedidos ADD COLUMN tipo_mora ENUM('Mora Blanda', 'Mora Dura') DEFAULT 'Mora Blanda';

ALTER TABLE pedidos ADD COLUMN numero_cuotas INT NOT NULL DEFAULT 1;

CREATE TABLE IF NOT EXISTS cuotas (
    cuota_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    numero_cuota INT NOT NULL,
    monto_cuota DECIMAL(10,2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    pagado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id) ON DELETE CASCADE
);
