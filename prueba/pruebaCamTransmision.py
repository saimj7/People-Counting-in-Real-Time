import cv2

# Lista de direcciones URL de las cámaras
camera_urls = [
    "rtsp://tapo2912:Riouch2000@192.168.1.11:554/h264/ch1/main/av_stream",
    # "rtsp://tapo2912:Riouch2000@192.168.1.16:554/h264/ch1/main/av_stream",
    # Agregue más direcciones URL aquí si desea visualizar más cámaras
]

# Lista para almacenar las conexiones con las cámaras
caps = []

# Inicializa las conexiones con las cámaras
for url in camera_urls:
    cap = cv2.VideoCapture(url)
    caps.append(cap)

# Verifica si se pudieron inicializar todas las conexiones
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"No se puede conectar a la cámara {i + 1}")
        exit()

# Lee el primer frame de video de cada cámara
frames = []
for i, cap in enumerate(caps):
    ret, frame = cap.read()
    frames.append(frame)

    # Verifica si se pudo leer el primer frame
    if not ret:
        print(f"No se pudo leer el primer frame de la cámara {i + 1}")
        exit()

# Configura las dimensiones de las ventanas
widths = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) for cap in caps]
heights = [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) for cap in caps]

# Crea ventanas para mostrar el video de cada cámara
window_names = [f"Cámara {i + 1}" for i in range(len(camera_urls))]
for i, name in enumerate(window_names):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, widths[i], heights[i])

# Mientras haya frames disponibles en el video de todas las cámaras
while all([cap.isOpened() for cap in caps]):
    # Lee el siguiente frame de cada cámara
    frames = []
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        frames.append(frame)

        # Verifica si se pudo leer el siguiente frame
        if not ret:
            break

    # Muestra el frame en la ventana correspondiente a cada cámara
    for i, frame in enumerate(frames):
        cv2.imshow(window_names[i], frame)

    # Verifica si se presionó la tecla "q" para detener la ejecución
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()
