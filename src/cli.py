import tkinter as tk
from tkinter import ttk, messagebox
import os

_HERE    = os.path.dirname(os.path.abspath(__file__))
_DATA    = os.path.normpath(os.path.join(_HERE, "..", "data"))
ARCHIVO  = os.path.join(_DATA, "clientes.txt")

HEADER   = "#1E3A5F"; ACCENT="#2563EB"; ACCENT_H="#1D4ED8"
SUCCESS  = "#16A34A"; SUCCESS_H="#15803D"; DANGER="#DC2626"; DANGER_H="#B91C1C"
NEUTRAL  = "#6B7280"; NEUTRAL_H="#4B5563"; WHITE="#FFFFFF"
BG       = "#F0F4F8"; TEXT="#111827"; BORDER="#E5E7EB"; ROW_ALT="#EBF5FF"

def flat_btn(parent, text, command, bg, hover):
    btn = tk.Button(parent, text=text, command=command,
                    bg=bg, fg=WHITE, relief="flat", bd=0,
                    font=("Arial", 10, "bold"), cursor="hand2",
                    activebackground=hover, activeforeground=WHITE, pady=10)
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn

def crear_archivo():
    os.makedirs(_DATA, exist_ok=True)
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w").close()

def limpiar_campos():
    for v in (codigo, nombre, apellido, dni, direccion): v.set("")
    estado.set("ACTIVO")
    status_var.set("Campos limpiados.")

def leer_clientes():
    crear_archivo()
    rows = []
    with open(ARCHIVO, "r") as f:
        for line in f:
            d = line.strip().split("|")
            if len(d) == 6:
                rows.append(d)
    return rows

def guardar_clientes(clientes):
    with open(ARCHIVO, "w") as f:
        for c in clientes:
            f.write("|".join(c) + "\n")

def cargar_tabla():
    for r in tabla.get_children(): tabla.delete(r)
    for i, c in enumerate(leer_clientes()):
        tabla.insert("", "end", values=c, tags=("alt" if i % 2 else "normal",))
    n = len(tabla.get_children())
    status_var.set(f"{n} cliente{'s' if n != 1 else ''} registrado{'s' if n != 1 else ''}.")

def alta_cliente():
    if not all([codigo.get(), nombre.get(), apellido.get(), dni.get(), direccion.get()]):
        messagebox.showwarning("Atencion", "Complete todos los campos."); return
    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser estrictamente numerico."); return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser estrictamente numerico."); return
    clientes = leer_clientes()
    if any(c[0] == codigo.get() for c in clientes):
        messagebox.showerror("Error", "El Identificador ya existe."); return
    clientes.append([codigo.get(), nombre.get(), apellido.get(), dni.get(), direccion.get(), estado.get()])
    guardar_clientes(clientes); cargar_tabla(); limpiar_campos()
    messagebox.showinfo("Alta", "Cliente dado de alta correctamente.")

def baja_cliente():
    if not codigo.get():
        messagebox.showwarning("Atencion", "Ingrese el Identificador."); return
    clientes = leer_clientes(); found = False
    for c in clientes:
        if c[0] == codigo.get(): c[5] = "BAJA"; found = True
    guardar_clientes(clientes); cargar_tabla()
    (messagebox.showinfo if found else messagebox.showerror)(
        "Baja" if found else "Error",
        "Cliente dado de baja." if found else "Cliente no encontrado.")

def modificar_cliente():
    if not codigo.get():
        messagebox.showwarning("Atencion", "Ingrese el Identificador."); return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser estrictamente numerico."); return
    if not direccion.get():
        messagebox.showerror("Error", "La direccion es obligatoria."); return
    clientes = leer_clientes(); found = False
    for c in clientes:
        if c[0] == codigo.get():
            c[1]=nombre.get(); c[2]=apellido.get(); c[3]=dni.get()
            c[4]=direccion.get(); c[5]=estado.get(); found=True
    guardar_clientes(clientes); cargar_tabla()
    (messagebox.showinfo if found else messagebox.showerror)(
        "Modificacion" if found else "Error",
        "Cliente modificado." if found else "Cliente no encontrado.")

def seleccionar(event):
    sel = tabla.focus()
    if sel:
        v = tabla.item(sel, "values")
        codigo.set(v[0]); nombre.set(v[1]); apellido.set(v[2])
        dni.set(v[3]); direccion.set(v[4]); estado.set(v[5])

ventana = tk.Tk()
ventana.title("Gestion de Clientes — Industrial del Sur")
ventana.geometry("1020x618"); ventana.resizable(False, False); ventana.configure(bg=BG)

hdr = tk.Frame(ventana, bg=HEADER, height=66)
hdr.pack(fill="x"); hdr.pack_propagate(False)
tk.Label(hdr, text="INDUSTRIAL DEL SUR", font=("Arial",10,"bold"), bg=HEADER, fg="#93C5FD").place(x=18, y=10)
tk.Label(hdr, text="GESTION DE CLIENTES", font=("Arial",18,"bold"), bg=HEADER, fg=WHITE).place(x=18, y=30)
tk.Frame(ventana, bg=ACCENT, height=3).pack(fill="x")

