import ping3

response = ping3.ping('192.168.1.11')
if response is not None:
    print("La cámara está disponible en la red.")
else:
    print("La cámara no está disponible en la red.")
