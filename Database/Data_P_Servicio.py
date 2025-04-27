from .database import crear_conexion
from cryptography.fernet import Fernet

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

def obtener_clave():
    with open('clave.key', 'r') as archivo_clave:
        clave = archivo_clave.read()
    return clave

def Verificar_datos(usuario, contraseña):

    # Leer la clave
    clave = obtener_clave()
    f = Fernet(clave)

    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Buscar en la base de datos por correo
    sql = "SELECT contraseña_servicio FROM data_base_servicio WHERE correo_servicio = %s"
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        contraseña_encriptada = resultado[0]  # la contraseña guardada en BD
        try:
            # Desencriptar
            contraseña_desencriptada = f.decrypt(contraseña_encriptada.encode('utf-8')).decode('utf-8')
            # Comparar
            if contraseña_desencriptada == contraseña:
                return True
            else:
                return False
        except Exception as e:
            print("Error al desencriptar:", e)
            return False
    else:
        return False

