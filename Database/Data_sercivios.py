from .database import crear_conexion
from cryptography.fernet import Fernet
import bcrypt

# Leer la clave de cifrado
def obtener_clave():
    with open('clave.key', 'rb') as archivo_clave:
        clave = archivo_clave.read()
    return clave

clave = obtener_clave()
fernet = Fernet(clave)

# Función para agreagr un nuevo servicio a la base de datos
def agregar_servicio(razon_social, nit,tipo_servicio, administrador, puestos, ubicacion, imagen):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_servicios (razon_social, nit, tipo_servicio, administrador, puestos, ubicacion, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    valores = (razon_social, nit, tipo_servicio, administrador, puestos, ubicacion, imagen)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

# Función para listar todos los servicios en la base de datos
def obtener_servicios_por_tipo(tipo_servicio):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "SELECT razon_social, administrador, ubicacion, imagen FROM data_servicios WHERE tipo_servicio = %s"
    cursor.execute(sql, (tipo_servicio,))
    servicios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return [
        {
            "razon_social": fernet.decrypt(row[0]).decode(),
            "administrador": fernet.decrypt(row[1]).decode(),
            "ubicacion": row[2],
            "imagen": row[3],
        }
        for row in servicios
    ]