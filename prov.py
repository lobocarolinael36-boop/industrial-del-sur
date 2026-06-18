import tkinter as tk
from tkinter import ttk, messagebox
import os

# -*- coding: utf-8 -*-

ARCHIVO = "proveedores.txt"

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()

def limpiar_campos():
    codigo.set("")
    empresa.set("")
    cuit.set("")
    rubro.set("")
    contacto.set("")
    estado.set("ACTIVO")

def leer_proveedores():
    crear_archivo()
    proveedores = []
    with open(ARCHIVO, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 6:
                proveedores.append(datos)
    return proveedores

def guardar_proveedores(proveedores):
    with open(ARCHIVO, "w") as archivo:
        for p in proveedores:
            archivo.write("|".join(p) + "\n")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for p in leer_proveedores():
        tabla.insert("", "end", values=p)

def alta_proveedor():
    if not (codigo.get() and empresa.get() and cuit.get() and rubro.get() and contacto.get()):
        messagebox.showwarning("Atencion", "Debe completar todos los campos del proveedor.")
        return

    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser estrictamente numerico.")
        return
   
    if not cuit.get().isdigit():
        messagebox.showerror("Error", "El CUIT debe ser estrictamente numerico (sin guiones).")
        return

    proveedores = leer_proveedores()
    for p in proveedores:
        if p[0] == codigo.get():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    nuevo = [
        codigo.get(),
        empresa.get(),
        cuit.get(),
        rubro.get(),
        contacto.get(),
        estado.get()
    ]

    proveedores.append(nuevo)
    guardar_proveedores(proveedores)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Proveedor dado de alta correctamente.")

def baja_proveedor():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del proveedor.")
        return

    proveedores = leer_proveedores()
    encontrado = False
    for p in proveedores:
        if p[0] == codigo.get():
            p[5] = "BAJA"
            encontrado = True

    guardar_proveedores(proveedores)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Baja", "Proveedor dado de baja correctamente.")
    else:
        messagebox.showerror("Error", "Proveedor no encontrado.")

def modificar_proveedor():
    if codigo.get() == "":
        messagebox.showwarning("Atencion", "Ingrese el Identificador del proveedor.")
        return
   
    if not cuit.get().isdigit():
        messagebox.showerror("Error", "El CUIT debe ser numerico.")
        return

    proveedores = leer_proveedores()
    encontrado = False
    for p in proveedores:
        if p[0] == codigo.get():
            p[1] = empresa.get()
            p[2] = cuit.get()
            p[3] = rubro.get()
            p[4] = contacto.get()
            p[5] = estado.get()
            encontrado = True

    guardar_proveedores(proveedores)
    cargar_tabla()
    if encontrado:
        messagebox.showinfo("Modificacion", "Proveedor modificado correctamente.")
    else:
        messagebox.showerror("Error", "Proveedor no encontrado.")

def seleccionar_proveedor(event):
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        codigo.set(valores[0])
        empresa.set(valores[1])
        cuit.set(valores[2])
        rubro.set(valores[3])
        contacto.set(valores[4])
        estado.set(valores[5])

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestion de Proveedores")
ventana.geometry("1000x580")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

# Variables
codigo = tk.StringVar()
empresa = tk.StringVar()
cuit = tk.StringVar()
rubro = tk.StringVar()
contacto = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

# Titulo
titulo = tk.Label(ventana, text="GESTION DE PROVEEDORES", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033")
titulo.pack(pady=15)

# Marco formulario
frame_form = tk.Frame(ventana, bg="white", padx=20, pady=10)
frame_form.place(x=30, y=80, width=380, height=450)

tk.Label(frame_form, text="Datos del proveedor", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Razón Social:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=empresa, width=30).grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="CUIT:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=cuit, width=30).grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="Rubro:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=rubro, values=["Telas", "Hilanderia", "Avios", "Tintoreria"], width=27).grid(row=4, column=1, pady=5)

tk.Label(frame_form, text="Contacto:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=contacto, width=30).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

# Botones
tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", command=alta_proveedor).grid(row=7, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", command=modificar_proveedor).grid(row=7, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", command=baja_proveedor).grid(row=8, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", command=limpiar_campos).grid(row=8, column=1, pady=5)

# Tabla
frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=430, y=80, width=540, height=360)

tabla = ttk.Treeview(frame_tabla, columns=("id", "empresa", "cuit", "rubro", "contacto", "estado"), show="headings")

tabla.heading("id", text="ID")
tabla.heading("empresa", text="Razón Social")
tabla.heading("cuit", text="CUIT")
tabla.heading("rubro", text="Rubro")
tabla.heading("contacto", text="Contacto")
tabla.heading("estado", text="Estado")

tabla.column("id", width=50)
tabla.column("empresa", width=110)
tabla.column("cuit", width=90)
tabla.column("rubro", width=80)
tabla.column("contacto", width=110)
tabla.column("estado", width=70)

tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_proveedor)

# Boton salir
tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=820, y=470)

crear_archivo()
cargar_tabla()

ventana.mainloop()