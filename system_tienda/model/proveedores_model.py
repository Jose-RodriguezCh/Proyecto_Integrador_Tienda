from conexionBD import conexion,cursor

class proveedores:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM proveedores")
            return cursor.fetchall()
        except:
            return []
        
    @staticmethod
    def insertarProveedor(nombre,telefono,direccion):
        try:
            sql="INSERT INTO proveedores VALUES (null,%s,%s,%s)"
            val=(nombre,telefono,direccion)
            cursor.execute(sql,val)
            conexion.commit()
            return True
        except:
            return False


    @staticmethod
    def actualizar(nombre,telefono,direccion,id):
        try:
            cursor.execute("UPDATE proveedores SET nombre=%s,telefono=%s,direccion=%s WHERE id_proveedor=%s",(nombre,telefono,direccion,id))
            conexion.commit()
            return True
        except:
            return False
    
    @staticmethod
    def eliminar(id):
        try:
            res=[]
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor=%s",(id,))
            res=cursor.fetchall()
            if len(res)>0:
                cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s",(id,))
                conexion.commit()
                return True
            else:
                print(f"No se encontro una nota con el id {id}")
        except:
            return False