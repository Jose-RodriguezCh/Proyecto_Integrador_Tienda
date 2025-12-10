from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from model import inventario_model as im

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

    @staticmethod
    def consultar(ventana):
        inventario.borrrarPantalla(ventana)
        usu.usuarios.menuPrincipal(ventana)
        titulo=Label(ventana,text=".::Listado de inventario::.")
        titulo.pack(pady=10)
        cursor=im.inventario.consultar()
        if len(cursor)>0:
            columnas=("ID","Lista","Fecha de actualizacion","ID del producto")
            style = ttk.Style()
            style.theme_use("default")
            # Header style
            style.configure("Treeview.Heading",
                            background="#d9d9d9",
                            relief="solid",
                            borderwidth=1,
                            padding=(6, 4))
            
            inventario_tree=ttk.Treeview(ventana,columns=columnas,show="headings")
            for i in columnas:
                inventario_tree.heading(i,text=i)
            for col in inventario_tree["columns"]:
                inventario_tree.column(col, stretch=True)

            font = tkFont.Font()
            for col in columnas:
                max_width = font.measure(col)
                for row in inventario_tree.get_children():
                    cell = inventario_tree.set(row, col)
                    cell_width = font.measure(cell)
                    if cell_width > max_width:
                        max_width = cell_width
                inventario_tree.column(col, width=max_width + 20, stretch=True)

            inventario_tree.pack(fill=BOTH,expand=True,padx=200,pady=(0,100))
            for i in cursor:
                inventario_tree.insert("",END,values=i)
        else:
            messagebox.showinfo(title="Error",message="No existe nada de inventario guardado en la BD...",icon="info")
                #Aqui iria una ruta a la pagina principal, despues del login del principio
                #Este mensaje se supone que no deberia de ejecutarse, ya que como accedes en primer
                #lugar a la app si no hay usuarios?
        
        btn_volver=Button(ventana,text="Volver",command="")
        btn_volver.pack(pady=5)