import tkinter as tk
from tkinter import ttk, messagebox
import os

ARCHIVO = "productos.txt"

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()

def limpiar_campos():
    codigo.set("")
    detalle.set("")
    talle.set("M")
    color.set("BLANCO")
    precio.set("")
    estado.set("ACTIVO")

def leer_productos():
    crear_archivo()
    productos = []
    with open(ARCHIVO, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 6:
                productos.append(datos)
    return productos

def guardar_productos(productos):
    with open(ARCHIVO, "w") as archivo:
        for p in productos:
            archivo.write("|".join(p) + "\n")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for p in leer_productos():
        tabla.insert("", "end", values=p)

def alta_producto():
    if not (codigo.get() and detalle.get() and talle.get() and color.get() and precio.get()):
        messagebox.showwarning("Atencion", "Debe completar todos los campos del producto.")
        return

    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser estrictamente numerico.")
        return
   
    if not precio.get().isdigit():
        messagebox.showerror("Error", "El Precio debe ser un numero entero (sin comas ni puntos).")
        return

    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    nuevo = [
        codigo.get(),
        detalle.get(),
        talle.get(),
        color.get(),
        precio.get(),
        estado.get()
    ]

    productos.append(nuevo)
    guardar_productos(productos)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Producto dado de alta correctamente.")

def baja_producto():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del producto.")
        return

    productos = leer_productos()
    encontrado = False
    for p in productos:
        if p[0] == codigo.get():
            p[5] = "BAJA"
            encontrado = True

    guardar_productos(productos)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Baja", "Producto dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

def modificar_producto():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del producto.")
        return
   
    if not precio.get().isdigit():
        messagebox.showerror("Error", "El Precio debe ser numerico.")
        return

    productos = leer_productos()
    encontrado = False
    for p in productos:
        if p[0] == codigo.get():
            p[1] = detalle.get()
            p[2] = talle.get()
            p[3] = color.get()
            p[4] = precio.get()
            p[5] = estado.get()
            encontrado = True

    guardar_productos(productos)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Modificacion", "Producto modificado correctamente.")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

def seleccionar_producto(event):
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        codigo.set(valores[0])
        detalle.set(valores[1])
        talle.set(valores[2])
        color.set(valores[3])
        precio.set(valores[4])
        estado.set(valores[5])

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestion de Productos")
ventana.geometry("1000x580")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

# Variables
codigo = tk.StringVar()
detalle = tk.StringVar()
talle = tk.StringVar(value="M")
color = tk.StringVar(value="BLANCO")
precio = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

# Titulo
titulo = tk.Label(ventana, text="GESTION DE PRODUCTOS", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033")
titulo.pack(pady=15)

# Marco formulario
frame_form = tk.Frame(ventana, bg="white", padx=20, pady=10)
frame_form.place(x=30, y=80, width=380, height=450)

tk.Label(frame_form, text="Datos del producto", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Detalle:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=detalle, width=30).grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="Talle:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=talle, values=["XS", "S", "M", "L", "XL", "XXL"], state="readonly", width=27).grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="Color:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=color, values=["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"], state="readonly", width=27).grid(row=4, column=1, pady=5)

tk.Label(frame_form, text="Precio:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=precio, width=30).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

# Botones
tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", command=alta_producto).grid(row=7, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", command=modificar_producto).grid(row=7, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", command=baja_producto).grid(row=8, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", command=limpiar_campos).grid(row=8, column=1, pady=5)

# Tabla
frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=430, y=80, width=540, height=360)

tabla = ttk.Treeview(frame_tabla, columns=("id", "detalle", "talle", "color", "precio", "estado"), show="headings")

tabla.heading("id", text="ID")
tabla.heading("detalle", text="Detalle")
tabla.heading("talle", text="Talle")
tabla.heading("color", text="Color")
tabla.heading("precio", text="Precio")
tabla.heading("estado", text="Estado")

tabla.column("id", width=50)
tabla.column("detalle", width=140)
tabla.column("talle", width=60)
tabla.column("color", width=80)
tabla.column("precio", width=70)
tabla.column("estado", width=70)

tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

# Boton salir
tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=820, y=470)

crear_archivo()
cargar_tabla()

ventana.mainloop()