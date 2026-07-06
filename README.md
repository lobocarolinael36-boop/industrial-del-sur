# INDUSTRIAL DEL SUR — Sistema de Gestión Comercial

> Sistema de escritorio en **Python + tkinter** para la gestión de clientes, proveedores, productos y generación de facturas.
>
> **Materia:** Desarrollo de Sistemas &nbsp;|&nbsp; **Autora:** Carolina Lobo &nbsp;|&nbsp; **Año:** 2026

---

## DER — Diagrama Entidad-Relación

![DER Industrial del Sur](docs/DER.svg)

---

## Instalación y ejecución

**Requisito:** Python 3.10 o superior con tkinter (incluido por defecto en Windows).

```bash
# Verificar Python
python --version

# Ejecutar el sistema
python iniciar.py
```

Los archivos de datos (`clientes.txt`, `proveedores.txt`, `productos.txt`) y la carpeta `facturas_emitidas/` se crean automáticamente dentro de `data/` la primera vez que se usa cada módulo.

---

## Módulos del sistema

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| Menú Principal | `src/menu.py` | Punto de entrada del sistema |
| Gestión de Clientes | `src/cli.py` | ABM de clientes |
| Gestión de Proveedores | `src/prov.py` | ABM de proveedores |
| Gestión de Productos | `src/prod.py` | ABM de productos con talle, color y precio |
| Facturación | `src/fact.py` | Generación de facturas por cliente y productos |
| Gestión de Usuarios | `src/usuarios.py` | ABM de usuarios con roles y estados |

---

## Documentación

| Archivo | Descripción |
|---------|-------------|
| [Manual de Instalación y Rollback](docs/Manual_Instalacion_Rollback.docx) | Requisitos, instalación, rollback, backup y recuperación |
| [Soporte y Garantía](docs/Soporte_Garantia.docx) | Período, canales, incidentes, horarios y exclusiones |
| [Manual de Usuario](docs/Manual_Usuario.docx) | Guía de uso de cada módulo |
| [Documento de Pruebas](docs/Documento_Pruebas.docx) | Casos de prueba y resultados |

---

<details>
<summary><strong>📋 Manual de Instalación y Rollback</strong> — ver contenido completo</summary>

<br>

## 1. Requisitos de Hardware y Software

### 1.1 Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Procesador | Intel Core i3 / AMD equivalente | Intel Core i5 o superior |
| Memoria RAM | 2 GB | 4 GB o más |
| Espacio en disco | 100 MB libres | 500 MB libres |
| Monitor | Resolución 1024×768 | Resolución 1366×768 o superior |
| Sistema operativo | Windows 10 (64 bits) | Windows 10/11 (64 bits) |

### 1.2 Requisitos de Software

