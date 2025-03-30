-- Asigna pedidos aleatorios a clientes, permitiendo múltiples pedidos por cliente
INSERT INTO pedidos (cliente_id, fecha_pedido, monto)
SELECT
    c.cliente_id,
    DATE_ADD('2024-01-01', INTERVAL FLOOR(RAND() * 30) DAY), -- Fecha aleatoria dentro de enero
    ROUND(RAND() * 500, 2) -- Monto aleatorio entre 0 y 500
FROM
    clientes c
CROSS JOIN
    (SELECT 1 UNION SELECT 2 UNION SELECT 3) AS nums -- Genera 1, 2, 3 para múltiples pedidos
ORDER BY
    RAND();