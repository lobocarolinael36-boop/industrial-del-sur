import tkinter as tk
from tkinter import ttk, messagebox
import os

# -*- coding: utf-8 -*-

ARCHIVO = "clientes.txt"

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()

def limpiar_campos():
    codigo.set("")
    nombre.set("")
    apellido.set("")
    dni.set("")
    direccion.set("")
    estado.set("ACTIVO")

def leer_clientes():
    crear_archivo()
    clientes = []
    with open(ARCHIVO, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 6:
                clientes.append(datos)
    return clientes

def guardar_clientes(clientes):
    with open(ARCHIVO, "w") as archivo:
        for cliente in clientes:
            archivo.write("|".join(cliente) + "\n")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for cliente in leer_clientes():
        tabla.insert("", "end", values=cliente)

def alta_cliente():
    if not (codigo.get() and nombre.get() and apellido.get() and dni.get() and direccion.get()):
        messagebox.showwarning("Atencion", "Debe completar todos los campos, incluida la direccion.")
        return

    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser estrictamente numerico.")
        return
   
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser estrictamente numerico.")
        return

    clientes = leer_clientes()
    for cliente in clientes:
        if cliente[0] == codigo.get():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    nuevo = [
        codigo.get(),
        nombre.get(),
        apellido.get(),
        dni.get(),
        direccion.get(),
        estado.get()
    ]

    clientes.append(nuevo)
    guardar_clientes(clientes)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Cliente dado de alta correctamente.")

def baja_cliente():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del cliente.")
        return

    clientes = leer_clientes()
    encontrado = False
    for cliente in clientes:
        if cliente[0] == codigo.get():
            cliente[5] = "BAJA"
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Baja", "Cliente dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")

def modificar_cliente():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del cliente.")
        return
   
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser numerico.")
        return
   
    if not direccion.get():
        messagebox.showerror("Error", "La direccion es obligatoria.")
        return

    clientes = leer_clientes()
    encontrado = False
    for cliente in clientes:
        if cliente[0] == codigo.get():
            cliente[1] = nombre.get()
            cliente[2] = apellido.get()
            cliente[3] = dni.get()
            cliente[4] = direccion.get()
            cliente[5] = estado.get()
            encontrado = True

    guardar_clientes(clientes)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Modificacion", "Cliente modificado correctamente.")
    else:
        messagebox.showerror("Error", "Cliente no encontrado.")

def seleccionar_cliente(event):
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        codigo.set(valores[0])
        nombre.set(valores[1])
        apellido.set(valores[2])
        dni.set(valores[3])
        direccion.set(valores[4])
        estado.set(valores[5])

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestion de Clientes")
ventana.geometry("1000x580")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

# Variables
codigo = tk.StringVar()
nombre = tk.StringVar()
apellido = tk.StringVar()
dni = tk.StringVar()
direccion = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

# Titulo
titulo = tk.Label(ventana, text="GESTION DE CLIENTES", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033")
titulo.pack(pady=15)

# Marco formulario
frame_form = tk.Frame(ventana, bg="white", padx=20, pady=10)
frame_form.place(x=30, y=80, width=380, height=450)

tk.Label(frame_form, text="Datos del cliente", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Nombre:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=nombre, width=30).grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="Apellido:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=apellido, width=30).grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="DNI:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=dni, width=30).grid(row=4, column=1, pady=5)

tk.Label(frame_form, text="Direccion:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=direccion, width=30).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

# Botones
tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", command=alta_cliente).grid(row=7, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", command=modificar_cliente).grid(row=7, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", command=baja_cliente).grid(row=8, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", command=limpiar_campos).grid(row=8, column=1, pady=5)

# Tabla
frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=430, y=80, width=540, height=360)

tabla = ttk.Treeview(frame_tabla, columns=("id", "nombre", "apellido", "dni", "direccion", "estado"), show="headings")

tabla.heading("id", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("apellido", text="Apellido")
tabla.heading("dni", text="DNI")
tabla.heading("direccion", text="Direccion")
tabla.heading("estado", text="Estado")

tabla.column("id", width=50)
tabla.column("nombre", width=90)
tabla.column("apellido", width=90)
tabla.column("dni", width=80)
tabla.column("direccion", width=130)
tabla.column("estado", width=70)

tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_cliente)

# Boton salir
tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=820, y=470)

crear_archivo()
cargar_tabla()

ventana.mainloop()