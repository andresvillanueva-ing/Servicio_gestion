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
def agregar_reserva(id_prestador, razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, id_usuario, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_reservas (id_prestador, razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, id_usuario, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (id_prestador, razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, id_usuario, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_reservas_realizadas(id_usuario):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "SELECT razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva FROM data_reservas WHERE id_usuario = %s"
    cursor.execute(sql, (id_usuario,))
    reservas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return[
        {
            "razon_social": seguro_descifrar(row[0]),
            "nit": seguro_descifrar(row[1]),
            "administrador": seguro_descifrar(row[2]),
            "ubicacion": row[3],
            "tipo_servicio":row[4],
            "imagen": row[5],
            "nombre_cliente": seguro_descifrar(row[6]),
            "telefono_cliente": seguro_descifrar(row[7]),
            "correo_cliente": row[8],
            "hora_reserva": row[9],
            "fecha_reserva": row[10],
        }
        for row in reservas
    ]

def obtener_reservas(id_prestador):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "SELECT razon_social, nit, administrador, ubicacion, tipo_servicio, imagen, id_usuario, nombre_cliente, telefono_cliente, correo_cliente, hora_reserva, fecha_reserva FROM data_reservas WHERE id_prestador = %s"
    cursor.execute(sql, (id_prestador,))
    reservas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return[
        {
            "razon_social": seguro_descifrar(row[0]),
            "nit": seguro_descifrar(row[1]),
            "administrador": seguro_descifrar(row[2]),
            "ubicacion": row[3],
            "tipo_servicio":row[4],
            "imagen": row[5],
            "id_usuario": row[6],
            "nombre_cliente": seguro_descifrar(row[7]),
            "telefono_cliente": seguro_descifrar(row[8]),
            "correo_cliente": row[9],
            "hora_reserva": row[10],
            "fecha_reserva": row[11],
        }
        for row in reservas
    ]

def seguro_descifrar(valor):
    try:
        return fernet.decrypt(valor).decode()
    except Exception:
        return "[ERROR DESCIFRADO]"