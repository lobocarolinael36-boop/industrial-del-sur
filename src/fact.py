import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

_HERE             = os.path.dirname(os.path.abspath(__file__))
_DATA             = os.path.normpath(os.path.join(_HERE, "..", "data"))
ARCHIVO_CLIENTES  = os.path.join(_DATA, "clientes.txt")
ARCHIVO_PRODUCTOS = os.path.join(_DATA, "productos.txt")
CARPETA_FACTURAS  = os.path.join(_DATA, "facturas_emitidas")

HEADER   = "#1E3A5F"; ACCENT="#2563EB"; ACCENT_H="#1D4ED8"
SUCCESS  = "#16A34A"; SUCCESS_H="#15803D"; DANGER="#DC2626"; DANGER_H="#B91C1C"
NEUTRAL  = "#6B7280"; NEUTRAL_H="#4B5563"; WHITE="#FFFFFF"
BG       = "#F0F4F8"; TEXT="#111827"; BORDER="#E5E7EB"; ROW_ALT="#EBF5FF"

clientes_dict  = {}
productos_dict = {}
items_factura  = []

def flat_btn(parent, text, command, bg, hover):
    btn = tk.Button(parent, text=text, command=command,
                    bg=bg, fg=WHITE, relief="flat", bd=0,
                    font=("Arial", 10, "bold"), cursor="hand2",
                    activebackground=hover, activeforeground=WHITE, pady=10)
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn

def inicializar_entorno():
    os.makedirs(CARPETA_FACTURAS, exist_ok=True)

def cargar_datos_combobox():
    clientes_dict.clear(); combo_cliente['values'] = ()
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r") as f:
            lista = []
            for line in f:
                d = line.strip().split("|")
                if len(d) == 6 and d[5] == "ACTIVO":
                    label = f"{d[3]} — {d[2]}, {d[1]}"
                    clientes_dict[label] = d; lista.append(label)
            combo_cliente['values'] = lista

    productos_dict.clear(); combo_producto['values'] = ()
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as f:
            lista = []
            for line in f:
                d = line.strip().split("|")
                if len(d) == 6 and d[5] == "ACTIVO":
                    label = f"{d[1]}  (Talle: {d[2]}, Color: {d[3]})"
                    productos_dict[label] = {"id": d[0], "detalle": d[1],
                                              "precio": int(d[4]) if d[4].isdigit() else 0}
                    lista.append(label)
            combo_producto['values'] = lista

def actualizar_precio(event):
    prod = combo_producto.get()
    precio_unitario.set(str(productos_dict[prod]["precio"]) if prod in productos_dict else "")

def agregar_item():
    prod_sel = combo_producto.get(); cant_sel = cantidad.get()
    if not prod_sel or not cant_sel:
        messagebox.showwarning("Atencion", "Seleccione un producto e ingrese la cantidad."); return
    if not cant_sel.isdigit() or int(cant_sel) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un numero entero mayor a 0."); return
    info = productos_dict[prod_sel]
    cant = int(cant_sel); subtotal = info["precio"] * cant
    items_factura.append([info["id"], info["detalle"], cant, info["precio"], subtotal])
    actualizar_vista()
    combo_producto.set(""); cantidad.set(""); precio_unitario.set("")

def actualizar_vista():
    for r in tabla_factura.get_children(): tabla_factura.delete(r)
    total = 0
    for i, item in enumerate(items_factura):
        tabla_factura.insert("", "end",
            values=(item[0], item[1], item[2], f"${item[3]}", f"${item[4]}"),
            tags=("alt" if i % 2 else "normal",))
        total += item[4]
    total_var.set(f"TOTAL:  ${total:,}")
    total_lbl.configure(fg="#DC2626" if total > 0 else TEXT)

def limpiar_pantalla():
    combo_cliente.set(""); combo_producto.set("")
    cantidad.set(""); precio_unitario.set("")
    items_factura.clear(); actualizar_vista()
    status_var.set("Pantalla limpiada.")

def finalizar_factura():
    cliente_sel = combo_cliente.get()
    if not cliente_sel:
        messagebox.showwarning("Atencion", "Seleccione un cliente."); return
    if not items_factura:
        messagebox.showwarning("Atencion", "Agregue al menos un producto."); return

    datos = clientes_dict[cliente_sel]
    dni = datos[3]; nombre = f"{datos[2]}, {datos[1]}"; direccion = datos[4]
    total_final = sum(i[4] for i in items_factura)
    fecha_str   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo     = os.path.join(CARPETA_FACTURAS, f"Factura_{dni}_{ts}.txt")

    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("          FACTURA DE COMPRA\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {fecha_str}\n")
            f.write("-" * 50 + "\n")
            f.write(f"CLIENTE: {nombre}\n")
            f.write(f"DNI: {dni}\n")
            f.write(f"Direccion: {direccion}\n")
            f.write("=" * 50 + "\n")
            f.write(f"{'ID':<5} {'Detalle':<20} {'Cant':<5} {'P.Unit':<8} {'Total':<8}\n")
            f.write("-" * 50 + "\n")
            for item in items_factura:
                f.write(f"{item[0]:<5} {item[1]:<20} {item[2]:<5} ${item[3]:<7} ${item[4]:<7}\n")
            f.write("=" * 50 + "\n")
            f.write(f"TOTAL A PAGAR: ${total_final:,}\n")
            f.write("=" * 50 + "\n")
            f.write("      Gracias por su preferencia.\n")
        messagebox.showinfo("Facturacion", f"Factura generada:\n{os.path.basename(archivo)}")
        status_var.set(f"Factura emitida: {os.path.basename(archivo)}")
        limpiar_pantalla()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la factura:\n{e}")

