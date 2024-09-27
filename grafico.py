import pandas as pd
import plotly.express as px   #LIBRERIA QUE GRAFICA


df_cantidad_productos = pd.read_csv('cantidad_productos.csv')
df_empleados_ordenados = pd.read_csv('empleados_ordenados.csv')
df_detalles_pedidos = pd.read_csv('detalles_pedidos.csv')              #SE IMPORTAN LOS CSV PARA USARLOS EN GRAFICAS
df_pedidos_por_cliente = pd.read_csv('pedidos_por_cliente.csv')

df_empleados_ordenados['edad'] = pd.to_datetime('today').year - pd.to_datetime(df_empleados_ordenados['birth_date']).dt.year  #CALCULO EDAD EMPLEADOS

fig1 = px.pie(      #PIE SIGNIFICA TORTA
    df_empleados_ordenados, 
    names='first_name', 
    values='edad', 
    title='Edad de los Empleados',     #GRAFICACION EN TORTA DE GRAFICOS EMPLEADOS
    labels={'edad': 'Edad'},           #AQUI LABELS SON LOS TROZOS DE TORTA
    hole=0.3
)


df_resumen_productos = df_cantidad_productos.groupby('product_name').agg({
    'quantity': 'sum'                                                                 #AGRUPA TODOS LOS PRODUCTOS POR NOMBRE Y LUEGO SUMA LA CANTIDAD TOTAL DE CADA UNO
}).reset_index()
df_resumen_productos = df_resumen_productos.sort_values(by='quantity', ascending=False)

fig2 = px.bar(        #BAR ES DIAGRAMA DE BARRA
    df_resumen_productos, 
    x='product_name', 
    y='quantity', 
    title='Cantidad Total de Productos',     #GRAFICO DE BARRAS
    labels={'quantity': 'Cantidad Total'}    #LOS LABELS SON LO QUE VA DENTRO DE LAS BARRAS
)

df_detalles_pedidos['discount'] = df_detalles_pedidos['discount'] * 100   #DISPERSION DONDE SE HACE EL CALCULO DE DESCUENTOS DE PRODUCTOS

fig3_cantidad = px.scatter(
    df_detalles_pedidos,
    x='product_id',
    y='quantity', 
    title='Dispersión de Cantidad por Product ID',   #GRAFICO DISPERSION POR CANTIDAD
    labels={'quantity': 'Cantidad'}  #AQUI YA SABE QUE SON LABELS
)

fig3_descuento = px.scatter(
    df_detalles_pedidos,
    x='product_id',
    y='discount',
    title='Dispersión de Descuento por Product ID',   #GRAFICO DE DISPERSION POR DESCUENTO
    labels={'discount': 'Descuento (%)'}
)

fig4 = px.bar(              #DIAGRAMA DE BARRAS DE FRECUENCIA DE COMPRA POR CLIENTES
    df_pedidos_por_cliente, 
    x='company_name', 
    y='total_orders', 
    title='Frecuencia de Pedidos por Cliente',
    labels={'total_orders': 'Total de Pedidos', 'company_name': 'Cliente'},   #DIAGRAMA DE BARRAS FRECUENCIA PEDIDOS
    text='total_orders'
)

fig1.write_html('empleados_ordenados.html')
fig2.write_html('cantidad_productos.html')
fig3_cantidad.write_html('dispersión_cantidad.html')
fig3_descuento.write_html('dispersión_descuento.html')  #SE EXPORTAN LOS GRAFICOS COMO HTML PARA PREVIAMENTE MOSTRARLOS EN INICIO
fig4.write_html('frecuencia_pedidos.html')
