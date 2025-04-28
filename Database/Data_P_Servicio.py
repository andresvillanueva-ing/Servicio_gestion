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

def agregar_prestador_servicio(correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO data_base_servicio 
        (correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def listar_usuario():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM data_base_servicio")
    for prestador in cursor.fetchall():
        print(prestador)
    cursor.close()
    conexion.close()

def Verificar_datos(usuario, contraseña):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Buscar en la base de datos el correo en texto plano
    sql = "SELECT contraseña_servicio FROM data_base_servicio WHERE correo_servicio = %s"
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        contraseña_hash = resultado[0]
        try:
            # Comparar la contraseña introducida con el hash almacenado
            if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash.encode('utf-8')):
                return True
            else:
                return False
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return False
    else:
        return False
