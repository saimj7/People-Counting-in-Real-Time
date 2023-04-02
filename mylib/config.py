#===============================================================================
""" Optional features config. """
#===============================================================================
# Enter mail below to receive real-time email alerts
# e.g., 'email@gmail.com'
MAIL = ''
# Enter the ip camera url (e.g., url = 'http://191.138.0.100:8040/video')
url = "rtsp://tapo2912:Riouch2000@192.168.1.11:554/h264/ch1/main/av_stream"

# ON/OFF for mail feature. Enter True to turn on the email alert feature.
ALERT = False
# Set max. people inside limit. Optimise number below: 10, 50, 100, etc.
Threshold = 10
# Threading ON/OFF
Thread = False
# Auto run/Schedule the software to run at your desired time
Scheduler = False
# Auto stop the software after certain a time/hours
Timer = False

#Variables de configuración

#Definir las variables de la línea
line_color = (0, 0, 0)  #Color de la línea en formato BGR
line_thickness = 3      #Grosor de la línea en píxeles
line_position = 140     #Posición verticall de la línea

#Definir las variables del recorte de la imagen: pixel_start= en que pixel comienza la imagen y pixel_end= a donde termina la imagen
pixel_start_height = 0
pixel_start_width = 0
pixel_end_height = 500
pixel_end_width = 500

#Tamaño máximo de nuestra frame en pixels
frame_size = 500

# Dirección entrada y salida
downIsEntry = False
#Argumentos
prototxt = "mobilenet_ssd/MobileNetSSD_deploy.prototxt"
model = "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"

#===============================================================================
#===============================================================================
