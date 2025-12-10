import customtkinter as ctk
from tkinter import ttk, BOTH, END
from tkinter import messagebox
import tkinter.font as tkFont
from model import proveedores_model as prm
from view import interfaz_principal

class proveedores:

    @staticmethod
    def borrrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()
        # Se asume que esta función existe en tu interfaz principal
        interfaz_principal.crear_menu_bar_Provedores(ventana)

    # --------------------------------------------------------------------------
    # 1. CONSULTAR
    # --------------------------------------------------------------------------
    @staticmethod
    def consultar(ventana):
        proveedores.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text="·::  Listado de Proveedores  ::·",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=20)

        cursor = prm.proveedores.consultar()

        if len(cursor) > 0:
            columnas = ("ID", "Nombre", "Telefono", "Direccion")

            # Frame contenedor para Treeview y Scrollbar
            tree_frame = ctk.CTkFrame(ventana, fg_color="transparent")
            tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

            proveedores_tree = ttk.Treeview(
                tree_frame,
                columns=columnas,
                show="headings",
                height=12
            )

            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=proveedores_tree.yview)
            proveedores_tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            proveedores_tree.pack(side="left", fill=BOTH, expand=True)

            # Estilos
            style = ttk.Style()
            style.theme_use("default")
            style.configure(
                "Treeview",
                background="#F0F0F0",
                foreground="black",
                rowheight=28,
                fieldbackground="#F0F0F0"
            )
            style.configure(
                "Treeview.Heading",
                background="#D1D5DB",
                foreground="black",
                font=("Arial", 12, "bold")
            )

            for col in columnas:
                proveedores_tree.heading(col, text=col)
                proveedores_tree.column(col, width=150, anchor="center")

            # Insertar datos
            for row in cursor:
                proveedores_tree.insert("", END, values=row)

        else:
            ctk.CTkLabel(ventana, text="No hay proveedores registrados.", font=ctk.CTkFont(size=16)).pack(pady=20)

    # --------------------------------------------------------------------------
    # 2. AGREGAR
    # --------------------------------------------------------------------------
    @staticmethod
    def agregar(ventana):
        proveedores.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text="·::  Agregar Nuevo Proveedor  ::·",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=20)

        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=10, padx=20)

        # Campos según tu modelo (Nombre, Telefono, Direccion)
        entry_nombre = proveedores._crear_campo(form_frame, "Nombre:", 0)
        entry_telefono = proveedores._crear_campo(form_frame, "Teléfono:", 1)
        entry_direccion = proveedores._crear_campo(form_frame, "Dirección:", 2)

        def guardar_datos():
            nom = entry_nombre.get()
            tel = entry_telefono.get()
            dir_ = entry_direccion.get()

            if not nom:
                messagebox.showwarning("Advertencia", "El campo Nombre es obligatorio.")
                return

            exito = prm.proveedores.insertarProveedor(nom, tel, dir_)
            
            if exito:
                messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
                proveedores.consultar(ventana)
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos.")

        btn_guardar = ctk.CTkButton(
            ventana, 
            text="Guardar Proveedor", 
            fg_color="#2CC985", 
            hover_color="#229A65", 
            command=guardar_datos
        )
        btn_guardar.pack(pady=20)

    # --------------------------------------------------------------------------
    # 3. CAMBIAR / EDITAR
    # --------------------------------------------------------------------------
    @staticmethod
    def cambiar(ventana):
        proveedores.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text="·::  Modificar Proveedor  ::·",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=10)
        
        lbl_info = ctk.CTkLabel(ventana, text="Ingrese el ID del proveedor a modificar y los nuevos datos", text_color="gray")
        lbl_info.pack(pady=(0,10))

        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=10, padx=20)

        # Campos necesarios: ID (para el WHERE) y los datos nuevos
        entry_id = proveedores._crear_campo(form_frame, "ID Proveedor a Modificar:", 0)
        entry_nombre = proveedores._crear_campo(form_frame, "Nuevo Nombre:", 1)
        entry_telefono = proveedores._crear_campo(form_frame, "Nuevo Teléfono:", 2)
        entry_direccion = proveedores._crear_campo(form_frame, "Nueva Dirección:", 3)

        def actualizar_datos():
            try:
                id_prov = int(entry_id.get())
                nom = entry_nombre.get()
                tel = entry_telefono.get()
                dir_ = entry_direccion.get()

                # Llamada al modelo: actualizar(nombre, telefono, direccion, id)
                exito = prm.proveedores.actualizar(nom, tel, dir_, id_prov)

                if exito:
                    messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
                    proveedores.consultar(ventana)
                else:
                    messagebox.showerror("Error", "No se pudo actualizar. Verifique que el ID exista.")
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")

        btn_actualizar = ctk.CTkButton(
            ventana, 
            text="Actualizar Proveedor", 
            fg_color="#FFA500", 
            hover_color="#CC8400", 
            command=actualizar_datos
        )
        btn_actualizar.pack(pady=20)

    # --------------------------------------------------------------------------
    # 4. BORRAR
    # --------------------------------------------------------------------------
    @staticmethod
    def borrar(ventana):
        proveedores.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text="·::  Eliminar Proveedor  ::·",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=20)

        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=20)

        entry_id = proveedores._crear_campo(form_frame, "ID del Proveedor a Eliminar:", 0)

        def eliminar_datos():
            try:
                id_prov = int(entry_id.get())
                confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al proveedor con ID {id_prov}?")
                
                if confirm:
                    exito = prm.proveedores.eliminar(id_prov)
                    if exito:
                        messagebox.showinfo("Éxito", "Proveedor eliminado.")
                        proveedores.consultar(ventana)
                    else:
                        messagebox.showerror("Error", "No se encontró el ID o hubo un error.")
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")

        btn_eliminar = ctk.CTkButton(
            ventana, 
            text="Eliminar Definitivamente", 
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            command=eliminar_datos
        )
        btn_eliminar.pack(pady=20)

    # --------------------------------------------------------------------------
    # HELPER
    # --------------------------------------------------------------------------
    @staticmethod
    def _crear_campo(parent, texto, fila):
        lbl = ctk.CTkLabel(parent, text=texto, font=("Arial", 14))
        lbl.grid(row=fila, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(parent, width=200)
        entry.grid(row=fila, column=1, padx=10, pady=5)
        return entry