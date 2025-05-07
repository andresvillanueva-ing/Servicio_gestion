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

def obtener_reservas_realizadas():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "SELECT razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva FROM data_reservas WHERE id = %s"
    cursor.execute(sql, (id,))
    reservas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return[
        {
            "razon_social": fernet.decrypt(row[0]).decode(),
            "nit": fernet.decrypt(row[1]).decode(),
            "administrador": fernet.decrypt(row[2]).decode(),
            "ubicacion": row[3],
            "tipo_servicio": fernet.decrypt(row[4]).decode(),
            "imagen": row[5],
            "nombre_cliente": fernet.decrypt(row[6]).decode(),
            "telefono_cliente": fernet.decrypt(row[7]).decode(),
            "correo_cliente": fernet.decrypt(row[8]).decode(),
            "hora_reserva": row[9],
            "fecha_reserva": row[10],
        }
        for row in reservas
    ]