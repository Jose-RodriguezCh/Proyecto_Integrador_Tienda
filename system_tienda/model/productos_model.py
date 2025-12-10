from conexionBD import conexion,cursor

class productos:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()
        except:
            return []
    
    @staticmethod
    def consultarProveedor(id):
        try:
            cursor.execute("SELECT nombre FROM proveedores where id_proveedor=%s",(id,))
            return cursor.fetchall()
        except:
            return []




    @staticmethod
    def insertarProductos(nombre,categoria,precio_compra,precio_venta,stock,id_proveedor_prod):
        try:
            sql="INSERT INTO productos VALUES (null,%s,%s,%s,%s,%s,%s)"
            val=(nombre,categoria,precio_compra,precio_venta,stock,id_proveedor_prod)
            cursor.execute(sql,val)
            conexion.commit()
            return True
        except:
            return False


    @staticmethod
    def actualizarProductos(nombre,categoria,precio_compra,precio_venta,stock,id_proveedor_prod,id):
        try:
            cursor.execute("UPDATE productos SET nombre=%s,categoria=%s,precio_compra=%s,precio_venta=%s,stock=%s,id_proveedor_prod=%s WHERE id_producto=%s",(nombre,categoria,precio_compra,precio_venta,stock,id_proveedor_prod,id))
            conexion.commit()
            return True
        except:
            return False
    
    @staticmethod
    def eliminar(id):
        try:
            res=[]
            cursor.execute("SELECT * FROM productos WHERE id_producto=%s",(id,))
            res=cursor.fetchall()
            if len(res)>0:
                cursor.execute("DELETE FROM productos WHERE id_producto=%s",(id,))
                conexion.commit()
                return True
            else:
                print(f"No se encontro una nota con el id {id}")
        except:
            return False
        
