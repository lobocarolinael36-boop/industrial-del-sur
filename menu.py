import tkinter as tk
from tkinter import messagebox
import subprocess

def abrir(archivo):
    try:
        # Llama al archivo .py de la entidad sin cerrar el menú
        subprocess.Popen(["python", archivo])
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró {archivo}\nVerificá que el archivo esté en la carpeta.")

def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar el sistema?"):
        root.destroy()

# Configuración de la interfaz
root = tk.Tk()
root.title("Industrial del Sur - Sistema de Gestión")
root.geometry("400x500")
root.configure(bg="#f4f6fa")

# Encabezado
tk.Label(
    root, 
    text="MENÚ PRINCIPAL", 
    font=("Arial", 20, "bold"), 
    bg="#f4f6fa",
    fg="#172033"
).pack(pady=30)

# Botones de Entidades
# Nota: Asegurate de que los archivos existan con estos nombres
tk.Button(root, text="GESTIÓN DE CLIENTES", width=25, height=2, bg="#2563EB", fg="white", font=("Arial", 10, "bold"),
          command=lambda: abrir("cli.py")).pack(pady=10)

tk.Button(root, text="GESTIÓN DE PROVEEDORES", width=25, height=2, bg="#2563EB", fg="white", font=("Arial", 10, "bold"),
          command=lambda: abrir("prov.py")).pack(pady=10)

tk.Button(root, text="GESTIÓN DE PRODUCTOS", width=25, height=2, bg="#2563EB", fg="white", font=("Arial", 10, "bold"),
          command=lambda: abrir("prod.py")).pack(pady=10)

tk.Button(root, text="FACTURACIÓN", width=25, height=2, bg="#2563EB", fg="white", font=("Arial", 10, "bold"),
          command=lambda: abrir("fact.py")).pack(pady=10)

# Botón Salir
tk.Button(root, text="CERRAR SISTEMA", width=25, bg="#DC2626", fg="white", font=("Arial", 10, "bold"), 
          command=salir).pack(pady=40)

root.mainloop()