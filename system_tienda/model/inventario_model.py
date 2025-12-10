from conexionBD import conexion,cursor

class inventario:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM inventario")
            return cursor.fetchall()
        except:
            return []