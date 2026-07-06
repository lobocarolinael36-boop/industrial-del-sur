import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

_HERE    = os.path.dirname(os.path.abspath(__file__))
_DATA    = os.path.normpath(os.path.join(_HERE, "..", "data"))
ARCHIVO  = os.path.join(_DATA, "usuarios.txt")

HEADER   = "#1E3A5F"; ACCENT="#2563EB"; ACCENT_H="#1D4ED8"
SUCCESS  = "#16A34A"; SUCCESS_H="#15803D"; DANGER="#DC2626"; DANGER_H="#B91C1C"
NEUTRAL  = "#6B7280"; NEUTRAL_H="#4B5563"; WHITE="#FFFFFF"
BG       = "#F0F4F8"; TEXT="#111827"; BORDER="#E5E7EB"; ROW_ALT="#EBF5FF"

ROLES   = ["Administrador", "Supervisor", "Operador", "Consulta"]
ESTADOS = ["ACTIVO", "INACTIVO"]

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

def fecha_ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def limpiar_campos():
    for v in (id_usr, nombre, apellido, password): v.set("")
    rol.set("Operador"); estado.set("ACTIVO"); fecha_mod.set("")
    entry_pass.configure(show="*")
    status_var.set("Campos limpiados.")

def leer_usuarios():
    crear_archivo()
    rows = []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        for line in f:
            d = line.strip().split("|")
            if len(d) == 7:
                rows.append(d)
    return rows

def guardar_usuarios(usuarios):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for u in usuarios:
            f.write("|".join(u) + "\n")

def cargar_tabla():
    for r in tabla.get_children(): tabla.delete(r)
    for i, u in enumerate(leer_usuarios()):
        display = [u[0], u[1], u[2], "••••••••", u[4], u[5], u[6]]
        tabla.insert("", "end", values=display, tags=("alt" if i % 2 else "normal",))
    n = len(tabla.get_children())
    status_var.set(f"{n} usuario{'s' if n != 1 else ''} registrado{'s' if n != 1 else ''}.")

def alta_usuario():
    if not all([id_usr.get(), nombre.get(), apellido.get(), password.get()]):
        messagebox.showwarning("Atencion", "Complete todos los campos obligatorios."); return
    if not id_usr.get().isdigit():
        messagebox.showerror("Error", "El ID (DNI) debe ser estrictamente numerico."); return
    if len(id_usr.get()) < 7 or len(id_usr.get()) > 8:
        messagebox.showerror("Error", "El DNI debe tener entre 7 y 8 digitos."); return
    if len(password.get()) < 4:
        messagebox.showerror("Error", "La contrasena debe tener al menos 4 caracteres."); return
    usuarios = leer_usuarios()
    if any(u[0] == id_usr.get() for u in usuarios):
        messagebox.showerror("Error", "Ya existe un usuario con ese DNI."); return
    usuarios.append([id_usr.get(), nombre.get(), apellido.get(),
                     password.get(), rol.get(), estado.get(), fecha_ahora()])
    guardar_usuarios(usuarios); cargar_tabla(); limpiar_campos()
    messagebox.showinfo("Alta", "Usuario dado de alta correctamente.")

def baja_usuario():
    if not id_usr.get():
        messagebox.showwarning("Atencion", "Ingrese el ID del usuario."); return
    if not id_usr.get().isdigit():
        messagebox.showerror("Error", "El ID debe ser numerico."); return
    usuarios = leer_usuarios(); found = False
    for u in usuarios:
        if u[0] == id_usr.get(): u[5] = "INACTIVO"; u[6] = fecha_ahora(); found = True
    guardar_usuarios(usuarios); cargar_tabla()
    if found:
        messagebox.showinfo("Baja", "Usuario dado de baja (INACTIVO).\nFecha de modificacion actualizada.")
    else:
        messagebox.showerror("Error", "Usuario no encontrado.")

