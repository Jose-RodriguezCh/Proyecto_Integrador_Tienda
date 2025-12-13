import customtkinter as ctk
from tkinter import ttk, Listbox, END, BOTH, StringVar
from tkinter import messagebox
import tkinter as tk
from view import interfaz_principal
from view import ventas as vent

from controller import controller

class ventas:

    @staticmethod
    def borrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    @staticmethod
    def interfaz_venta(ventana):
        ventas.borrarPantalla(ventana)
        interfaz_principal.crear_menu_bar_ventas(ventana)

        # CARGA DE DATOS PARA EL AUTOCOMPLETADO 
        try:
            lista_productos_bd = controller.productos.consultar()
        except Exception as e:
        
            print(f"Error al cargar productos (usando mock data): {e}")

        #  TÍTULO 
        titulo = ctk.CTkLabel(ventana, text="Punto de Venta", font=ctk.CTkFont(size=26, weight="bold"))
        titulo.pack(pady=(10, 10))

        # CONTENEDOR PRINCIPAL 
        main_frame = ctk.CTkFrame(ventana, fg_color="transparent")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        #  COLUMNA IZQUIERDA: CARRITO 
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill=BOTH, expand=True, padx=(0, 10))

        ctk.CTkLabel(left_frame, text="Carrito de Compras", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        columnas = ("ID", "Producto", "Precio", "Cantidad", "Subtotal")
        tree_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

        carrito_tree = ttk.Treeview(tree_frame, columns=columnas, show="headings", height=10)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=carrito_tree.yview)
        carrito_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        carrito_tree.pack(side="left", fill=BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#F0F0F0", foreground="black", rowheight=25, fieldbackground="#F0F0F0")
        style.configure("Treeview.Heading", background="#D1D5DB", foreground="black", font=("Arial", 11, "bold"))

        for col in columnas:
            carrito_tree.heading(col, text=col)
            ancho = 80 if col in ["ID", "Cantidad"] else 120
            carrito_tree.column(col, width=ancho, anchor="center")

        #  COLUMNA DERECHA: CONTROLES 
        right_frame = ctk.CTkFrame(main_frame, width=300)
        right_frame.pack(side="right", fill="y", padx=(10, 0))

        ctk.CTkLabel(right_frame, text="Buscar Producto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        #  BUSCADOR CON AUTOCOMPLETADO 
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(pady=(5,0), padx=20, fill="x")
        search_frame.columnconfigure(0, weight=1)

        var_busqueda = StringVar()
        
        entry_id_prod = ctk.CTkEntry(search_frame, placeholder_text="Escribe ID o Nombre...", textvariable=var_busqueda)
        entry_id_prod.focus()
        entry_id_prod.pack(fill="x")

        lista_sugerencias = Listbox(search_frame, height=4, font=("Arial", 11), bg="#ffffff", fg="#333333", selectbackground="#175A8E", bd=1, relief="solid")

        def al_escribir(event):
            texto = var_busqueda.get().lower()
            lista_sugerencias.delete(0, END)
            
            if texto == "":
                lista_sugerencias.pack_forget()
                return
            
            coincidencias = []
            for item in lista_productos_bd:
                id_prod = str(item[0])
                nom_prod = str(item[1]).lower()
                
                if texto in id_prod or texto in nom_prod:
                    coincidencias.append(f"{id_prod} - {item[1]}")
            
            if coincidencias:
                for c in coincidencias:
                    lista_sugerencias.insert(END, c)
                lista_sugerencias.pack(pady=(0, 5), fill="x") 
            else:
                lista_sugerencias.pack_forget()

        entry_id_prod.bind("<KeyRelease>", al_escribir)

        def seleccionar_sugerencia(event):
            seleccion = lista_sugerencias.curselection()
            if seleccion:
                texto_item = lista_sugerencias.get(seleccion[0])
                solo_id = texto_item.split(" - ")[0]
                
                entry_id_prod.delete(0, END)
                entry_id_prod.insert(0, solo_id)
                lista_sugerencias.pack_forget()
                entry_cantidad.focus()

        lista_sugerencias.bind("<<ListboxSelect>>", seleccionar_sugerencia)
        # FIN DEL BUSCADOR 


        entry_cantidad = ctk.CTkEntry(right_frame, placeholder_text="Cantidad")
        entry_cantidad.pack(pady=(5, 10), padx=20, fill="x")

        #  LÓGICA DE TOTALES 
        def actualizar_total():
            total = 0.0
            for child in carrito_tree.get_children():
                # El subtotal está en la posición 4 de la tupla de valores
                val = carrito_tree.item(child)["values"][4] 
                # Quitamos el símbolo $ si lo tiene y convertimos a float
                val_clean = float(str(val).replace("$", "").replace(",", "")) 
                total += val_clean
            
            # Actualizamos entry_total
            entry_total.configure(state="normal")
            entry_total.delete(0, END)
            entry_total.insert(0, f"{total:.2f}")
            entry_total.configure(state="readonly")
            
            # Recalculamos cambio
            calcular_cambio(None)

        def agregar_al_carrito():
            pid = entry_id_prod.get()
            cant = entry_cantidad.get()
            
            if not pid or not cant:
                messagebox.showwarning("Datos", "Ingresa ID y Cantidad")
                return
            try:
                cantidad_int = int(cant)
                if cantidad_int <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Cantidad", "La cantidad debe ser un número entero positivo.")
                return
            producto_encontrado = None
            respuesta=False
            for item in lista_productos_bd:
                if str(item[0]) == str(pid):
                    cont=item[5]-int(cant)
                    if cont<0:
                        respuesta=True
                        break
                    else:
                        producto_encontrado = item
                        break
            
            if producto_encontrado:
                nombre = producto_encontrado[1]
                precio = float(producto_encontrado[4]) # Precio Venta

                subtotal = precio * cantidad_int
                contt = 0
                for item in carrito_tree.get_children():
                    valores = carrito_tree.item(item)["values"]

                    if str(valores[0]) == str(pid):  # mismo producto
                        cantidad_en_carrito = int(valores[3])
                        contt += cantidad_en_carrito

                stock_disponible = producto_encontrado[5]

                if contt + cantidad_int <= stock_disponible:
                    fila = (pid, nombre, f"${precio:.2f}", cantidad_int, f"${subtotal:.2f}")
                    carrito_tree.insert("", END, values=fila)
                    actualizar_total()
                    entry_id_prod.delete(0, END)
                    entry_cantidad.delete(0, END)
                    lista_sugerencias.pack_forget()
                else:
                    faltan = (contt + cantidad_int) - stock_disponible
                    messagebox.showwarning(
                        message=f"No hay stock para realizar la compra, faltan {faltan} productos"
                    )

            elif respuesta==True:
                messagebox.showwarning(message=f"No hay stock para realizar la compra, falta {cont*(-1)} Productos")
            else:
                messagebox.showerror("Error", "Producto no encontrado con ese ID")

        def quitar_del_carrito():
            pid_a_borrar = entry_id_prod.get()
            if not pid_a_borrar:
                messagebox.showwarning("Atención", "Selecciona o escribe el ID del producto que quieres quitar.")
                return

            encontrado = False
            items_a_borrar = []
            
            # Buscamos todas las instancias del ID para borrarlas todas
            for item in carrito_tree.get_children():
                valores = carrito_tree.item(item)["values"]
                # Solo borramos la primera instancia encontrada para no vaciar por error
                if str(valores[0]) == pid_a_borrar:
                    items_a_borrar.append(item)
                    encontrado = True
                    break # Borramos solo la primera ocurrencia

            if encontrado:
                carrito_tree.delete(items_a_borrar[0])
                actualizar_total()
                messagebox.showinfo("Éxito", f"Una unidad del Producto ID {pid_a_borrar} ha sido eliminada.")
                entry_id_prod.delete(0, END)
            else:
                messagebox.showerror("Error", "No se encontró ese ID en el carrito.")
                
        #NUEVA FUNCIÓN: CANCELAR VENTA 
        def cancelar_venta():
            if not carrito_tree.get_children():
                messagebox.showinfo("Atención", "El carrito ya está vacío.")
                return

            # Pedir confirmación al usuario
            respuesta = messagebox.askyesno("Confirmar Cancelación", "¿Estás seguro de que quieres cancelar la venta y vaciar completamente el carrito?")
            
            if respuesta:
                # 1. Borrar todos los items del carrito
                carrito_tree.delete(*carrito_tree.get_children())
                
                # 2. Resetear campos de pago y total
                entry_pago.delete(0, END)
                actualizar_total() # Esto llama a calcular_cambio y resetea el total
                
                # Asegurar que el cambio vuelve a 0.00
                entry_cambio.configure(state="normal")
                entry_cambio.delete(0, END)
                entry_cambio.insert(0, "0.00")
                entry_cambio.configure(state="readonly", text_color="#2CC985")
                
                messagebox.showinfo("Cancelado", "Venta cancelada. El carrito se ha vaciado.")


        btn_agregar = ctk.CTkButton(right_frame, text="Agregar (+)", fg_color="#2CC985", hover_color="#229A65", command=agregar_al_carrito)
        btn_agregar.pack(pady=(5, 5), padx=20, fill="x")

        btn_quitar = ctk.CTkButton(right_frame, text="Quitar ID (-)", fg_color="#2FD38C", hover_color="#B71C1C", command=quitar_del_carrito)
        btn_quitar.pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkFrame(right_frame, height=2, fg_color="gray").pack(fill="x", pady=10, padx=10) 

        #  SECCIÓN DE COBRO 
        ctk.CTkLabel(right_frame, text="Resumen de Venta", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        lbl_total = ctk.CTkLabel(right_frame, text="TOTAL A PAGAR:", font=("Arial", 12))
        lbl_total.pack(pady=(5,0))
        entry_total = ctk.CTkEntry(right_frame, font=("Arial", 20, "bold"), justify="center")
        entry_total.pack(pady=5, padx=20)
        entry_total.insert(0, "0.00")
        entry_total.configure(state="readonly")

        lbl_pago = ctk.CTkLabel(right_frame, text="CANTIDAD DE PAGO:", font=("Arial", 12))
        lbl_pago.pack(pady=(5,0))
        entry_pago = ctk.CTkEntry(right_frame, font=("Arial", 16), justify="center")
        entry_pago.pack(pady=5, padx=20)

        lbl_cambio = ctk.CTkLabel(right_frame, text="CAMBIO:", font=("Arial", 12))
        lbl_cambio.pack(pady=(5,0))
        entry_cambio = ctk.CTkEntry(right_frame, font=("Arial", 20, "bold"), justify="center", text_color="#2CC985")
        entry_cambio.pack(pady=5, padx=20)
        entry_cambio.insert(0, "0.00")
        entry_cambio.configure(state="readonly")

        def calcular_cambio(event):
            try:
                total_str = entry_total.get().replace("$", "").replace(",", "")
                total = float(total_str)
                pago_txt = entry_pago.get()
                pago = float(pago_txt) if pago_txt else 0.0
                cambio = pago - total
                
                entry_cambio.configure(state="normal")
                entry_cambio.delete(0, END)
                
                if cambio < 0:
                    entry_cambio.configure(text_color="red")
                    entry_cambio.insert(0, "Falta dinero")
                else:
                    entry_cambio.configure(text_color="#2CC985")
                    entry_cambio.insert(0, f"${cambio:.2f}")
                entry_cambio.configure(state="readonly")
            except ValueError:
                pass

        entry_pago.bind("<KeyRelease>", calcular_cambio)

        def finalizar_venta():
            total = entry_total.get()
            if float(total) == 0:
                messagebox.showwarning("Vacío", "El carrito está vacío.")
                return

            try:
                pago = float(entry_pago.get()) if entry_pago.get() else 0
                cambio_txt = entry_cambio.get().replace("$", "")
                cambio = float(cambio_txt) if cambio_txt not in ["Falta dinero", ""] else 0

                if pago>=float(total):
                    # INSERT - UNA FILA POR PRODUCTO
                    lista_prod=""
                    lista_cantidad=""
                    for item in carrito_tree.get_children():
                        valores = carrito_tree.item(item)["values"]

                        producto = valores[1]
                        cantidad = valores[3]
                        lista_prod+=f"{producto}\n"
                        lista_cantidad+=f"{cantidad}\n"


                    res=controller.ventas.insertar(
                        lista_prod,
                        lista_cantidad,
                        total,
                        pago,
                        cambio
                    )
                    if res:
                        for item in carrito_tree.get_children():
                            valores = carrito_tree.item(item)["values"]
                            id_producto = int(valores[0])
                            cantidad_vendida = int(valores[3])

                            # Buscar producto en la lista de productos
                            for j in lista_productos_bd:
                                if int(j[0]) == id_producto:
                                    nuevo_stock = j[5] - cantidad_vendida  # j[5] = stock actual
                                    controller.productos.actualizarUno(id_producto, nuevo_stock)
                                    break
                        

                    messagebox.showinfo("Venta", f"Venta exitosa por ${total}")
                    # Limpiar todo
                    carrito_tree.delete(*carrito_tree.get_children())
                    entry_pago.delete(0, END)
                else:
                    messagebox.showinfo("Venta", f"Falta ${float(total)-pago} para completar el pago",icon="warning")
                # Llamamos a cancelar venta para reutilizar la lógica de limpieza
            except ValueError:
                messagebox.showerror("Error", "Solo se aceptan numeros")
            

        # BOTÓN CANCELAR VENTA
        btn_cancelar = ctk.CTkButton(right_frame, text="CANCELAR VENTA", fg_color="#FF4136", hover_color="#CC0000", height=40, font=("Arial", 14, "bold"), command=cancelar_venta)
        btn_cancelar.pack(pady=(10, 5), padx=20, fill="x")

        btn_finalizar = ctk.CTkButton(right_frame, text="COBRAR", fg_color="#2CC985", hover_color="#229A65", height=40, font=("Arial", 14, "bold"), command=finalizar_venta)
        btn_finalizar.pack(side="bottom", pady=20, padx=20, fill="x")


    
    # CONSULTAR VENTAS
 

    @staticmethod
    def consultar(ventana):
        vent.ventas.borrarPantalla(ventana)
        interfaz_principal.crear_menu_bar_ventas(ventana)

        # Título
        titulo = ctk.CTkLabel(
            ventana,
            text=" Registro de Ventas",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=20, fill="x")

        # Contenedor Canvas + Scrollbar
        canvas_frame = ctk.CTkFrame(ventana, fg_color="#F1FAFF", corner_radius=15)
        canvas_frame.pack(fill="both", expand=True, padx=30, pady=10)

        canvas = tk.Canvas(canvas_frame, bg="#F1FAFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame interno dentro del canvas
        rows_frame = tk.Frame(canvas, bg="#F1FAFF")
        canvas_window = canvas.create_window((0, 0), window=rows_frame, anchor="nw")

        # Encabezados
        columnas = ["ID Venta", "ID Producto", "Cantidad", "Total ($)", "Pago ($)", "Cambio ($)", "Fecha"]
        for col_idx, col in enumerate(columnas):
            lbl = tk.Label(rows_frame, text=col, font=("Arial", 11, "bold"),
                        bg="#D1D5DB", borderwidth=1, relief="solid")
            lbl.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
            rows_frame.grid_columnconfigure(col_idx, weight=1)  # Todas las columnas igual

        # Tooltip global
        tooltip = tk.Toplevel(ventana)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label_tt = tk.Label(tooltip, text="", bg="#FFFFE0", relief="solid", borderwidth=1)
        label_tt.pack()

        def mostrar_tooltip(event, texto):
            label_tt.config(text=texto)
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()

        def ocultar_tooltip(event):
            tooltip.withdraw()

        # Datos desde el modelo
        ventas_data = controller.ventas.consultar()

        for row_idx, v in enumerate(ventas_data, start=1):  # start=1 porque row 0 es header
            for col_idx, valor in enumerate(v):
                lbl = tk.Label(rows_frame, text=valor, anchor="w", justify="left", wraplength=200,
                            borderwidth=1, relief="solid")
                lbl.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                rows_frame.grid_columnconfigure(col_idx, weight=1)

                # Tooltip
                lbl.bind("<Enter>", lambda e, txt=valor: mostrar_tooltip(e, txt))
                lbl.bind("<Leave>", ocultar_tooltip)

        # Ajuste de scroll y ancho
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas_frame.winfo_width())

        rows_frame.bind("<Configure>", on_frame_configure)
        canvas_frame.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas_frame.winfo_width()))

        if len(ventas_data) == 0:
            messagebox.showinfo("Ventas", "No hay ventas registradas.")











    @staticmethod
    def borrar(ventana):
        vent.ventas.borrarPantalla(ventana)
        interfaz_principal.crear_menu_bar_ventas(ventana)

        titulo = ctk.CTkLabel(
            ventana,
            text=" Eliminar Venta",
            font=ctk.CTkFont(size=26, weight="bold"),
            
        )
        titulo.pack(pady=20)

        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=20)

        lbl = ctk.CTkLabel(
            frame,
            text="Ingresa el ID de la venta a eliminar:",
            font=ctk.CTkFont(size=18)
        )
        lbl.pack(pady=10)

        entrada_id = ctk.CTkEntry(frame, width=200)
        entrada_id.pack(pady=10)

        # Función interna
        def procesar_borrado():
            id_venta = entrada_id.get().strip()

            if not id_venta.isdigit():
                messagebox.showerror("Error", "Debes ingresar un ID válido.")
                return

            try:
                cantidad_int = int(id_venta)
                if cantidad_int <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Cantidad", "La cantidad debe ser un número entero positivo.")
                return
            
            venta = controller.ventas.buscar_id(int(id_venta))

            if venta is None:
                messagebox.showerror("Error", "No existe una venta con ese ID.")
                return
            else:

                # Mostrar datos en alerta
                datos = (
                    f"ID Venta: {venta[0]}\n"
                    f"Productos: {venta[1]}\n"
                    f"Cantidad: {venta[2]}\n"
                    f"Total: ${venta[3]}\n"
                    f"Pago: ${venta[4]}\n"
                    f"Cambio: ${venta[5]}\n"
                    f"Fecha: {venta[6]}"
                )

                respuesta = messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Seguro que deseas eliminar esta venta?\n\n{datos}"
                )

                if respuesta:
                    controller.ventas.eliminar(id_venta)
                    messagebox.showinfo("Éxito", "La venta ha sido eliminada.")
                    ventas.consultar(ventana)  # recargar la interfaz

        btn = ctk.CTkButton(
            frame,
            text="Eliminar venta",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=procesar_borrado,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        btn.pack(pady=15)