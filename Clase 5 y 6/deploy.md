Instrucciones para inicializar la aplicación:

1 - Validar ejecución del servicio/proceso de base de datos
2 - Terminar proceso MariaDB, de ser necesario
3 - Ejecutar ambiente virtual:
    pipenv shell
4 - Si es la primera ejecución, o si hay nuevas librerías/dependencias ejecutar:
    pipenv install
5 - Ejecutar backend:
    python crud.py
6 - Abrir aplicación a través del navegador:
    http://127.0.0.1:5000/

Mejoras pendientes:

- Eliminar clientes que tengan pedidos, restricción actual de llave foránea.
- Ordenar los valores de pedidos mediante columnas.
- Revisar porque no se está poblando la tabla cuotas.

Mejorar propuestas: 
- TODO: Generar nuevas métricas
- TODO: Los pedidos, generar una nueva tabla de cobros/cobranza
- TODO: Estado de pedidos - cobrados o por cobrar

- () Compromiso de pago de 10 cuotas, 100, primera cuota 01/01/25, ¿En marzo a pagado todas las cuotas?
- () Clientes que han pagado todas las cuotas.
- (OK) Clientes con tipo de mora: Mora blanda, Mora dura.
- () Permanencia.
- () Cumplimiento.


