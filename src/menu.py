import tkinter as tk
from tkinter import messagebox
import subprocess
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

BG       = "#F0F4F8"; HEADER="#1E3A5F"; ACCENT="#2563EB"; ACCENT_H="#1D4ED8"
SUCCESS  = "#16A34A"; SUCCESS_H="#15803D"; DANGER="#DC2626"; DANGER_H="#B91C1C"
NEUTRAL  = "#6B7280"; BORDER="#E5E7EB"; WHITE="#FFFFFF"

def abrir(archivo):
    try:
        subprocess.Popen(["python", os.path.join(_HERE, archivo)])
    except Exception as e:
        messagebox.showerror("Error", f"No se encontro {archivo}.\nVerifica que este en la carpeta src/.")

def salir():
    if messagebox.askyesno("Salir", "Desea cerrar el sistema?"):
        root.destroy()

def nav_btn(parent, text, cmd, color=ACCENT, hover=ACCENT_H):
    f = tk.Frame(parent, bg=color)
    f.pack(fill="x", pady=5)
    btn = tk.Button(f, text=text, command=cmd,
                    bg=color, fg=WHITE, relief="flat", bd=0,
                    font=("Arial", 11, "bold"), cursor="hand2",
                    padx=18, pady=14, anchor="w",
                    activebackground=hover, activeforeground=WHITE)
    btn.pack(fill="x")
    for w in (btn, f):
        w.bind("<Enter>", lambda e: btn.configure(bg=hover))
        w.bind("<Leave>", lambda e: btn.configure(bg=color))

root = tk.Tk()
root.title("Industrial del Sur — Menu Principal")
root.geometry("400x620")
root.resizable(False, False)
root.configure(bg=BG)

hdr = tk.Frame(root, bg=HEADER, height=100)
hdr.pack(fill="x"); hdr.pack_propagate(False)
tk.Label(hdr, text="SISTEMA DE GESTION COMERCIAL",
         font=("Arial", 9, "bold"), bg=HEADER, fg="#93C5FD").pack(pady=(24, 0))
tk.Label(hdr, text="INDUSTRIAL DEL SUR",
         font=("Arial", 20, "bold"), bg=HEADER, fg=WHITE).pack(pady=(4, 0))
tk.Frame(root, bg=ACCENT, height=3).pack(fill="x")

content = tk.Frame(root, bg=BG, padx=24, pady=18)
content.pack(fill="both", expand=True)
tk.Label(content, text="MODULOS DEL SISTEMA",
         font=("Arial", 9, "bold"), bg=BG, fg=NEUTRAL).pack(anchor="w", pady=(0, 12))

nav_btn(content, "  Gestion de Clientes",    lambda: abrir("cli.py"))
nav_btn(content, "  Gestion de Proveedores", lambda: abrir("prov.py"))
nav_btn(content, "  Gestion de Productos",   lambda: abrir("prod.py"))
nav_btn(content, "  Facturacion",            lambda: abrir("fact.py"),     SUCCESS,  SUCCESS_H)
nav_btn(content, "  Gestion de Usuarios",    lambda: abrir("usuarios.py"), "#7C3AED","#6D28D9")

tk.Frame(content, bg=BORDER, height=1).pack(fill="x", pady=16)
nav_btn(content, "  Cerrar Sistema", salir, DANGER, DANGER_H)

ftr = tk.Frame(root, bg=HEADER, height=28)
ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
tk.Label(ftr, text="v1.0  |  Desarrollo de Sistemas  |  2026  |  Carolina Lobo",
         font=("Arial", 8), bg=HEADER, fg="#93C5FD").pack(expand=True)

root.mainloop()
