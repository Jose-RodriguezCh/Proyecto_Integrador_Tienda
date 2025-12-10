from conexionBD import conexion,cursor

class usuarios:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()
        except:
            return []
