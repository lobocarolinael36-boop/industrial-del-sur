import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_PRODUCTOS = "productos.txt"
CARPETA_FACTURAS = "facturas_emitidas"

# Estructuras de datos en memoria para el manejo local de la factura
clientes_dict = {}
productos_dict = {}
items_factura = []  # Guarda listas de: [ID_Prod, Detalle, Cantidad, Precio_Unit, Costo_Total]

def inicializar_entorno():
    if not os.path.exists(CARPETA_FACTURAS):
        os.makedirs(CARPETA_FACTURAS)

def cargar_datos_combobox():
    # Cargar Clientes
    clientes_dict.clear()
    combo_cliente['values'] = ()
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r") as f:
            lista_clientes = []
            for linea in f:
                datos = linea.strip().split("|")
                if len(datos) == 6 and datos[5] == "ACTIVO":
                    # Formato para el combo: "DNI - Apellido, Nombre"
                    label = f"{datos[3]} - {datos[2]}, {datos[1]}"
                    clientes_dict[label] = datos # Guardamos toda la info del cliente
                    lista_clientes.append(label)
            combo_cliente['values'] = lista_clientes

    # Cargar Productos
    productos_dict.clear()
    combo_producto['values'] = ()
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as f:
            lista_productos = []
            for linea in f:
                datos = linea.strip().split("|")
                if len(datos) == 6 and datos[5] == "ACTIVO":
                    # Formato para el combo: "Detalle (Talle: X, Color: Y)"
                    label = f"{datos[1]} (Talle: {datos[2]}, Col: {datos[3]})"
                    # Guardamos [ID, Detalle, Precio]
                    productos_dict[label] = {
                        "id": datos[0],
                        "detalle": datos[1],
                        "precio": int(datos[4]) if datos[4].isdigit() else 0
                    }
                    lista_productos.append(label)
            combo_producto['values'] = lista_productos

def actualizar_precio_unitario(event):
    prod_seleccionado = combo_producto.get()
    if prod_seleccionado in productos_dict:
        precio_unitario.set(str(productos_dict[prod_seleccionado]["precio"]))
    else:
        precio_unitario.set("")

def agregar_item():
    prod_sel = combo_producto.get()
    cant_sel = cantidad.get()

    if not prod_sel or not cant_sel:
        messagebox.showwarning("Atención", "Debe seleccionar un producto e ingresar la cantidad.")
        return

    if not cant_sel.isdigit() or int(cant_sel) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0.")
        return

    info_prod = productos_dict[prod_sel]
    id_prod = info_prod["id"]
    detalle_prod = info_prod["detalle"]
    prec_unit = info_prod["precio"]
    cant = int(cant_sel)
    costo_total_item = prec_unit * cant

    # Validar si el producto ya fue agregado para sumar cantidad o listarlo de nuevo
    items_factura.append([id_prod, detalle_prod, cant, prec_unit, costo_total_item])
    
    actualizar_vista_factura()
    
    # Limpiar campos de carga de producto
    combo_producto.set("")
    cantidad.set("")
    precio_unitario.set("")

def actualizar_vista_factura():
    # Limpiar Treeview de la derecha
    for fila in tabla_factura.get_children():
        tabla_factura.delete(fila)
    
    total = 0
    for item in items_factura:
        # Inserta: ID, Detalle, Cant, Precio U., Subtotal
        tabla_factura.insert("", "end", values=(item[0], item[1], item[2], f"${item[3]}", f"${item[4]}"))
        total += item[4]
    
    # Actualizar la etiqueta del costo total general
    total_factura.set(f"TOTAL: ${total}")

def limpiar_pantalla():
    combo_cliente.set("")
    combo_producto.set("")
    cantidad.set("")
    precio_unitario.set("")
    items_factura.clear()
    actualizar_vista_factura()

