from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from model import usuarios_model as um

from view import productos as pro
from view import proveedores as pree
from view import inventario as inv

class usuarios:
    def __init__(self,ventana):

        self.consultar(ventana) #Aqui lo cambias a la ventana principal que vea el usuario

    #Borrar Pantalla
    @staticmethod
    def borrrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    #Menu de usuarios
    @staticmethod
    def menuPrincipal(ventana):
        menuBar=Menu(ventana)
        ventana.config(menu=menuBar)
        
        usuariosMenu=Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Usuarios",menu=usuariosMenu)
        usuariosMenu.add_command(label="Agregar",command=lambda: "")
        usuariosMenu.add_command(label="Consultar",command=lambda: usuarios.consultar(ventana))
        usuariosMenu.add_command(label="Cambiar",command=lambda: "")
        usuariosMenu.add_command(label="Borrar",command=lambda: "")
        usuariosMenu.add_separator()
        usuariosMenu.add_command(label="salir",command=ventana.quit)
        pro.productos.menuPrincipal(ventana,menuBar)
        pree.proveedores.menuPrincipal(ventana,menuBar)
        inv.inventario.menuPrincipal(ventana,menuBar)


    @staticmethod
    def consultar(ventana):
        usuarios.borrrarPantalla(ventana)
        usuarios.menuPrincipal(ventana)
        titulo=Label(ventana,text=".::Listado de usuarios::.")
        titulo.pack(pady=10)
        cursor=um.usuarios.consultar()
        if len(cursor)>0:
            columnas=("ID","Usuario")
            style = ttk.Style()
            style.theme_use("default")
            # Header style
            style.configure("Treeview.Heading",
                            background="#d9d9d9",
                            relief="solid",
                            borderwidth=1,
                            padding=(6, 4))
            
            usuario_tree=ttk.Treeview(ventana,columns=columnas,show="headings")
            for i in columnas:
                usuario_tree.heading(i,text=i)
            usuario_tree.pack(fill=BOTH,expand=True,padx=200,pady=(0,100))
            for i in cursor:
                usuario_tree.insert("",END,values=i)
        else:
            messagebox.showinfo(title="Error",message="No existen usuarios guardados en la BD...",icon="info")
                #Aqui iria una ruta a la pagina principal, despues del login del principio
                #Este mensaje se supone que no deberia de ejecutarse, ya que como accedes en primer
                #lugar a la app si no hay usuarios?
        
        btn_volver=Button(ventana,text="Volver",command="")
        btn_volver.pack(pady=5)