- **Python 3.10 o superior** — [python.org/downloads](https://www.python.org/downloads/)
- **Módulo tkinter** — incluido en la instalación estándar de Python
- No requiere bases de datos ni servidores externos
- No requiere conexión a Internet durante el uso

---

## 2. Instalación del Sistema

**Paso 1 — Instalar Python**
Descargar Python 3.10+ desde python.org. Durante la instalación marcar la opción **"Add Python to PATH"** y completar con los valores por defecto.

**Paso 2 — Verificar la instalación**
```
python --version
```
Debe mostrar la versión instalada (ej: `Python 3.11.4`).

**Paso 3 — Obtener los archivos del sistema**
Copiar la carpeta completa del repositorio al equipo. Ejemplo:
```
C:\Sistemas\industriSur
```
La carpeta debe contener: `iniciar.py` y la carpeta `src/` con todos los módulos.

**Paso 4 — Ejecutar el sistema**
```
cd C:\Sistemas\industriSur
python iniciar.py
```
Se abrirá la ventana gráfica del Menú Principal.

---

## 3. Configuración Inicial

### 3.1 Archivos y directorios creados automáticamente

Al ejecutar el sistema por primera vez se crean automáticamente, sin intervención del usuario:

- `clientes.txt` — datos de clientes
- `proveedores.txt` — datos de proveedores
- `productos.txt` — datos de productos
- `facturas_emitidas/` — carpeta donde se guardan las facturas generadas

### 3.2 Estructura de los archivos de datos

Los archivos `.txt` usan `|` (pipe) como separador. Cada línea es un registro:

| Archivo | Estructura |
|---------|------------|
| `clientes.txt` | ID \| Nombre \| Apellido \| DNI \| Dirección \| Estado |
| `proveedores.txt` | ID \| Razón Social \| CUIT \| Rubro \| Contacto \| Estado |
| `productos.txt` | ID \| Detalle \| Talle \| Color \| Precio \| Estado |

---

## 4. Desinstalación y Rollback

### 4.1 Desinstalación

1. Cerrar todas las ventanas del sistema
2. Eliminar la carpeta del sistema con todo su contenido
3. El sistema **no escribe en el registro de Windows** ni en otras ubicaciones
4. Python puede desinstalarse desde *Panel de Control → Programas → Desinstalar*

### 4.2 Procedimiento de Rollback

En caso de actualización fallida o comportamiento inesperado:

1. **Detener el sistema** — cerrar todas las ventanas abiertas
2. **Reemplazar archivos** — restaurar la carpeta `src/` desde la copia de seguridad anterior (ver Sección 5)
3. **Verificar datos** — cada línea de los `.txt` debe tener exactamente los campos correctos separados por `|`
4. **Reiniciar** — ejecutar nuevamente `python iniciar.py`

---

## 5. Backup y Copia de Seguridad

### 5.1 ¿Qué copiar?

- **Código fuente:** carpeta `src/` completa e `iniciar.py`
- **Datos:** carpeta `data/` completa (`clientes.txt`, `proveedores.txt`, `productos.txt`, `usuarios.txt`)
- **Facturas:** carpeta `data/facturas_emitidas/`

### 5.2 Frecuencia recomendada

| Tipo de Backup | Frecuencia | Qué incluye |
|----------------|------------|-------------|
| Backup completo | Semanal | Toda la carpeta del sistema |
| Backup de datos | Diario | Solo los `.txt` y `facturas_emitidas/` |
| Backup antes de cambios | Antes de modificar código | Los `.py` que se van a editar |

### 5.3 Cómo realizar el backup

Copiar la carpeta completa a:
- Pendrive o disco externo
- Google Drive, OneDrive u otro servicio en la nube

Nombrar la copia con la fecha. Ejemplo: `industriSur_backup_2026-06-19`

---

## 6. Recuperación de Backup

### Caso 1 — Pérdida de código fuente

1. Localizar la copia de seguridad más reciente
2. Copiar los `.py` al directorio del sistema
3. Verificar que la carpeta `src/` contenga todos los módulos
4. Ejecutar `python iniciar.py` para verificar

### Caso 2 — Pérdida o corrupción de datos (.txt)

1. Restaurar el archivo `.txt` desde el backup
2. Si no hay backup, el sistema crea un archivo vacío automáticamente al iniciar. **Se perderán los datos no respaldados**
3. Mantener al menos 2 copias de backup en ubicaciones distintas

### Caso 3 — Pérdida de facturas emitidas

1. Restaurar desde el backup más reciente
2. Sin backup, las facturas se pierden definitivamente (no hay base de datos centralizada)
3. El sistema recreará la carpeta `facturas_emitidas/` automáticamente al próximo uso

> ⚠ **Importante:** el sistema guarda toda la información en archivos de texto plano sin redundancia. Un backup reciente puede ser la diferencia entre recuperar el trabajo o comenzar desde cero.

</details>

---

<details>
<summary><strong>🛠 Soporte y Garantía</strong> — ver contenido completo</summary>

<br>

## 1. Período de Soporte

| Etapa | Duración / Condiciones |
|-------|------------------------|
| Garantía inicial | 6 meses desde la entrega (hasta diciembre 2026) |
| Soporte post-garantía | A convenir — consultar disponibilidad |
| Vigencia del documento | Válido para la versión 1.0 del sistema |

Durante el período de garantía, los incidentes relacionados con el funcionamiento del sistema se atienden **sin costo adicional**, dentro de los plazos definidos en este documento.

---

## 2. Servicios Incluidos

Durante la garantía activa se incluyen:

- ✅ Corrección de errores (bugs) del funcionamiento normal
- ✅ Asistencia para la instalación y configuración inicial
- ✅ Orientación sobre el uso correcto de los módulos
- ✅ Asistencia en la recuperación de datos ante errores del sistema (no por uso indebido)
- ✅ Actualizaciones correctivas para la versión actual
- ✅ Orientación sobre el procedimiento de backup y recuperación

❌ **No se incluyen:** nuevas funcionalidades, capacitación extendida ni soporte para modificaciones realizadas por terceros.

---

## 3. Clasificación de Incidentes y Tiempos de Resolución

| Prioridad | Clasificación | Tiempo de Resolución | Ejemplo |
|-----------|---------------|----------------------|---------|
| **ALTA** | Crítico | 24–48 hs hábiles | El sistema no inicia o pierde datos |
| **MEDIA** | Funcional | 3–5 días hábiles | Un módulo no funciona correctamente |
| **BAJA** | Consulta / Mejora | 5–10 días hábiles | Dudas de uso, sugerencias |

Los tiempos comienzan desde la **confirmación de recepción** del reporte. En incidentes críticos se realiza contacto inicial dentro de las primeras **4 horas hábiles**.

---

## 4. Canales de Atención

| Canal | Detalle |
|-------|---------|
| Correo electrónico | lobocarolina99@gmail.com |
| GitHub Issues | Reportar incidentes en el repositorio del proyecto |
| Presencial (escolar) | Consultas durante horario de cursada — Desarrollo de Sistemas |

Para una atención más rápida, incluir en el reporte:
- Descripción detallada del problema
- Pasos para reproducir el error
- Capturas de pantalla si es posible
- Versión del SO y Python instalada

---

## 5. Horarios de Atención

| Día | Horario |
|-----|---------|
| Lunes a Viernes | 09:00 a 18:00 hs |
| Sábados | 10:00 a 14:00 hs |
| Domingos y feriados | Sin atención |

Las consultas fuera de horario se responden el siguiente día hábil.
En períodos de receso escolar los tiempos pueden extenderse hasta el doble.

---

## 6. Exclusiones

El soporte y garantía **NO cubre** las siguientes situaciones:

- Daños por uso incorrecto, modificaciones no autorizadas o eliminación voluntaria de archivos
- Problemas por versiones de Python distintas a las indicadas en el manual
- Pérdida de datos por falta de backup cuando el usuario fue informado del procedimiento
- Ataques de virus, malware o problemas de seguridad ajenos al sistema
- Solicitudes de nuevas funcionalidades fuera del alcance original
- Soporte para sistemas operativos distintos a Windows (el sistema fue diseñado y probado en Windows)
- Incidentes reportados fuera del período de garantía activo

> Para dudas sobre si una situación está cubierta, comunicarse **antes** de realizar cambios en el sistema.

---

**Contacto:** Carolina Lobo — lobocarolina99@gmail.com

</details>

---

## Estructura del repositorio

```
industrial-del-sur/
├── iniciar.py                 # Lanzador principal
├── src/                       # Código fuente
│   ├── menu.py                # Menú principal
│   ├── cli.py                 # Módulo clientes
│   ├── prov.py                # Módulo proveedores
│   ├── prod.py                # Módulo productos
│   ├── fact.py                # Módulo facturación
│   └── usuarios.py            # Módulo usuarios
├── data/                      # Datos generados en tiempo de ejecución
│   ├── clientes.txt
│   ├── proveedores.txt
│   ├── productos.txt
│   └── facturas_emitidas/     # Facturas generadas (.txt)
└── docs/                      # Documentación del proyecto
    ├── DER.svg                           # Diagrama Entidad-Relación
    ├── Manual_Instalacion_Rollback.docx  # Manual instalación
    ├── Soporte_Garantia.docx             # Soporte y garantía
    ├── Manual_Usuario.docx               # Manual de usuario
    └── Documento_Pruebas.docx            # Documento de pruebas
```

---

## Almacenamiento de datos

Todos los datos se persisten en archivos `.txt` con `|` como separador:

```
data/clientes.txt     →  ID | Nombre | Apellido | DNI | Dirección | Estado
data/proveedores.txt  →  ID | Razón Social | CUIT | Rubro | Teléfono | Estado
data/productos.txt    →  ID | Detalle | Talle | Color | Precio | Estado
data/usuarios.txt     →  ID | Nombre | Apellido | Password | Rol | Estado | FechaModificacion
```

Las facturas se guardan como archivos `.txt` en `data/facturas_emitidas/` con el formato:
```
Factura_<DNI>_<YYYYMMDD_HHMMSS>.txt
```

---

*Proyecto escolar — Escuela Técnica — Materia: Desarrollo de Sistemas — 2026*
