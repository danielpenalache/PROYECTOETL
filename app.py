import pandas as pd
from sqlalchemy import create_engine


URL_BASE_DE_DATOS = 'postgresql://postgres:12345@localhost/northwind'  #CONEXION USANDO SQLALCHEMY
engine = create_engine(URL_BASE_DE_DATOS)

consulta_pedidos_por_cliente = """
SELECT c.customer_id, c.company_name, COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_orders DESC;
"""
consulta_productos = "SELECT product_id, product_name FROM products" 
consulta_detalles_pedidos = "SELECT product_id, quantity, discount FROM order_details"   #CONSULTAS A USAR DE LA BASE
consulta_empleados = "SELECT first_name, birth_date FROM employees" 

df_pedidos_por_cliente = pd.read_sql(consulta_pedidos_por_cliente, engine)
df_productos = pd.read_sql(consulta_productos, engine)
df_detalles_pedidos = pd.read_sql(consulta_detalles_pedidos, engine) # ENGINE ES NECESARIO PARA QUE PANDAS PUEDA EJECUTAR CONSULTAS SOBRE LA BASE DE DATOS
df_empleados = pd.read_sql(consulta_empleados, engine)

conteo_productos = len(df_productos)
conteo_detalles_pedidos = len(df_detalles_pedidos) #LEN ES LONGITUD, NUMERO DE ELEMENTOS DE UN OBJETO, ES ESTE CASO EL CONTEO.
conteo_empleados = len(df_empleados)
conteo_pedidos =len(df_pedidos_por_cliente)

print(f"Datos extraidos de la tabla productos: {conteo_productos} filas")
print(f"Datos extraidos de la tabla detalles_pedidos: {conteo_detalles_pedidos} filas")  #IMPRIME EN CONSOLA
print(f"Datos extraidos de la tabla empleados: {conteo_empleados} filas")
print(f"Datos extraidos de la tabla clientes: {conteo_pedidos}filas")

#IMPRIME DATOS DE CONTEO EN HTML
contenido_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conteo de Datos</title>
</head>
<body>
    <h1>Conteo de Datos Extraidos</h1>
    <p><strong>Datos extraidos de la tabla productos:</strong> {conteo_productos} filas</p>   
    <p><strong>Datos extraidos de la tabla detalles_pedidos:</strong> {conteo_detalles_pedidos} filas</p>  
    <p><strong>Datos extraidos de la tabla empleados:</strong> {conteo_empleados} filas</p>
    <p><strong>Datos extraidos de la tabla clientes:</strong> {conteo_pedidos} filas</p>
</body>
</html>
"""


with open('conteo_datos.html', 'w') as archivo:   #EXPORTA LOS DATOS DE CONTEO COMO HTML
    archivo.write(contenido_html)


df_combinado = df_detalles_pedidos.merge(df_productos, on='product_id') # ES COMO UN JOIN DONDE SE MEZCLAN LAS FILAS DE DETALLES PEDIDOS Y PRODUCTOS


df_cantidad_productos = df_combinado.groupby('product_name').agg({   #AGRUPA POR NOMBRE DE PRODUCTO Y SUMA TODAS LAS CANTIDADES, DE EL ATRIBUTO QUANTITY
    'quantity': 'sum'
}).reset_index()


df_empleados_ordenados = df_empleados.sort_values(by='birth_date')   #ORGANIZAR VALORES DE FECHA DE NACIMIENTO PARA IDENTIFICAR EMPLEADO MAS VIEJO

df_pedidos_por_cliente.to_csv('pedidos_por_cliente.csv', index=False)
df_cantidad_productos.to_csv('cantidad_productos.csv', index=False)     #EXPORTA LOS DATAFRAMES A CSV, QUE ES EL FORMATO DE FILAS Y COLUMNAS (YA AVERIGUE, NO ES EXCEL EN SI)
df_empleados_ordenados.to_csv('empleados_ordenados.csv', index=False)
df_detalles_pedidos.to_csv('detalles_pedidos.csv', index=False) 