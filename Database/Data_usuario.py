"""Conexion con la tabla de usaurio."""

import bcrypt

from cryptography.fernet import Fernet

from .database import crear_conexion


# Leer la clave de cifrado
def obtener_clave():
    with open("clave.key", "rb") as archivo_clave:
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
                usuario_descifrado[campo] = fernet.decrypt(
                    usuario_descifrado[campo].encode()
                ).decode()
            except Exception as e:
                print(f"Error al descifrar el campo '{campo}': {e}")
                usuario_descifrado[campo] = "Dato inválido"
    return usuario_descifrado


def agregar_usuario(nombre, correo, telefono, contraseña_usuario):
    """Metodo para registrar los datos del cliente."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO data_base_usuario (nombre, correo, telefono, contraseña_usuario) 
        VALUES (%s, %s, %s, %s)
    """
    valores = (nombre, correo, telefono, contraseña_usuario)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


# funcion para verificar datos de correo y contraseña


def Verificar_datos_usuario(usuario, contraseña):
    """Metodo para verificar los datos del usuario."""

    conexion = crear_conexion()
    cursor = conexion.cursor(buffered=True)  # ← Esto es importante

    sql = """
        SELECT id, nombre, telefono, correo, contraseña_usuario
        FROM data_base_usuario WHERE correo = %s
    """
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    if resultado:
        id, nombre, telefono, correo, hash_contraseña = resultado
        try:
            if bcrypt.checkpw(
                contraseña.encode("utf-8"), hash_contraseña.encode("utf-8")
            ):
                usuario_dict = {
                    "id": id,
                    "nombre": nombre,
                    "telefono": telefono,
                    "correo": correo,
                }
                # Descifrar los campos
                usuario_descifrado = descifrar_campos_usuario(
                    usuario_dict, ["nombre", "correo", "telefono"]
                )

                cursor.close()
                conexion.close()

                return usuario_descifrado
        except Exception as e:
            print("Error al verificar contraseña:", e)

    cursor.close()
    conexion.close()
    return None


def obtener_usuario(id_usuario):
    """Metodo para obtener los datos del usuario por su ID."""

    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, correo, telefono, id FROM data_base_usuario WHERE id = %s",
        (id_usuario,),
    )
    row = cursor.fetchone()

    cursor.close()
    conexion.close()

    if row:
        return {
            "nombre": fernet.decrypt(row[0]).decode(),
            "correo": row[1],
            "telefono": fernet.decrypt(row[2]).decode(),
            "id": row[3],
        }
    else:
        return None


def modificar_usuario(nombre, correo, telefono, id):
    """Metodo para modificar los datos del usuario."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE data_base_usuario 
        SET nombre = %s, correo = %s,  telefono = %s 
        WHERE id = %s
    """
    valores = (nombre, correo, telefono, id)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_usuario(id):
    """Metodo para eliminar el usaurio de la base de datos."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "DELETE FROM `data_base_usuario` WHERE id = %s"
    cursor.execute(sql, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
