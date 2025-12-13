from view import productos as pro
from view import proveedores as pree
from view import inventario as inv
from view import usuarios as us
from view import ventas as ven
from tkinter import *
import customtkinter as ctk
from model import productos_model 
import os
from PIL import Image as PILImage

def crear_menu_bar_Productos(ventana):
        
        menuBar = Menu(ventana)

        productosMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Productos", menu=productosMenu)

        productosMenu.add_command(label="Agregar", command=lambda: pro.productos.agregar(ventana))
        productosMenu.add_command(label="Consultar", command=lambda: pro.productos.consultar(ventana))
        productosMenu.add_command(label="Cambiar", command=lambda: pro.productos.buscar_id(ventana,"cambiar"))
        productosMenu.add_command(label="Borrar", command=lambda: pro.productos.buscar_id(ventana,"borrar"))
        productosMenu.add_separator()
        productosMenu.add_command(label="Salir", command=ventana.quit)

        ventana.master.config(menu=menuBar)


def crear_menu_bar_Provedores(ventana):
        
        menuBar = Menu(ventana)

        provedoresMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Provedores", menu=provedoresMenu)

        provedoresMenu.add_command(label="Agregar", command=lambda: pree.proveedores.agregar(ventana))
        provedoresMenu.add_command(label="Consultar", command=lambda: pree.proveedores.consultar(ventana))
        provedoresMenu.add_command(label="Cambiar", command=lambda: pree.proveedores.buscar_id(ventana))
        provedoresMenu.add_separator()
        provedoresMenu.add_command(label="Salir", command=ventana.quit)

        ventana.master.config(menu=menuBar)


def crear_menu_bar_ventas(ventana):
        
        menuBar = Menu(ventana)

        ventasMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Ventas", menu=ventasMenu)

        ventasMenu.add_command(label="Agregar", command=lambda: ven.ventas.interfaz_venta(ventana))
        ventasMenu.add_command(label="Consultar", command=lambda: ven.ventas.consultar(ventana))
        ventasMenu.add_command(label="Borrar", command=lambda: ven.ventas.borrar(ventana))
        ventasMenu.add_separator()
        ventasMenu.add_command(label="Salir", command=ventana.quit)

        ventana.master.config(menu=menuBar)


class InventarioApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Menú Principal - Inventario")
        self.geometry("1024x768")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)



        
        # LADO IZQUIERDO
        
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar_frame,
            text="MI TIENDA",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10))

        
        # BOTÓN DE VOLVER (CTkButton)
        
        btn_volver = ctk.CTkButton(
            self.sidebar_frame,
            text="MI TIENDA",
            
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
            self.sidebar_frame, text="Venta", command=self.abrir_ventas
        ).grid(row=3, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.sidebar_frame, text="Inventario", command=self.abrir_inventario
        ).grid(row=4, column=0, padx=20, pady=10)

        

        ctk.CTkButton(
            self.sidebar_frame, text="Salir", command=self.quit
        ).grid(row=5, column=0, padx=20, pady=400)
        
        # CONTENEDOR DERECHO (MAIN FRAME)
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.mostrar_bienvenida()

    # MÉTODO PARA BORRAR PANTALLAS
    
    def cambiar_contenido(self, funcion):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        funcion(self.main_frame)

    # CONTENIDO PRINCIPAL POR DEFECTO
    
    def mostrar_bienvenida(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # CONTENEDOR CENTRAL DEL DASHBOARD
        dashboard = ctk.CTkFrame(self.main_frame, fg_color="#F2F2F2", corner_radius=15)
        dashboard.pack(expand=True, fill="both", padx=40, pady=40)

        #  TÍTULO PRINCIPAL 
        titulo = ctk.CTkLabel(
            dashboard,
            text="DULCES Y BOTANAS GARY",
            text_color="#0A3D62",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        titulo.pack(pady=(40, 5))

        #  SUBTÍTULO 
        subtitulo = ctk.CTkLabel(
            dashboard,
            text="Sistema de Gestión de Inventario",
            text_color="#1B6CA8",
            font=ctk.CTkFont(size=18)
        )
        subtitulo.pack(pady=(0, 30))

        # IMAGEN CENTRAL 
        try:
            
            ruta_base = os.path.dirname(os.path.abspath(__file__))
            ruta_imagen = os.path.join(ruta_base, "dulces.png")

            # Guardamos en self para evitar el recolector de basura
            self.img_dulces = ctk.CTkImage(
                light_image=PILImage.open(ruta_imagen), 
                dark_image=PILImage.open(ruta_imagen), 
                size=(250, 250)
            )

            self.imagen_label = ctk.CTkLabel(dashboard, image=self.img_dulces, text="")
            self.imagen_label.pack(pady=(0, 20))

        except Exception as e:
            print("Error al cargar la imagen:", e)




        #  CONTENEDOR DE BOTONES 
        botones_frame = ctk.CTkFrame(dashboard, fg_color="transparent")
        botones_frame.pack(pady=20)

       #  BOTONES GRANDES (ACCESOS RÁPIDOS) 

        # FILA 1 → 2 BOTONES (Producto / Proveedor)
        btn1 = ctk.CTkButton(
            botones_frame,
            text="📦 Agregar Producto",
            width=220,
            height=50,
            fg_color="#1B6CA8",
            hover_color="#0A3D62",
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.cambiar_contenido(pro.productos.agregar)
        )
        btn1.grid(row=0, column=0, padx=20, pady=15)

        btn2 = ctk.CTkButton(
            botones_frame,
            text="🏷️ Agregar Proveedor",
            width=220,
            height=50,
            fg_color="#A8E6CF",
            hover_color="#7CD9BC",
            text_color="#0A3D62",
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.cambiar_contenido(pree.proveedores.agregar)
        )
        btn2.grid(row=0, column=1, padx=20, pady=15)

        
        btn3 = ctk.CTkButton(
            botones_frame,
            text="🛒 Historial de Ventas",
            width=220,
            height=50,
            fg_color="#1B6CA8",
            hover_color="#0A3D62",
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.cambiar_contenido(ven.ventas.consultar)
        )
        
        btn3.grid(row=1, column=0, columnspan=2, pady=15)

 
    # BOTONES DEL MENÚ
   
    def abrir_productos(self):
        self.cambiar_contenido(pro.productos.consultar)

    def abrir_proveedores(self):
        self.cambiar_contenido(pree.proveedores.consultar)

    def abrir_inventario(self):
        self.cambiar_contenido(inv.inventario.consultar)

    def abrir_ventas(self):
        
        self.cambiar_contenido(ven.ventas.interfaz_venta)