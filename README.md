# 🍊 Sistema de Inspección de Calidad - ITLag

Sistema de control de calidad visual basado en inteligencia artificial (YOLOv8) para clasificar frutas en tiempo real mediante cámara o imágenes estáticas.

---

## 📋 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.9 o superior** → https://www.python.org/downloads/
- **pip** (viene incluido con Python)
- El archivo del modelo entrenado: `best.pt` (debe estar en la misma carpeta que el script)

---

## 📦 Librerías necesarias

| Librería | Versión recomendada | Uso en el proyecto |
|---|---|---|
| `ultralytics` | ≥ 8.0 | Motor de IA YOLOv8 para detección de objetos |
| `opencv-python` | ≥ 4.8 | Captura de cámara, lectura de imágenes y dibujo de cajas |
| `Pillow` | ≥ 10.0 | Puente entre OpenCV y la interfaz gráfica Tkinter |
| `tkinter` | (incluida en Python) | Interfaz gráfica de la aplicación |

---

## 🚀 Pasos para configurar y ejecutar el proyecto

### Paso 1 — Clonar o descargar el proyecto

Descarga o clona los archivos del proyecto en una carpeta de tu elección. Asegúrate de que la estructura quede así:

```
mi_proyecto/
├── main.py
├── best.pt
└── README.md
```

---

### Paso 2 — Crear el entorno virtual

Abre una terminal (CMD, PowerShell o la terminal de tu sistema) dentro de la carpeta del proyecto y ejecuta:

```bash
python -m venv venv
```

Esto creará una carpeta llamada `venv` con un entorno Python aislado.

---

### Paso 3 — Activar el entorno virtual

**En Windows:**
```bash
venv\Scripts\activate
```

**En macOS / Linux:**
```bash
source venv/bin/activate
```

Sabrás que está activo porque verás `(venv)` al inicio de tu línea de comandos.

---

### Paso 4 — Instalar las librerías

Con el entorno virtual activo, instala todas las dependencias con un solo comando:

```bash
pip install ultralytics opencv-python Pillow
```

> ⚠️ La instalación de `ultralytics` puede tardar varios minutos ya que descarga PyTorch y otras dependencias automáticamente.

Para verificar que todo se instaló correctamente:

```bash
pip list
```

---

### Paso 5 — Ejecutar el proyecto

Con el entorno virtual aún activo, corre el script principal:

```bash
python main.py
```

La aplicación abrirá una ventana con el sistema de inspección listo para usar.

---

## 🖥️ Uso de la aplicación

Una vez abierta la ventana, tienes dos modos disponibles:

- **📁 Cargar Imagen** — Selecciona una foto `.jpg`, `.jpeg` o `.png` de tu equipo para analizarla.
- **📷 Activar Cámara** — Enciende la cámara web para inspección en tiempo real.

Los resultados aparecen en el panel lateral:
- 🟢 **COMESTIBLES** — Frutas clasificadas como sanas y sin solapamiento con defectos.
- 🔴 **DEFECTUOSAS** — Frutas con algún defecto detectado (inmaduras, dañadas, etc.).

---

## ❌ Desactivar el entorno virtual

Cuando termines de trabajar, puedes desactivar el entorno con:

```bash
deactivate
```

---

## 🛠️ Solución de problemas comunes

**Error: `No module named 'tkinter'`**
> En Linux, tkinter no viene preinstalado. Instálalo con:
> ```bash
> sudo apt-get install python3-tk
> ```

**Error: `best.pt not found`**
> Asegúrate de que el archivo `best.pt` esté en la **misma carpeta** que `main.py`.

**La cámara no enciende**
> Verifica que ninguna otra aplicación esté usando la cámara. También puedes cambiar el índice de cámara en el código (`cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`).

**Instalación lenta de `ultralytics`**
> Es normal. Descarga PyTorch (~700 MB). Asegúrate de tener buena conexión a internet.

---

## 📁 Estructura final del proyecto

```
mi_proyecto/
├── venv/               ← Entorno virtual (no subir a Git)
├── main.py             ← Script principal
├── best.pt             ← Modelo YOLOv8 entrenado
└── README.md           ← Este archivo
```

---

> Desarrollado en **ITLag** — Sistema de Inspección de Calidad con IA 🤖
