from view.interfaz_principal import InventarioApp
from model import usuarios_model as um
from model import usuarios_model as um

class Login_controller:
    @staticmethod
    def nueva_ventana(ventana_login):
        master_root = ventana_login.master   # Obtener root principal
        ventana_login.destroy()              # Cerrar el login

        # Abrir la ventana del Inventario como Toplevel
        InventarioApp(master=master_root)
    
    @staticmethod
    def verificar(usuario,clave):
        res=um.usuarios.verificar_usuario(usuario,clave)
        return res

class usuarios:
    @staticmethod
    def consultar():
        cursor=um.usuarios.consultar()
        return cursor