ventana = tk.Tk()
ventana.title("Facturacion — Industrial del Sur")
ventana.geometry("1020x618"); ventana.resizable(False, False); ventana.configure(bg=BG)

hdr = tk.Frame(ventana, bg=HEADER, height=66)
hdr.pack(fill="x"); hdr.pack_propagate(False)
tk.Label(hdr, text="INDUSTRIAL DEL SUR", font=("Arial",10,"bold"), bg=HEADER, fg="#93C5FD").place(x=18, y=10)
tk.Label(hdr, text="GENERACION DE FACTURAS", font=("Arial",18,"bold"), bg=HEADER, fg=WHITE).place(x=18, y=30)
tk.Frame(ventana, bg=ACCENT, height=3).pack(fill="x")

ftr = tk.Frame(ventana, bg=HEADER, height=26)
ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
status_var = tk.StringVar(value="Seleccione un cliente y agregue productos.")
tk.Label(ftr, textvariable=status_var, font=("Arial",9), bg=HEADER, fg="#93C5FD").pack(side="left", padx=12, pady=4)

cantidad=tk.StringVar(); precio_unitario=tk.StringVar(); total_var=tk.StringVar(value="TOTAL:  $0")

fc = tk.Frame(ventana, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
fc.place(x=24, y=74, width=378, height=518)
fch = tk.Frame(fc, bg=ACCENT, height=36); fch.pack(fill="x"); fch.pack_propagate(False)
tk.Label(fch, text="  Datos de la Venta", font=("Arial",11,"bold"), bg=ACCENT, fg=WHITE).pack(side="left", padx=10, pady=8)

ff = tk.Frame(fc, bg=WHITE, padx=18, pady=12); ff.pack(fill="x")
def lbl(t): return tk.Label(ff, text=t, bg=WHITE, fg=TEXT, font=("Arial",10,"bold"), anchor="w")

lbl("Cliente:").grid(row=0, column=0, sticky="w", pady=(0,4))
combo_cliente = ttk.Combobox(ff, state="readonly", font=("Arial",10))
combo_cliente.grid(row=0, column=1, sticky="ew", pady=(0,4), padx=(10,0))
tk.Frame(ff, bg=BORDER, height=1).grid(row=1, column=0, columnspan=2, sticky="ew", pady=12)
lbl("Producto:").grid(row=2, column=0, sticky="w", pady=(0,4))
combo_producto = ttk.Combobox(ff, state="readonly", font=("Arial",10))
combo_producto.grid(row=2, column=1, sticky="ew", pady=(0,4), padx=(10,0))
combo_producto.bind("<<ComboboxSelected>>", actualizar_precio)
lbl("Precio Unit:").grid(row=3, column=0, sticky="w", pady=(6,4))
tk.Entry(ff, textvariable=precio_unitario, font=("Arial",10), relief="solid", bd=1, state="readonly").grid(row=3, column=1, sticky="ew", pady=(6,4), padx=(10,0))
lbl("Cantidad:").grid(row=4, column=0, sticky="w", pady=(6,4))
tk.Entry(ff, textvariable=cantidad, font=("Arial",10), relief="solid", bd=1).grid(row=4, column=1, sticky="ew", pady=(6,4), padx=(10,0))
ff.columnconfigure(1, weight=1)

tk.Frame(fc, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(4,0))
bf = tk.Frame(fc, bg=WHITE, padx=14, pady=12); bf.pack(fill="x")
flat_btn(bf,"Agregar Producto", agregar_item,    SUCCESS, SUCCESS_H).pack(fill="x", pady=(0,6))
r2 = tk.Frame(bf, bg=WHITE); r2.pack(fill="x", pady=(0,10))
flat_btn(r2,"Emitir Factura", finalizar_factura, ACCENT,  ACCENT_H ).pack(side="left",fill="x",expand=True,padx=(0,4))
flat_btn(r2,"Limpiar Todo",   limpiar_pantalla,  NEUTRAL, NEUTRAL_H).pack(side="left",fill="x",expand=True)
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
tk.Label(tch, text="  Detalle de la Factura", font=("Arial",11,"bold"), bg=HEADER, fg=WHITE).pack(side="left", padx=10, pady=8)

tf = tk.Frame(tc, bg=WHITE); tf.pack(fill="both", expand=True)
vsb = ttk.Scrollbar(tf, orient="vertical"); vsb.pack(side="right", fill="y")
tabla_factura = ttk.Treeview(tf, columns=("id","detalle","cant","precio_u","subtotal"),
                              show="headings", style="I.Treeview", yscrollcommand=vsb.set)
vsb.configure(command=tabla_factura.yview)
for col,txt,w,anch in [("id","ID",52,"center"),("detalle","Detalle del Producto",200,"w"),
    ("cant","Cant.",64,"center"),("precio_u","Precio U.",92,"center"),("subtotal","Subtotal",100,"center")]:
    tabla_factura.heading(col,text=txt); tabla_factura.column(col,width=w,minwidth=w,anchor=anch)
tabla_factura.tag_configure("alt",background=ROW_ALT); tabla_factura.tag_configure("normal",background=WHITE)
tabla_factura.pack(fill="both", expand=True)

total_frame = tk.Frame(tc, bg=WHITE, pady=12); total_frame.pack(fill="x")
tk.Frame(total_frame, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(0,10))
total_lbl = tk.Label(total_frame, textvariable=total_var, font=("Arial",16,"bold"), bg=WHITE, fg=TEXT)
total_lbl.pack(anchor="e", padx=20)

inicializar_entorno(); cargar_datos_combobox()
ventana.mainloop()
