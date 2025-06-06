"""Conexion con la tabla de prestador de servicio."""

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


def agregar_prestador_servicio(correo, nombre, telefono, contraseña_servicio):
    """Agregar datos de un nuevo prestador de servicio."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO data_base_servicio 
        (correo, nombre, telefono, contraseña_servicio) 
        VALUES (%s, %s, %s, %s)
    """
    valores = (correo, nombre, telefono, contraseña_servicio)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


def Verificar_datos(usuario, contraseña):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    sql = """
        SELECT id, correo, nombre,  telefono, contraseña_servicio 
        FROM data_base_servicio 
        WHERE correo = %s
    """
    cursor.execute(sql, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        id, correo, nombre, telefono, hast_contraseña = resultado
        try:
            if bcrypt.checkpw(
                contraseña.encode("utf-8"), hast_contraseña.encode("utf-8")
            ):
                # Creamos el diccionario con los datos cifrados
                usuario_dict = {
                    "id": id,
                    "correo": correo,
                    "nombre": nombre,
                    "telefono": telefono,
                }
                # Desciframos los campos antes de retornarlos
                usuario_descifrado = descifrar_campos_usuario(
                    usuario_dict, ["nombre", "telefono"]
                )
                return usuario_descifrado
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return None


def obtener_prestador(id_prestador):
    """Obtener los datos del prestador de servicio por su ID."""

    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, correo, telefono, id FROM data_base_servicio WHERE id = %s",
        (id_prestador,),
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


def modificar_prestador(nombre, correo, telefono, id):
    """Modificar los datos del prestador de servicio."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE data_base_servicio 
        SET nombre = %s, correo = %s,  telefono = %s 
        WHERE id = %s
    """
    valores = (nombre, correo, telefono, id)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_prestador(id):
    """Eliminar la cuenta del prestador de servicio."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "DELETE FROM `data_base_servicio` WHERE id = %s"
    cursor.execute(sql, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
