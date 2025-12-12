from view import productos as pro
from view import proveedores as pree
from view import inventario as inv
from view import usuarios as us
from tkinter import *
import customtkinter as ctk
from model import productos_model 

  
def crear_menu_bar_Productos(ventana):
        
        menuBar = Menu(ventana)

        productosMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Productos", menu=productosMenu)

        productosMenu.add_command(label="Agregar", command=lambda: pro.productos.agregar(ventana))
        productosMenu.add_command(label="Consultar", command=lambda: pro.productos.consultar(ventana))
        productosMenu.add_command(label="Cambiar", command=lambda: pro.productos.cambiar(ventana))
        productosMenu.add_command(label="Borrar", command=lambda: pro.productos.borrar(ventana))
        productosMenu.add_separator()
        productosMenu.add_command(label="Salir", command=ventana.quit)

        ventana.master.config(menu=menuBar)


def crear_menu_bar_Provedores(ventana):
        
        menuBar = Menu(ventana)

        provedoresMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Provedores", menu=provedoresMenu)

        provedoresMenu.add_command(label="Agregar", command=lambda: pree.proveedores.agregar(ventana))
        provedoresMenu.add_command(label="Consultar", command=lambda: pree.proveedores.consultar(ventana))
        provedoresMenu.add_command(label="Cambiar", command=lambda: pree.proveedores.cambiar(ventana))
        provedoresMenu.add_command(label="Borrar", command=lambda: pree.proveedores.borrar(ventana))
        provedoresMenu.add_separator()
        provedoresMenu.add_command(label="Salir", command=ventana.quit)

        ventana.master.config(menu=menuBar)



class InventarioApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Menú Principal - Inventario")
        self.geometry("1024x768")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)



        # ---------------------------------------------------------------------
        # LADO IZQUIERDO
        # ---------------------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar_frame,
            text="MI TIENDA",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10))

        # -------------------------
        # BOTÓN DE VOLVER (CTkButton)
        # -------------------------
        btn_volver = ctk.CTkButton(
            self.sidebar_frame,
            text="MI TIENDA",
            fg_color="transparent",
            hover_color="#175A8E",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.mostrar_bienvenida()
        )
        btn_volver.grid(row=0, column=0, padx=20, pady=(20, 10))


        # BOTONES DEL MENÚ LATERAL
        ctk.CTkButton(
            self.sidebar_frame, text="Productos", command=self.abrir_productos
        ).grid(row=1, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar_frame, text="Proveedores", command=self.abrir_proveedores
        ).grid(row=2, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar_frame, text="Inventario", command=self.abrir_inventario
        ).grid(row=3, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar_frame, text="Salir", command=self.quit
        ).grid(row=4, column=0, padx=20, pady=400)
        # ---------------------------------------------------------------------
        # CONTENEDOR DERECHO (MAIN FRAME)
        # ---------------------------------------------------------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.mostrar_bienvenida()


    
        



    # ---------------------------------------------------------------------
    # MÉTODO PARA CAMBIAR PANTALLAS
    # ---------------------------------------------------------------------
    def cambiar_contenido(self, funcion):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        funcion(self.main_frame)

    # ---------------------------------------------------------------------
    # CONTENIDO PRINCIPAL POR DEFECTO
    # ---------------------------------------------------------------------
    def mostrar_bienvenida(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.main_frame,
            text="Bienvenido a Dulces y Botanas Gary",
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self.main_frame,
            text="Selecciona una opción del menú lateral para comenzar.",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

    # ---------------------------------------------------------------------
    # BOTONES DEL MENÚ
    # ---------------------------------------------------------------------
    def abrir_productos(self):
        from view.productos import productos
        self.cambiar_contenido(productos.consultar)

    def abrir_proveedores(self):
        from view.proveedores import proveedores
        self.cambiar_contenido(proveedores.consultar)

    def abrir_inventario(self):
        from view.inventario import inventario
        self.cambiar_contenido(inventario.consultar)