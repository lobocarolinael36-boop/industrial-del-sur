# Sistema Industrial del Sur

Sistema de gestión de escritorio desarrollado en Python con interfaz gráfica (tkinter).  
Permite administrar clientes, proveedores, productos y generar facturas de compra.

**Materia:** Desarrollo de Sistemas | **Autora:** Carolina Lobo | **Año:** 2026

---

## Módulos del sistema

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| Menú Principal | `menu.py` | Punto de entrada del sistema |
| Gestión de Clientes | `cli.py` | ABM de clientes (alta, baja, modificación) |
| Gestión de Proveedores | `prov.py` | ABM de proveedores |
| Gestión de Productos | `prod.py` | ABM de productos con talle, color y precio |
| Facturación | `fact.py` | Generación de facturas por cliente y productos |

---

## Cómo ejecutar

**Requisitos:** Python 3.10 o superior con tkinter (incluido en la instalación estándar).

```bash
python menu.py
```

Los archivos de datos (`clientes.txt`, `proveedores.txt`, `productos.txt`) y la carpeta `facturas_emitidas/` se crean automáticamente al primer uso.

---

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [Manual de Instalación y Rollback](Manual_de_Instalacion_y_Rollback_Industrial_del_Sur.docx) | Requisitos, pasos de instalación, desinstalación, backup y recuperación |
| [Soporte y Garantía](Soporte_y_Garantia_Industrial_del_Sur.docx) | Período de soporte, canales de atención, clasificación de incidentes y exclusiones |
| [Manual de Usuario](Manual_de_Usuario_Industrial_del_Sur_Caro_Lobo.docx) | Guía de uso de cada módulo del sistema |
| [Documento de Pruebas](Documento_de_Pruebas_Sistema_Industrial_del_Sur.docx) | Casos de prueba y resultados esperados |

---

## Estructura del proyecto

```
industriSur/
├── menu.py                          # Menú principal
├── cli.py                           # Módulo clientes
├── prov.py                          # Módulo proveedores
├── prod.py                          # Módulo productos
├── fact.py                          # Módulo facturación
├── clientes.txt                     # Datos de clientes
├── proveedores.txt                  # Datos de proveedores
├── productos.txt                    # Datos de productos
├── facturas_emitidas/               # Facturas generadas (.txt)
├── Manual_de_Instalacion_y_Rollback_Industrial_del_Sur.docx
├── Soporte_y_Garantia_Industrial_del_Sur.docx
├── Manual_de_Usuario_Industrial_del_Sur_Caro_Lobo.docx
└── Documento_de_Pruebas_Sistema_Industrial_del_Sur.docx
```

---

## Almacenamiento de datos

Los datos se guardan en archivos `.txt` con `|` como separador de campos:

```
clientes.txt     → ID | Nombre | Apellido | DNI | Dirección | Estado
proveedores.txt  → ID | Razón Social | CUIT | Rubro | Contacto | Estado
productos.txt    → ID | Detalle | Talle | Color | Precio | Estado
```

---

*Proyecto escolar — Escuela Técnica — Materia: Desarrollo de Sistemas*