def modificar_usuario():
    if not id_usr.get():
        messagebox.showwarning("Atencion", "Ingrese el ID del usuario."); return
    if not id_usr.get().isdigit():
        messagebox.showerror("Error", "El ID debe ser numerico."); return
    if len(id_usr.get()) < 7 or len(id_usr.get()) > 8:
        messagebox.showerror("Error", "El DNI debe tener entre 7 y 8 digitos."); return
    if not nombre.get() or not apellido.get():
        messagebox.showwarning("Atencion", "Nombre y apellido son obligatorios."); return
    usuarios = leer_usuarios(); found = False
    for u in usuarios:
        if u[0] == id_usr.get():
            u[1]=nombre.get(); u[2]=apellido.get()
            if password.get(): u[3]=password.get()
            u[4]=rol.get(); u[5]=estado.get(); u[6]=fecha_ahora(); found=True
    guardar_usuarios(usuarios); cargar_tabla()
    if found:
        messagebox.showinfo("Modificacion", "Usuario modificado.\nFecha de modificacion actualizada.")
    else:
        messagebox.showerror("Error", "Usuario no encontrado.")

def seleccionar(event):
    sel = tabla.focus()
    if not sel: return
    dni_sel = tabla.item(sel, "values")[0]
    for u in leer_usuarios():
        if u[0] == dni_sel:
            id_usr.set(u[0]); nombre.set(u[1]); apellido.set(u[2])
            password.set(u[3]); rol.set(u[4]); estado.set(u[5]); fecha_mod.set(u[6])
            break

def toggle_pass():
    entry_pass.configure(show="" if entry_pass.cget("show") == "*" else "*")

ventana = tk.Tk()
ventana.title("Gestion de Usuarios — Industrial del Sur")
ventana.geometry("1140x640"); ventana.resizable(False, False); ventana.configure(bg=BG)

hdr = tk.Frame(ventana, bg=HEADER, height=66)
hdr.pack(fill="x"); hdr.pack_propagate(False)
tk.Label(hdr, text="INDUSTRIAL DEL SUR", font=("Arial",10,"bold"), bg=HEADER, fg="#93C5FD").place(x=18, y=10)
tk.Label(hdr, text="GESTION DE USUARIOS", font=("Arial",18,"bold"), bg=HEADER, fg=WHITE).place(x=18, y=30)
tk.Frame(ventana, bg=ACCENT, height=3).pack(fill="x")

ftr = tk.Frame(ventana, bg=HEADER, height=26)
ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
status_var = tk.StringVar()
tk.Label(ftr, textvariable=status_var, font=("Arial",9), bg=HEADER, fg="#93C5FD").pack(side="left", padx=12, pady=4)

id_usr=tk.StringVar(); nombre=tk.StringVar(); apellido=tk.StringVar()
password=tk.StringVar(); rol=tk.StringVar(value="Operador")
estado=tk.StringVar(value="ACTIVO"); fecha_mod=tk.StringVar()

fc = tk.Frame(ventana, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
fc.place(x=24, y=74, width=378, height=540)
fch = tk.Frame(fc, bg=ACCENT, height=36); fch.pack(fill="x"); fch.pack_propagate(False)
tk.Label(fch, text="  Datos del Usuario", font=("Arial",11,"bold"), bg=ACCENT, fg=WHITE).pack(side="left", padx=10, pady=8)

ff = tk.Frame(fc, bg=WHITE, padx=18, pady=6); ff.pack(fill="x")
def campo_lbl(row, text):
    tk.Label(ff, text=text, bg=WHITE, fg=TEXT, font=("Arial",10,"bold"), anchor="w").grid(row=row, column=0, sticky="w", pady=(7,2))
def campo_ent(row, var, **kwargs):
    e = tk.Entry(ff, textvariable=var, font=("Arial",10), relief="solid", bd=1, **kwargs)
    e.grid(row=row, column=1, sticky="ew", pady=(7,2), padx=(10,0)); return e
def campo_combo(row, var, values, state="readonly"):
    c = ttk.Combobox(ff, textvariable=var, values=values, state=state, font=("Arial",10))
    c.grid(row=row, column=1, sticky="ew", pady=(7,2), padx=(10,0)); return c

campo_lbl(0, "ID (DNI):"); campo_ent(0, id_usr)
campo_lbl(1, "Nombre:");   campo_ent(1, nombre)
campo_lbl(2, "Apellido:"); campo_ent(2, apellido)

campo_lbl(3, "Contrasena:")
pass_frame = tk.Frame(ff, bg=WHITE)
pass_frame.grid(row=3, column=1, sticky="ew", pady=(7,2), padx=(10,0))
entry_pass = tk.Entry(pass_frame, textvariable=password, font=("Arial",10), relief="solid", bd=1, show="*")
entry_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame, text="Ver", font=("Arial",8), relief="flat",
          bg=NEUTRAL, fg=WHITE, cursor="hand2", command=toggle_pass, padx=6).pack(side="left", padx=(2,0))

