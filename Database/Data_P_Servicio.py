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

def descifrar_campos_usuario(usuario_dict, campos_a_descifrar):
    """Descifra los campos especificados de un diccionario de usuario"""
    usuario_descifrado = usuario_dict.copy()
    for campo in campos_a_descifrar:
        if campo in usuario_descifrado:
            try:
                usuario_descifrado[campo] = fernet.decrypt(usuario_descifrado[campo].encode()).decode()
            except Exception as e:
                print(f"Error al descifrar el campo '{campo}': {e}")
                usuario_descifrado[campo] = "Dato inválido"
    return usuario_descifrado


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

def Verificar_datos(usuario, contraseña):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = """
        SELECT correo_servicio, nombre_propietario, nit, razon_social, telefono_servicio, contraseña_servicio 
        FROM data_base_servicio 
        WHERE correo_servicio = %s
    """
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        correo, nombre, nit, razon, telefono, contraseña_hash = resultado
        try:
            if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash.encode('utf-8')):
                # Creamos el diccionario con los datos cifrados
                usuario_dict = {
                    "correo": correo,
                    "nombre": nombre,
                    "nit": nit,
                    "razon_social": razon,
                    "telefono": telefono
                }
                # Desciframos los campos antes de retornarlos
                usuario_descifrado = descifrar_campos_usuario(usuario_dict, ['nombre', 'nit', 'razon_social', 'telefono'])
                return usuario_descifrado
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return None
    return None

