from view.interfaz_principal import InventarioApp

class Login_controller:

    @staticmethod
    def nueva_ventana(ventana_login):
        master_root = ventana_login.master   # Obtener root principal
        ventana_login.destroy()              # Cerrar el login

        # Abrir la ventana del Inventario como Toplevel
        InventarioApp(master=master_root)