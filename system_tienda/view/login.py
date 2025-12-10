from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
#from PIL import Image,ImageTk
import customtkinter as ctk
from controller.login_controller import Login_controller
from conexionBD import *

'''
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(ruta_base,"login_icon.png")

        imagen_pil = Image.open(ruta_imagen)

        ancho=100
        alto=100

        imagen_pil.thumbnail((ancho, alto), Image.Resampling.LANCZOS)

        imagen = ImageTk.PhotoImage(imagen_pil)

        etiqueta = Label(ventana, image=imagen, compound="top")
        etiqueta.pack()

            
        label_login=ttk.Label(ventana,text="Inicio de sesión",justify="center")
        label_login.config(
            font=("Arial",15,"bold")
        )
        label_login.pack(pady=10)
        '''
class Login(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Login")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="Usuario").pack(pady=10)
        self.usuario_entry = ctk.CTkEntry(self)
        self.usuario_entry.pack()

        ctk.CTkLabel(self, text="Contraseña").pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self, show="•")
        self.pass_entry.pack()

        ctk.CTkButton(
            self,
            text="Ingresar",
            command=self.abrir_inventario
        ).pack(pady=20)

    @staticmethod
    def verificar_usuario(nombre,contraseña):
        try:
            cursor.execute(
              "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s",
              (nombre,contraseña)
            )

            resultado=cursor.fetchone()
            conexion.commit()

            if resultado:
                return True
            else:
                return False
        except:
            messagebox.showerror("Error", "Error de conexión con la base de datos")
            return False

    def abrir_inventario(self):
        usuario = self.usuario_entry.get()
        clave = self.pass_entry.get()

        # 2. Validar que no estén vacíos
        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor llene todos los campos")
            return

        # 3. Llamar al método estático para verificar en BD
        if Login.verificar_usuario(usuario, clave):
            messagebox.showinfo("Éxito", f"Bienvenido {usuario}")
            # 4. Si es correcto, abrir la siguiente ventana
            Login_controller.nueva_ventana(self)
            self.destroy() # Opcional: Cierra la ventana de login
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

