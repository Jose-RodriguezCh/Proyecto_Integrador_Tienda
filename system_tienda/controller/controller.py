from model import productos_model as pm
from model import inventario_model as im
from model import proveedores_model as prm
from model import ventas_model as ven

class productos:
    @staticmethod
    def consultar():
        cursor=pm.productos.consultar()
        return cursor  
    
    @staticmethod
    def consultar_proveedor(id):
        cursor=pm.productos.consultarProveedor(id)
        return cursor
    
    @staticmethod
    def agregar(nom,cat,pc,pv,stk,idp):
        res=pm.productos.insertarProductos(nom,cat,pc,pv,stk,idp)
        return res
    
    @staticmethod
    def actualizar(nom,cat,pc,pv,stk,idp,id_prod):
        res=pm.productos.actualizarProductos(nom,cat,pc,pv,stk,idp,id_prod)
        return res
    
    @staticmethod
    def eliminar(id_prod):
        res=pm.productos.eliminar(id_prod)
        return res
    
    @staticmethod
    def actualizarUno(id_producto,cantidad):
        res=pm.productos.actualizarUno(id_producto,cantidad)
        return res
    
    @staticmethod
    def buscar_id(id_prod):
        res=pm.productos.buscar_id(id_prod)
        return res

class proveedores:
    @staticmethod
    def consultar():
        cursor=prm.proveedores.consultar()
        return cursor
    
    @staticmethod
    def agregar(nom,tel,dir_):
        res=prm.proveedores.insertarProveedor(nom,tel,dir_)
        return res

    @staticmethod
    def actualizar(nom,tel,dir_,id_prov):
        res=prm.proveedores.actualizar(nom,tel,dir_,id_prov)
        return res
    
    @staticmethod
    def buscar_id(id_prod):
        res=prm.proveedores.buscar_id(id_prod)
        return res
    


class ventas:
    @staticmethod
    def buscar_id(id_venta):
        venta=ven.ventas.buscar_por_id(int(id_venta))
        return venta
    
    @staticmethod
    def consultar():
        res=ven.ventas.consultar()
        return res
    
    @staticmethod
    def eliminar(id_venta):
        res=ven.ventas.eliminar(int(id_venta))
        return res
    
    @staticmethod
    def insertar(lista_prod, cantidad, total, pago, cambio):
        res=ven.ventas.insertar(lista_prod, cantidad, total, pago, cambio)
        return res
        

class inventario:
    @staticmethod
    def consultar():
        contar=im.inventario.consultar()
        return contar
    
    @staticmethod
    def consultar_agotado():
        agotado=im.inventario.consultarProd_ago()
        return agotado