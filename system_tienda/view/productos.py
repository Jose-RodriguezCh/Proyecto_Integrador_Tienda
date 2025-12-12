import customtkinter as ctk
from tkinter import ttk, BOTH, END
from tkinter import messagebox
import tkinter.font as tkFont
from model import productos_model as pm
# Asegúrate de importar la interfaz principal correctamente según tu estructura de carpetas
from view import interfaz_principal 

class productos:

    @staticmethod
    def borrrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()
        # Asumo que esta función vuelve a pintar la barra de menú superior
        interfaz_principal.crear_menu_bar_Productos(ventana)

    # --------------------------------------------------------------------------
    # 1. CONSULTAR (YA EXISTENTE, LIGERAMENTE MEJORADO)
    # --------------------------------------------------------------------------
    @staticmethod
    def consultar(ventana):
        productos.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(ventana, text="Listado de Productos", font=ctk.CTkFont(size=26, weight="bold"))
        titulo.pack(pady=20)

        cursor = pm.productos.consultar()

        if len(cursor) > 0:
            columnas = ("ID", "Nombre", "Categoria", "Precio Compra", "Precio Venta", "Stock", "Proveedor")
            
            # Frame contenedor para el Treeview y Scrollbar
            tree_frame = ctk.CTkFrame(ventana, fg_color="transparent")
            tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

            productos_tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", height=12)
            
            # Scrollbar vertical
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=productos_tree.yview)
            productos_tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            productos_tree.pack(side="left", fill=BOTH, expand=True)

            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="#F0F0F0", foreground="black", rowheight=28, fieldbackground="#F0F0F0")
            style.configure("Treeview.Heading", background="#D1D5DB", foreground="black", font=("Arial", 12, "bold"))

            for col in columnas:
                productos_tree.heading(col, text=col)
                productos_tree.column(col, width=120, anchor="center")

            for item in cursor:
                # Manejo seguro del proveedor por si devuelve lista vacía o tupla
                prov_data = pm.productos.consultarProveedor(item[6])
                nombre_proveedor = prov_data[0][0] if prov_data and len(prov_data) > 0 else "Desc."
                
                fila = (item[0], item[1], item[2], item[3], item[4], item[5], nombre_proveedor)
                productos_tree.insert("", END, values=fila)
        else:
            ctk.CTkLabel(ventana, text="No hay datos para mostrar", font=ctk.CTkFont(size=16)).pack(pady=20)

    # --------------------------------------------------------------------------
    # 2. AGREGAR (NUEVO)
    # --------------------------------------------------------------------------
    @staticmethod
    def agregar(ventana):
        productos.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(ventana, text="Agregar Nuevo Producto", font=ctk.CTkFont(size=26, weight="bold"))
        titulo.pack(pady=20)

        # Frame para el formulario
        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=10, padx=20)

        # Entradas
        entry_nombre = productos._crear_campo(form_frame, "Nombre:", 0)
        entry_categoria = productos._crear_campo(form_frame, "Categoría:", 1)
        entry_p_compra = productos._crear_campo(form_frame, "Precio Compra:", 2)
        entry_p_venta = productos._crear_campo(form_frame, "Precio Venta:", 3)
        entry_stock = productos._crear_campo(form_frame, "Stock:", 4)
        entry_prov_id = productos._crear_campo(form_frame, "ID Proveedor:", 5)

        def guardar_datos():
            try:
                # Validaciones simples
                nom = entry_nombre.get()
                cat = entry_categoria.get()
                pc = float(entry_p_compra.get())
                pv = float(entry_p_venta.get())
                stk = int(entry_stock.get())
                idp = int(entry_prov_id.get())

                if not nom or not cat:
                    messagebox.showwarning("Advertencia", "Nombre y Categoría son obligatorios.")
                    return

                exito = pm.productos.insertarProductos(nom, cat, pc, pv, stk, idp)
                if exito:
                    messagebox.showinfo("Éxito", "Producto guardado correctamente.")
                    productos.consultar(ventana) # Ir a la lista
                else:
                    messagebox.showerror("Error", "No se pudo guardar en la base de datos.")
            except ValueError:
                messagebox.showerror("Error", "Verifique que los precios y stock sean números válidos.")

        btn_guardar = ctk.CTkButton(ventana, text="Guardar Producto", fg_color="#2CC985", hover_color="#229A65", command=guardar_datos)
        btn_guardar.pack(pady=20)

    # --------------------------------------------------------------------------
    # 3. CAMBIAR / EDITAR (NUEVO)
    # --------------------------------------------------------------------------
    @staticmethod
    def cambiar(ventana):
        productos.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(ventana, text="Modificar Producto", font=ctk.CTkFont(size=26, weight="bold"))
        titulo.pack(pady=10)

        info_lbl = ctk.CTkLabel(ventana, text="Ingrese el ID del producto a modificar y los nuevos valores", text_color="gray")
        info_lbl.pack(pady=(0,10))

        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=10, padx=20)

        # Campos
        entry_id = productos._crear_campo(form_frame, "ID Producto a Modificar:", 0)
        entry_nombre = productos._crear_campo(form_frame, "Nuevo Nombre:", 1)
        entry_categoria = productos._crear_campo(form_frame, "Nueva Categoría:", 2)
        entry_p_compra = productos._crear_campo(form_frame, "Nuevo Precio Compra:", 3)
        entry_p_venta = productos._crear_campo(form_frame, "Nuevo Precio Venta:", 4)
        entry_stock = productos._crear_campo(form_frame, "Nuevo Stock:", 5)
        entry_prov_id = productos._crear_campo(form_frame, "Nuevo ID Proveedor:", 6)

        def actualizar_datos():
            try:
                id_prod = int(entry_id.get())
                nom = entry_nombre.get()
                cat = entry_categoria.get()
                pc = float(entry_p_compra.get())
                pv = float(entry_p_venta.get())
                stk = int(entry_stock.get())
                idp = int(entry_prov_id.get())

                exito = pm.productos.actualizarProductos(nom, cat, pc, pv, stk, idp, id_prod)
                if exito:
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                    productos.consultar(ventana)
                else:
                    messagebox.showerror("Error", "No se pudo actualizar. Verifique que el ID exista.")
            except ValueError:
                messagebox.showerror("Error", "Verifique que los datos numéricos sean correctos.")

        btn_actualizar = ctk.CTkButton(ventana, text="Actualizar Producto", fg_color="#FFA500", hover_color="#CC8400", command=actualizar_datos)
        btn_actualizar.pack(pady=20)

    # --------------------------------------------------------------------------
    # 4. BORRAR (NUEVO)
    # --------------------------------------------------------------------------
    @staticmethod
    def borrar(ventana):
        productos.borrrarPantalla(ventana)

        titulo = ctk.CTkLabel(ventana, text="Eliminar Producto", font=ctk.CTkFont(size=26, weight="bold"))
        titulo.pack(pady=20)

        form_frame = ctk.CTkFrame(ventana)
        form_frame.pack(pady=20)

        entry_id = productos._crear_campo(form_frame, "ID del Producto a Eliminar:", 0)

        def eliminar_datos():
            try:
                id_prod = int(entry_id.get())
                confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto ID {id_prod}?")
                if confirm:
                    exito = pm.productos.eliminar(id_prod)
                    if exito:
                        messagebox.showinfo("Éxito", "Producto eliminado.")
                        productos.consultar(ventana)
                    else:
                        messagebox.showerror("Error", "No se encontró el ID o hubo un error.")
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")

        btn_eliminar = ctk.CTkButton(ventana, text="Eliminar Definitivamente", fg_color="#D32F2F", hover_color="#B71C1C", command=eliminar_datos)
        btn_eliminar.pack(pady=20)

    # --------------------------------------------------------------------------
    # HELPER: Para crear labels y entrys rápido
    # --------------------------------------------------------------------------
    @staticmethod
    def _crear_campo(parent, texto, fila):
        lbl = ctk.CTkLabel(parent, text=texto, font=("Arial", 14))
        lbl.grid(row=fila, column=0, padx=10, pady=5, sticky="e")
        entry = ctk.CTkEntry(parent, width=200)
        entry.grid(row=fila, column=1, padx=10, pady=5)
        return entry