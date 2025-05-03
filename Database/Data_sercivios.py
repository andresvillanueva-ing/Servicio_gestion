from .database import crear_conexion
from cryptography.fernet import Fernet
import bcrypt

# Función para agreagr un nuevo servicio a la base de datos
def agregar_servicio(razon_social, nit, adminstrador, ubicacion, imagen):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_servicios (razon_social, nit, adminstrador, ubicacion, imagen) VALUES (%s, %s, %s, %s, %s)"
    valores = (razon_social, nit, adminstrador, ubicacion, imagen)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

# Función para listar todos los servicios en la base de datos
def mostrar_servicios():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM data_servicios")
    for servicio in cursor.fetchall():
        print(servicio) 
    cursor.close()
    conexion.close()
