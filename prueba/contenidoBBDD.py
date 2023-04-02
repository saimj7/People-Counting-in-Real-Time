# Importar el módulo sqlite3
import mysql.connector

# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
		host="localhost",
		user="root",
		password="12345678"
	)

# Crear el objeto Cursor
cur = conn.cursor()
#Usar la base de datos creada
cur.execute("USE db")
# Ejecutar la sentencia SELECT para obtener todos los registros de la tabla
cur.execute("SELECT * FROM biblioteca")
# Obtener los datos como una lista de tuplas
datos = cur.fetchall()
# Recorrer la lista y mostrar cada tupla
for biblioteca in datos:
  print(biblioteca)