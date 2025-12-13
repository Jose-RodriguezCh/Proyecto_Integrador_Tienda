from conexionBD import conexion,cursor

class ventas    :
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM ventas")
            return cursor.fetchall()
        except:
            return []
        
    @staticmethod
    def eliminar(id):
        try:
            res=[]
            cursor.execute("SELECT * FROM ventas WHERE id_ventas=%s",(id,))
            res=cursor.fetchall()
            if len(res)>0:
                cursor.execute("DELETE FROM ventas WHERE id_ventas=%s",(id,))
                conexion.commit()
                return True
            else:
                print(f"No se encontro una venta con el id {id}")
        except:
            return False 

    @staticmethod
    def buscar_por_id(id_venta):
        try:
            cursor.execute("SELECT * FROM ventas WHERE id_ventas = %s",(id_venta,))
            venta = cursor.fetchone()
            return venta 
        except:
            return False

    @staticmethod
    def insertar(lista_prod, cantidad, total, pago, cambio):
        try:
            sql="INSERT INTO ventas (lista_prod, cantidad, total, cantidad_pago, cambio) VALUES (%s, %s, %s, %s, %s)"
            val=(lista_prod, cantidad, total, pago, cambio)
            cursor.execute(sql,val)
            conexion.commit()
            return True
        except:
            return False

       
        