from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from model import productos_model as pm
from model import inventario_model as im
import customtkinter as ctk
from view import usuarios as usu

class inventario:
    def __init__(self,ventana):
        self.consultar(ventana) #Aqui lo cambias a la ventana principal que vea el usuario

    #Borrar Pantalla
    @staticmethod
    def borrrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    #Menu de usuarios
    @staticmethod
    def menuPrincipal(ventana,menuBar):
        inventarioMenu=Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Inventario",menu=inventarioMenu)
        inventarioMenu.add_command(label="Agregar",command=lambda: "")
        inventarioMenu.add_command(label="Consultar",command=lambda: inventario.consultar(ventana))
        inventarioMenu.add_command(label="Cambiar",command=lambda: "")
        inventarioMenu.add_command(label="Borrar",command=lambda: "")
        inventarioMenu.add_separator()
        inventarioMenu.add_command(label="salir",command=ventana.quit)

    # --------------------------------------------------------------------------
    # 1. CONSULTAR
    # --------------------------------------------------------------------------
    @staticmethod
    def consultar(ventana):
        inventario.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text="Reporte de inventario",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=20)

        cursor = pm.productos.consultar()

        if len(cursor) > 0:
            contar=im.inventario.consultar()

            # --- NUEVO CONTENEDOR PARA LOS TOTALES (Alineado a la izquierda) ---
            frame_totales = ctk.CTkFrame(ventana, fg_color="transparent")
            # Asegura que el frame ocupe todo el ancho de la ventana y esté a la izquierda
            frame_totales.pack(fill="x", padx=40, pady=20, anchor="w")
            
            # --- LABEL DE INVERSIÓN TOTAL ---
            pc = ctk.CTkLabel(
                frame_totales, # <- Ahora el master es frame_totales
                text=f"Inversión Total \n\n${contar[0][0]}\n", # Añadido formato .2f
                font=ctk.CTkFont(size=20, weight="bold", slant="roman"),
                anchor="w",    # Alinea el texto a la izquierda DENTRO del label
                justify="left"
            )
            # Empaqueta el label para que ocupe todo el ancho del frame
            pc.pack(fill="x", expand=True, pady=10)
            
            # --- LABEL DE GANANCIAS ---
            pv = ctk.CTkLabel(
                frame_totales, # <- Ahora el master es frame_totales
                text=f"Venta total estimada \n\n${contar[0][1]}\n", # Añadido formato .2f
                font=ctk.CTkFont(size=20, weight="bold", slant="roman"),
                anchor="w",    # Alinea el texto a la izquierda DENTRO del label
                justify="left"
            )
            # Empaqueta el label para que ocupe todo el ancho del frame
            pv.pack(fill="x", expand=True, pady=10)
            # --- LABEL DE Stock ---
            tp = ctk.CTkLabel(
                frame_totales, # <- Ahora el master es frame_totales
                text=f"Total de productos \n\n{round(contar[0][2])}\n", # Añadido formato .2f
                font=ctk.CTkFont(size=20, weight="bold", slant="roman"),
                anchor="w",    # Alinea el texto a la izquierda DENTRO del label
                justify="left"
            )
            # Empaqueta el label para que ocupe todo el ancho del frame
            tp.pack(fill="x", expand=True, pady=10)

            # --- LABEL DE PRODUCTOS CON STOCK MENOR A 10 ---
            agotados=im.inventario.consultarProd_ago()
            res=""
            for i in agotados:
                res+=f"Nombre: {i[0]} - Cantidad: {i[1]}\n"
            ag = ctk.CTkLabel(
                frame_totales, # <- Ahora el master es frame_totales
                text=f"Productos cerca de agotarse \n\n{res}\n", # Añadido formato .2f
                font=ctk.CTkFont(size=20, weight="bold", slant="roman"),
                anchor="w",    # Alinea el texto a la izquierda DENTRO del label
                justify="left"
            )
            # Empaqueta el label para que ocupe todo el ancho del frame
            ag.pack(fill="x", expand=True, pady=10)
            # ------------------------------------------------------------------

        else:
            ctk.CTkLabel(ventana, text="No hay productos registrados.", font=ctk.CTkFont(size=16)).pack(pady=20)

            # columnas = ("ID", "Nombre", "Telefono", "Direccion")

            # # Frame contenedor para Treeview y Scrollbar
            # tree_frame = ctk.CTkFrame(ventana, fg_color="transparent")
            # tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

            # proveedores_tree = ttk.Treeview(
            #     tree_frame,
            #     columns=columnas,
            #     show="headings",
            #     height=12
            # )

            # # Scrollbar
            # scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=proveedores_tree.yview)
            # proveedores_tree.configure(yscroll=scrollbar.set)
            # scrollbar.pack(side="right", fill="y")
            # proveedores_tree.pack(side="left", fill=BOTH, expand=True)

            # # Estilos
            # style = ttk.Style()
            # style.theme_use("default")
            # style.configure(
            #     "Treeview",
            #     background="#F0F0F0",
            #     foreground="black",
            #     rowheight=28,
            #     fieldbackground="#F0F0F0"
            # )
            # style.configure(
            #     "Treeview.Heading",
            #     background="#D1D5DB",
            #     foreground="black",
            #     font=("Arial", 12, "bold")
            # )

            # for col in columnas:
            #     proveedores_tree.heading(col, text=col)
            #     proveedores_tree.column(col, width=150, anchor="center")

            # # Insertar datos
            # for row in cursor:
            #     proveedores_tree.insert("", END, values=row)
