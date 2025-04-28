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

def agregar_usuario(nombre_usuario, correo_usuario, telefono_usuario, contraseña_usuario):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO data_base_usuario (nombre_usuario, correo_usuario, telefono_usuario, contraseña_usuario) VALUES (%s, %s, %s, %s)"
    valores = (nombre_usuario, correo_usuario, telefono_usuario, contraseña_usuario)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()
    print('Usuario registrado con exito')

def listar_usuario():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM data_base_usuario")
    for usaurio in  cursor.fetchall():
        print(usaurio)
    cursor.close()
    conexion.close()

#funcion para verificar datos de correo y contraseña

def Verificar_datos_usuario(usuario, contraseña):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Buscar en la base de datos el correo en texto plano
    sql = "SELECT contraseña_usuario FROM data_base_usuario WHERE correo_usuario = %s"
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