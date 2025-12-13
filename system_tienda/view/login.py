from controller import login_controller as lc
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import math 
from controller.login_controller import Login_controller
from conexionBD import * 

class Login(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

       
        self.title("Acceso al Sistema")
        self.resizable(False, False)
        
      
        window_width = 400
        window_height = 450
        
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        
        
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(ruta_base, "login_icon.png")

        try:
            imagen_pil = Image.open(ruta_imagen)
            self.icon_image = ctk.CTkImage(light_image=imagen_pil, 
                                           dark_image=imagen_pil, 
                                           size=(100, 100))
            
            self.lbl_imagen = ctk.CTkLabel(self, text="", image=self.icon_image)
            self.lbl_imagen.pack(pady=(30, 10))
        except Exception:
            self.lbl_titulo = ctk.CTkLabel(self, text="LOGIN", font=("Arial", 24, "bold"))
            self.lbl_titulo.pack(pady=(40, 10))

        # Campos de Texto
        self.lbl_user = ctk.CTkLabel(self, text="Usuario", font=("Arial", 14))
        self.lbl_user.pack(pady=(5, 0))
        
        self.usuario_entry = ctk.CTkEntry(self, width=220, placeholder_text="Nombre de usuario")
        self.usuario_entry.pack(pady=5)

        self.lbl_pass = ctk.CTkLabel(self, text="Contraseña", font=("Arial", 14))
        self.lbl_pass.pack(pady=(10, 0))

        self.pass_entry = ctk.CTkEntry(self, width=220, show="*", placeholder_text="••••••")
        self.pass_entry.pack(pady=5)

        # Botón
        self.btn_ingresar = ctk.CTkButton(
            self,
            text="INICIAR SESIÓN",
            width=220,
            height=40,
            cursor="hand2",
            command=self.abrir_inventario
        )
        self.btn_ingresar.pack(pady=30)
        
    
        self.lift()
        self.focus_force()

    def on_closing(self):
        
        self.master.destroy()

    

    def abrir_inventario(self):
        usuario = self.usuario_entry.get()
        clave = self.pass_entry.get()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor llene todos los campos")
            return

        if lc.Login_controller.verificar(usuario, clave):
            messagebox.showinfo("Éxito", f"Bienvenido {usuario}")
            
            Login_controller.nueva_ventana(self)
            self.destroy() 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
