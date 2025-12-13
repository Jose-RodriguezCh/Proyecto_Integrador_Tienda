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
    def buscar_id(id_prov):
      try:
        cursor.execute(
          "select * from proveedores where id_proveedor=%s",
          (id_prov,)
        )
        return cursor.fetchone()
      except:    
        return []

    @staticmethod
    def actualizar(nombre,telefono,direccion,id):
        try:
            cursor.execute("UPDATE proveedores SET nombre=%s,telefono=%s,direccion=%s WHERE id_proveedor=%s",(nombre,telefono,direccion,id))
            conexion.commit()
            return True
        except:
            return False
    