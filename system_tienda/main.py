import customtkinter as ctk
from view.login import Login


class App:
    def __init__(self, root):
        self.root = root
        #Crear la ventana de login como Toplevel
        self.login_window = Login(master=self.root)

if __name__=="__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()   # ÚNICO ROOT

    root.withdraw()    # Root oculto (solo sirve de base para Toplevels)

    app = App(root)
    root.mainloop()