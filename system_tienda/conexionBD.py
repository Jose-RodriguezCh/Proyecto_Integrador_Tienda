import mysql.connector

try:
    conexion=mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_integradora_tienda"
    )
    cursor=conexion.cursor(buffered=True)
except:
    print("En este momento no es posible comunicarse con el sistema, intentelo mas tarde...")