campo_lbl(4, "Rol:");    campo_combo(4, rol, ROLES)
campo_lbl(5, "Estado:"); campo_combo(5, estado, ESTADOS)
campo_lbl(6, "Ultima mod.:")
tk.Entry(ff, textvariable=fecha_mod, font=("Arial",10), relief="solid", bd=1,
         state="readonly", fg=NEUTRAL).grid(row=6, column=1, sticky="ew", pady=(7,2), padx=(10,0))
tk.Label(ff, text="Contrasena vacia = no se modifica", bg=WHITE, fg=NEUTRAL,
         font=("Arial",8), anchor="w").grid(row=7, column=0, columnspan=2, sticky="w", pady=(2,0))
ff.columnconfigure(1, weight=1)

tk.Frame(fc, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(4,0))
bf = tk.Frame(fc, bg=WHITE, padx=14, pady=10); bf.pack(fill="x")
r1 = tk.Frame(bf, bg=WHITE); r1.pack(fill="x", pady=(0,6))
flat_btn(r1,"Alta",           alta_usuario,     SUCCESS,  SUCCESS_H).pack(side="left",fill="x",expand=True,padx=(0,4))
flat_btn(r1,"Modificar",      modificar_usuario, ACCENT,  ACCENT_H ).pack(side="left",fill="x",expand=True)
r2 = tk.Frame(bf, bg=WHITE); r2.pack(fill="x", pady=(0,8))
flat_btn(r2,"Baja (Inactivo)",baja_usuario,     DANGER,   DANGER_H ).pack(side="left",fill="x",expand=True,padx=(0,4))
flat_btn(r2,"Limpiar",        limpiar_campos,   NEUTRAL,  NEUTRAL_H).pack(side="left",fill="x",expand=True)
tk.Frame(fc, bg=BORDER, height=1).pack(fill="x", padx=14)
bf2 = tk.Frame(fc, bg=WHITE, padx=14, pady=8); bf2.pack(fill="x")
flat_btn(bf2,"Volver al Menu", ventana.destroy, HEADER, "#2D4E7A").pack(fill="x")

sty = ttk.Style(); sty.theme_use("clam")
sty.configure("I.Treeview", background=WHITE, foreground=TEXT, rowheight=27, fieldbackground=WHITE, font=("Arial",10))
sty.configure("I.Treeview.Heading", background=HEADER, foreground=WHITE, font=("Arial",10,"bold"), relief="flat", padding=5)
sty.map("I.Treeview", background=[("selected","#DBEAFE")], foreground=[("selected",HEADER)])

tc = tk.Frame(ventana, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
tc.place(x=418, y=74, width=698, height=540)
tch = tk.Frame(tc, bg=HEADER, height=36); tch.pack(fill="x"); tch.pack_propagate(False)
tk.Label(tch, text="  Listado de Usuarios", font=("Arial",11,"bold"), bg=HEADER, fg=WHITE).pack(side="left", padx=10, pady=8)

tf = tk.Frame(tc, bg=WHITE); tf.pack(fill="both", expand=True)
vsb = ttk.Scrollbar(tf, orient="vertical"); vsb.pack(side="right", fill="y")
tabla = ttk.Treeview(tf, columns=("id","nombre","apellido","password","rol","estado","fecha"),
                     show="headings", style="I.Treeview", yscrollcommand=vsb.set)
vsb.configure(command=tabla.yview)
for col,txt,w,anch in [
    ("id","DNI",90,"center"),("nombre","Nombre",98,"w"),("apellido","Apellido",98,"w"),
    ("password","Contrasena",90,"center"),("rol","Rol",108,"center"),
    ("estado","Estado",78,"center"),("fecha","Ultima Mod.",148,"center")]:
    tabla.heading(col,text=txt); tabla.column(col,width=w,minwidth=w,anchor=anch)
tabla.tag_configure("alt",background=ROW_ALT); tabla.tag_configure("normal",background=WHITE)
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar)

crear_archivo(); cargar_tabla()
ventana.mainloop()