def finalizar_factura():
    cliente_sel = combo_cliente.get()
    if not cliente_sel:
        messagebox.showwarning("Atención", "Debe seleccionar un cliente para confeccionar la factura.")
        return
    
    if not items_factura:
        messagebox.showwarning("Atención", "La factura debe contener al menos un producto.")
        return

    datos_cliente = clientes_dict[cliente_sel]
    dni_cliente = datos_cliente[3]
    nombre_cliente = f"{datos_cliente[2]}, {datos_cliente[1]}"
    direccion_cliente = datos_cliente[4]

    # Calcular total final
    total_final = sum(item[4] for item in items_factura)
    
    # Formatear el archivo de salida
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.join(CARPETA_FACTURAS, f"Factura_{dni_cliente}_{timestamp_archivo}.txt")

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("               FACTURA DE COMPRA                  \n")
            f.write("==================================================\n")
            f.write(f"Fecha: {fecha_actual}\n")
            f.write("--------------------------------------------------\n")
            f.write(f"CLIENTE: {nombre_cliente}\n")
            f.write(f"DNI: {dni_cliente}\n")
            f.write(f"Dirección: {direccion_cliente}\n")
            f.write("==================================================\n")
            f.write(f"{'ID':<5} {'Detalle':<20} {'Cant':<5} {'P.Unit':<8} {'Total':<8}\n")
            f.write("--------------------------------------------------\n")
            for item in items_factura:
                f.write(f"{item[0]:<5} {item[1]:<20} {item[2]:<5} ${item[3]:<7} ${item[4]:<7}\n")
            f.write("==================================================\n")
            f.write(f"TOTAL A PAGAR: ${total_final}\n")
            f.write("==================================================\n")
            f.write("          Gracias por su preferencia.             \n")
        
        messagebox.showinfo("Facturación", f"Factura generada con éxito:\n{os.path.basename(nombre_archivo)}")
        limpiar_pantalla()
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo de la factura: {e}")

# Interfaz gráfica (Mantiene geometría y paleta de los ABM tradicionales)
ventana = tk.Tk()
ventana.title("Generación de Facturas")
ventana.geometry("1000x580")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")


cantidad = tk.StringVar()
precio_unitario = tk.StringVar()
total_factura = tk.StringVar(value="TOTAL: $0")


titulo = tk.Label(ventana, text="GENERACIÓN DE FACTURAS", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033")
titulo.pack(pady=15)


frame_form = tk.Frame(ventana, bg="white", padx=20, pady=10)
frame_form.place(x=30, y=80, width=380, height=450)

tk.Label(frame_form, text="Datos de la Venta", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

# Selector de Clientes
tk.Label(frame_form, text="Seleccionar Cliente:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
combo_cliente = ttk.Combobox(frame_form, state="readonly", width=27)
combo_cliente.grid(row=1, column=1, pady=5)


ttk.Separator(frame_form, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", pady=15)


tk.Label(frame_form, text="Producto:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
combo_producto = ttk.Combobox(frame_form, state="readonly", width=27)
combo_producto.grid(row=3, column=1, pady=5)
combo_producto.bind("<<ComboboxSelected>>", actualizar_precio_unitario)

# Mostrar Precio
tk.Label(frame_form, text="Precio Unitario:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=precio_unitario, width=30, state="readonly").grid(row=4, column=1, pady=5)

# Cantidad 
tk.Label(frame_form, text="Cantidad:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=cantidad, width=30).grid(row=5, column=1, pady=5)

# Botones
tk.Button(frame_form, text="Agregar Item", width=12, bg="#16A34A", fg="white", command=agregar_item).grid(row=6, column=1, pady=20, sticky="e")
tk.Button(frame_form, text="Limpiar Todo", width=12, bg="#6B7280", fg="white", command=limpiar_pantalla).grid(row=7, column=0, pady=5)
tk.Button(frame_form, text="Emitir Factura", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=finalizar_factura).grid(row=7, column=1, pady=5)

frame_factura_vista = tk.Frame(ventana, bg="white")
frame_factura_vista.place(x=430, y=80, width=540, height=360)

tabla_factura = ttk.Treeview(frame_factura_vista, columns=("id", "detalle", "cant", "precio_u", "subtotal"), show="headings")

tabla_factura.heading("id", text="ID")
tabla_factura.heading("detalle", text="Detalle Producto")
tabla_factura.heading("cant", text="Cant.")
tabla_factura.heading("precio_u", text="P. Unit")
tabla_factura.heading("subtotal", text="Subtotal")

tabla_factura.column("id", width=40, anchor="center")
tabla_factura.column("detalle", width=190)
tabla_factura.column("cant", width=50, anchor="center")
tabla_factura.column("precio_u", width=80, anchor="e")
tabla_factura.column("subtotal", width=90, anchor="e")

tabla_factura.pack(fill="both", expand=True)

# Sección inferior derecha: Mostrador de costo total consolidado
lbl_total = tk.Label(ventana, textvariable=total_factura, font=("Arial", 16, "bold"), bg="#f4f6fa", fg="#DC2626")
lbl_total.place(x=430, y=455)

# Botón salir corporativo
tk.Button(ventana, text="Volver al Menú", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=820, y=470)

# Inicializar componentes e hilos de datos
inicializar_entorno()
cargar_datos_combobox()

ventana.mainloop()