import cv2
import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk
from ultralytics import YOLO

# --- FUNCIÓN MATEMÁTICA PARA MEDIR EL EMPALME (IoU) ---
def calcular_empalme(caja1, caja2):
    xA, yA = max(caja1[0], caja2[0]), max(caja1[1], caja2[1])
    xB, yB = min(caja1[2], caja2[2]), min(caja1[3], caja2[3])
    area_interseccion = max(0, xB - xA) * max(0, yB - yA)
    area_caja1 = (caja1[2] - caja1[0]) * (caja1[3] - caja1[1])
    area_caja2 = (caja2[2] - caja2[0]) * (caja2[3] - caja2[1])
    
    if (area_caja1 + area_caja2 - area_interseccion) == 0: return 0
    return area_interseccion / float(area_caja1 + area_caja2 - area_interseccion)

print("Cargando el motor de IA...")
modelo = YOLO("best.pt")

camara = None
modo_camara_activo = False

# --- MOTOR PRINCIPAL DE PROCESAMIENTO ---
def procesar_imagen(frame, es_video=False):
    if es_video:
        frame = cv2.flip(frame, 1)

    resultados = modelo.predict(frame, stream=True, conf=0.40, verbose=False)
    cajas_buenas, cajas_malas = [], []
    
    for resultado in resultados:
        for caja in resultado.boxes:
            coords = list(map(int, caja.xyxy[0]))
            confianza = float(caja.conf[0])
            nombre_clase = modelo.names[int(caja.cls[0])]

            # ==========================================
            # FILTRO DE EMERGENCIA PARA LA DEMOSTRACIÓN
            # ==========================================
            if nombre_clase == "Inmadura" and confianza < 0.60:
                continue  # Ignora la caja por completo y pasa a la siguiente
            # ==========================================

            datos = {"coords": coords, "conf": confianza, "clase": nombre_clase}
            
            if nombre_clase == "Comestible": cajas_buenas.append(datos)
            else: cajas_malas.append(datos)

    contador_sanas = 0
    contador_alertas = len(cajas_malas)

    # Dibujar Alertas (Rojo)
    for mala in cajas_malas:
        x1, y1, x2, y2 = mala["coords"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(frame, f"{mala['clase']} {mala['conf']:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Dibujar Comestibles Seguras (Verde)
    for buena in cajas_buenas:
        es_segura = True
        for mala in cajas_malas:
            if calcular_empalme(buena["coords"], mala["coords"]) > 0.10:
                es_segura = False
                break
        
        if es_segura:
            contador_sanas += 1
            x1, y1, x2, y2 = buena["coords"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Sana {buena['conf']:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame, contador_sanas, contador_alertas

# --- FUNCIONES DE LA INTERFAZ ---
def actualizar_visor(imagen_cv2):
    imagen_cv2 = cv2.resize(imagen_cv2, (640, 480))
    imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(imagen_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    
    lbl_visor.imgtk = img_tk
    lbl_visor.configure(image=img_tk)

def bucle_camara():
    global modo_camara_activo
    if modo_camara_activo and camara is not None:
        exito, frame = camara.read()
        if exito:
            frame_procesado, sanas, alertas = procesar_imagen(frame, es_video=True)
            actualizar_visor(frame_procesado)
            lbl_sanas.config(text=str(sanas))
            lbl_alertas.config(text=str(alertas))
        ventana.after(15, bucle_camara)

def encender_camara():
    global camara, modo_camara_activo
    if not modo_camara_activo:
        camara = cv2.VideoCapture(0)
        camara.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        modo_camara_activo = True
        bucle_camara()

def detener_camara():
    global camara, modo_camara_activo
    modo_camara_activo = False
    if camara is not None:
        camara.release()
        camara = None

def cargar_imagen():
    detener_camara()
    ruta = filedialog.askopenfilename(title="Selecciona una imagen de naranjas", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
    if ruta:
        imagen = cv2.imread(ruta)
        if imagen is not None:
            img_procesada, sanas, alertas = procesar_imagen(imagen, es_video=False)
            actualizar_visor(img_procesada)
            lbl_sanas.config(text=str(sanas))
            lbl_alertas.config(text=str(alertas))

def salir():
    detener_camara()
    ventana.quit()

# --- DISEÑO GRÁFICO (UI) ---
ventana = tk.Tk()
ventana.title("Sistema de Control de Calidad")
ventana.geometry("900x550")
ventana.configure(bg="#2B2B2B")

fuente_titulos = font.Font(family="Segoe UI", size=14, weight="bold")
fuente_numeros = font.Font(family="Segoe UI", size=28, weight="bold")
fuente_botones = font.Font(family="Segoe UI", size=11, weight="bold")

panel_lateral = tk.Frame(ventana, bg="#1E1E1E", width=250)
panel_lateral.pack(side="left", fill="y")
panel_lateral.pack_propagate(False)

lbl_logo = tk.Label(panel_lateral, text="🔍 INSPECCIÓN\nITLag", fg="#FFFFFF", bg="#1E1E1E", font=fuente_titulos)
lbl_logo.pack(pady=30)

btn_imagen = tk.Button(panel_lateral, text="📁 Cargar Imagen", bg="#3498DB", fg="white", font=fuente_botones, relief="flat", command=cargar_imagen)
btn_imagen.pack(fill="x", padx=20, pady=10, ipady=5)

btn_camara = tk.Button(panel_lateral, text="📷 Activar Cámara", bg="#9B59B6", fg="white", font=fuente_botones, relief="flat", command=encender_camara)
btn_camara.pack(fill="x", padx=20, pady=10, ipady=5)

lbl_tit_sanas = tk.Label(panel_lateral, text="COMESTIBLES", fg="#2ECC71", bg="#1E1E1E", font=("Segoe UI", 10, "bold"))
lbl_tit_sanas.pack(pady=(30, 0))
lbl_sanas = tk.Label(panel_lateral, text="-", fg="#2ECC71", bg="#1E1E1E", font=fuente_numeros)
lbl_sanas.pack()

lbl_tit_alertas = tk.Label(panel_lateral, text="DEFECTUOSAS", fg="#E74C3C", bg="#1E1E1E", font=("Segoe UI", 10, "bold"))
lbl_tit_alertas.pack(pady=(20, 0))
lbl_alertas = tk.Label(panel_lateral, text="-", fg="#E74C3C", bg="#1E1E1E", font=fuente_numeros)
lbl_alertas.pack()

btn_salir = tk.Button(panel_lateral, text="Salir", bg="#E74C3C", fg="white", font=fuente_botones, relief="flat", command=salir)
btn_salir.pack(side="bottom", fill="x", padx=20, pady=20, ipady=5)

panel_principal = tk.Frame(ventana, bg="#2B2B2B")
panel_principal.pack(side="right", expand=True, fill="both")

lbl_visor = tk.Label(panel_principal, bg="#000000", text="Esperando entrada de imagen/video...", fg="#7F8C8D", font=("Segoe UI", 12))
lbl_visor.pack(expand=True)

ventana.mainloop()