from .database import crear_conexion

def agregar_prestador_servicio(correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_base_servicio (correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def listar_usuario():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM data_base_servicio")
    for prestador in  cursor.fetchall():
        print(prestador)
    cursor.close()
    conexion.close()