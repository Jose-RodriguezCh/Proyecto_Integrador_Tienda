from conexionBD import conexion,cursor

class inventario:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT SUM(precio_compra*stock) as pc,SUM(precio_venta*stock) as pv,SUM(stock) as st FROM productos")
            return cursor.fetchall()
        except:
            return []
    
    @staticmethod
    def consultarProd_ago():
        try:
            cursor.execute("SELECT nombre,stock FROM productos where stock<10")
            return cursor.fetchall()
        except:
            return []