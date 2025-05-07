from Database.database import crear_conexion
from cryptography.fernet import Fernet

# Leer la clave de cifrado
def obtener_clave():
    with open('clave.key', 'rb') as archivo_clave:
        clave = archivo_clave.read()
    return clave

clave = obtener_clave()
fernet = Fernet(clave)

# Función para agregar una nueva reserva a la base de datos
def agregar_reserva(razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_reservas (razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

