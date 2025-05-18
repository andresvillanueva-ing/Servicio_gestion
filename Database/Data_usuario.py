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
    sql ="""
            SELECT id, nombre_usuario, telefono_usuario, correo_usuario, contraseña_usuario
            FROM data_base_usuario WHERE correo_usuario = %s
        """
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        id, correo_usuario, nombre_nombre, telefono_usuario, hast_contraseña = resultado
        try:
            if bcrypt.checkpw(contraseña.encode('utf-8'), hast_contraseña.encode('utf-8')):
                # Creamos el diccionario con los datos cifrados
                usuario_dict = {
                    "id": id,
                    "correo": correo_usuario,
                    "nombre": nombre_nombre,
                    "telefono": telefono_usuario,
                }
                # Desciframos los campos antes de retornarlos
                usuario_descifrado = descifrar_campos_usuario(usuario_dict, ['nombre_usuario', 'correo_usuario', 'telefono_usuario'])
                return usuario_descifrado
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return None