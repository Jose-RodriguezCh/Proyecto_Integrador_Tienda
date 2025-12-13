from conexionBD import conexion,cursor
from tkinter import messagebox

class usuarios:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()
        except:
            return []

    @staticmethod
    def verificar_usuario(nombre, contraseña):
        try:
            cursor.execute(
                "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s",
                (nombre, contraseña)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error BD: {e}")
            messagebox.showerror("Error", "Error de conexión con la base de datos")
            return False