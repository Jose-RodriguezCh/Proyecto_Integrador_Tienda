from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from view import productos as pro
from view import proveedores as pree
from view import inventario as inv

from controller import login_controller as lc

class usuarios:
    def __init__(self,ventana):

        self.consultar(ventana) 

    #Borrar Pantalla
    @staticmethod
    def borrrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

   


    @staticmethod
    def consultar(ventana):
        usuarios.borrrarPantalla(ventana)
        usuarios.menuPrincipal(ventana)
        titulo=Label(ventana,text=".::Listado de usuarios::.")
        titulo.pack(pady=10)
        cursor=lc.usuarios.consultar()
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
                
        
        btn_volver=Button(ventana,text="Volver",command="")
        btn_volver.pack(pady=5)