ftr = tk.Frame(ventana, bg=HEADER, height=26)
ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
status_var = tk.StringVar()
tk.Label(ftr, textvariable=status_var, font=("Arial",9), bg=HEADER, fg="#93C5FD").pack(side="left", padx=12, pady=4)

codigo=tk.StringVar(); nombre=tk.StringVar(); apellido=tk.StringVar()
dni=tk.StringVar(); direccion=tk.StringVar(); estado=tk.StringVar(value="ACTIVO")

fc = tk.Frame(ventana, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
fc.place(x=24, y=74, width=378, height=518)
fch = tk.Frame(fc, bg=ACCENT, height=36); fch.pack(fill="x"); fch.pack_propagate(False)
tk.Label(fch, text="  Datos del Cliente", font=("Arial",11,"bold"), bg=ACCENT, fg=WHITE).pack(side="left", padx=10, pady=8)

ff = tk.Frame(fc, bg=WHITE, padx=18, pady=8); ff.pack(fill="x")
def campo(row, label, var, widget=None):
    tk.Label(ff, text=label, bg=WHITE, fg=TEXT, font=("Arial",10,"bold"), anchor="w").grid(row=row, column=0, sticky="w", pady=(8,2))
    w = widget or tk.Entry(ff, textvariable=var, font=("Arial",10), relief="solid", bd=1)
    w.grid(row=row, column=1, sticky="ew", pady=(8,2), padx=(10,0))

campo(0, "Identificador:", codigo); campo(1, "Nombre:", nombre)
campo(2, "Apellido:", apellido);    campo(3, "DNI:", dni)
campo(4, "Direccion:", direccion)
campo(5, "Estado:", estado, ttk.Combobox(ff, textvariable=estado, values=["ACTIVO","BAJA"], state="readonly", font=("Arial",10)))
ff.columnconfigure(1, weight=1)

tk.Frame(fc, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(4,0))
bf = tk.Frame(fc, bg=WHITE, padx=14, pady=12); bf.pack(fill="x")
r1 = tk.Frame(bf, bg=WHITE); r1.pack(fill="x", pady=(0,6))
flat_btn(r1,"Alta",     alta_cliente,     SUCCESS, SUCCESS_H).pack(side="left", fill="x", expand=True, padx=(0,4))
flat_btn(r1,"Modificar",modificar_cliente, ACCENT,  ACCENT_H ).pack(side="left", fill="x", expand=True)
r2 = tk.Frame(bf, bg=WHITE); r2.pack(fill="x", pady=(0,10))
flat_btn(r2,"Baja",    baja_cliente,   DANGER,  DANGER_H ).pack(side="left", fill="x", expand=True, padx=(0,4))
flat_btn(r2,"Limpiar", limpiar_campos, NEUTRAL, NEUTRAL_H).pack(side="left", fill="x", expand=True)
tk.Frame(fc, bg=BORDER, height=1).pack(fill="x", padx=14)
bf2 = tk.Frame(fc, bg=WHITE, padx=14, pady=10); bf2.pack(fill="x")
flat_btn(bf2,"Volver al Menu", ventana.destroy, HEADER, "#2D4E7A").pack(fill="x")

sty = ttk.Style(); sty.theme_use("clam")
sty.configure("I.Treeview", background=WHITE, foreground=TEXT, rowheight=27, fieldbackground=WHITE, font=("Arial",10))
sty.configure("I.Treeview.Heading", background=HEADER, foreground=WHITE, font=("Arial",10,"bold"), relief="flat", padding=5)
sty.map("I.Treeview", background=[("selected","#DBEAFE")], foreground=[("selected",HEADER)])

tc = tk.Frame(ventana, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
tc.place(x=418, y=74, width=578, height=518)
tch = tk.Frame(tc, bg=HEADER, height=36); tch.pack(fill="x"); tch.pack_propagate(False)
tk.Label(tch, text="  Listado de Clientes", font=("Arial",11,"bold"), bg=HEADER, fg=WHITE).pack(side="left", padx=10, pady=8)

tf = tk.Frame(tc, bg=WHITE); tf.pack(fill="both", expand=True)
vsb = ttk.Scrollbar(tf, orient="vertical"); vsb.pack(side="right", fill="y")
tabla = ttk.Treeview(tf, columns=("id","nombre","apellido","dni","direccion","estado"),
                     show="headings", style="I.Treeview", yscrollcommand=vsb.set)
vsb.configure(command=tabla.yview)
for col,txt,w,anch in [("id","ID",52,"center"),("nombre","Nombre",100,"w"),("apellido","Apellido",100,"w"),
    ("dni","DNI",84,"center"),("direccion","Direccion",142,"w"),("estado","Estado",82,"center")]:
    tabla.heading(col,text=txt); tabla.column(col,width=w,minwidth=w,anchor=anch)
tabla.tag_configure("alt",background=ROW_ALT); tabla.tag_configure("normal",background=WHITE)
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar)

crear_archivo(); cargar_tabla()
ventana.mainloop()
