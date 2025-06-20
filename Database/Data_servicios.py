"""Crear conexion con la tabla de servicios."""

from cryptography.fernet import Fernet

from .database import crear_conexion


# Leer la clave de cifrado
def obtener_clave():
    with open("clave.key", "rb") as archivo_clave:
        clave = archivo_clave.read()
    return clave


clave = obtener_clave()
fernet = Fernet(clave)


# Función para agreagr un nuevo servicio a la base de datos
def agregar_servicio(
    razon_social,
    nit,
    tipo_servicio,
    administrador,
    id_prestador,
    descripcion,
    horario,
    puestos,
    ubicacion,
    imagen,
):
    """Agregar servicio a la base de datos."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO data_servicios 
        (razon_social, nit, tipo_servicio, administrador, id_prestador, 
        descripcion, horario, puestos, ubicacion, imagen) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        razon_social,
        nit,
        tipo_servicio,
        administrador,
        id_prestador,
        descripcion,
        horario,
        puestos,
        ubicacion,
        imagen,
    )
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


# Función para listar todos los servicios en la base de datos
def obtener_servicios_por_tipo(tipo_servicio):
    """Obtener los servicios por tipo de servicio."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        SELECT id_prestador, razon_social, administrador, tipo_servicio, 
        ubicacion, imagen, descripcion, horario, puestos, nit 
        FROM data_servicios WHERE tipo_servicio = %s
    """
    cursor.execute(sql, (tipo_servicio,))
    servicios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return [
        {
            "id_prestador": row[0],
            "razon_social": fernet.decrypt(row[1]).decode(),
            "administrador": fernet.decrypt(row[2]).decode(),
            "tipo_servicio": row[3],
            "ubicacion": fernet.decrypt(row[4]).decode(),
            "imagen": row[5],
            "descripcion": fernet.decrypt(row[6]).decode(),
            "horario": fernet.decrypt(row[7]).decode(),
            "puestos": fernet.decrypt(row[8]).decode(),
            "nit": fernet.decrypt(row[9]).decode(),
        }
        for row in servicios
    ]


def obtener_servicios(id_prestador):
    """Obtener los servicios por ID"""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        SELECT razon_social, administrador, tipo_servicio, ubicacion, 
        puestos, nit, horario,imagen,descripcion, id_prestador 
        FROM data_servicios WHERE id_prestador = %s
    """
    cursor.execute(sql, (id_prestador,))
    servicios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return [
        {
            "razon_social": fernet.decrypt(row[0]).decode(),
            "administrador": fernet.decrypt(row[1]).decode(),
            "tipo_servicio": row[2],
            "ubicacion": fernet.decrypt(row[3]).decode(),
            "puestos": fernet.decrypt(row[4]).decode(),
            "nit": fernet.decrypt(row[5]).decode(),
            "horario": fernet.decrypt(row[6]).decode(),
            "imagen": row[7],
            "descripcion": fernet.decrypt(row[8]).decode(),
            "id_prestador": row[9],
        }
        for row in servicios
    ]


def modificar_servicio(
    razon_social,
    nit,
    administrador,
    id_prestador,
    descripcion,
    horario,
    puestos,
    ubicacion,
    imagen,
):
    """Modificar los datos del servicio."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE data_servicios 
        SET razon_social = %s, nit = %s,  administrador = %s, 
            descripcion = %s, horario = %s, puestos = %s, ubicacion = %s, imagen = %s 
        WHERE id_prestador = %s
    """
    valores = (
        razon_social,
        nit,
        administrador,
        descripcion,
        horario,
        puestos,
        ubicacion,
        imagen,
        id_prestador,
    )
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_servicio(id_prestador):
    """Eliminar el servicio de la base de datos."""

    conexion = crear_conexion()
    cursor = conexion.cursor()
    sql = "DELETE FROM `data_servicios` WHERE id_prestador = %s"
    cursor.execute(sql, (id_prestador,))
    conexion.commit()
    cursor.close()
    conexion.close()


def reducir_puestos_servicio(id_prestador):
    conexion = crear_conexion()  # Asegúrate de usar tu base de datos real
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT puestos FROM data_servicios WHERE id_prestador = %s",
            (id_prestador,),
        )
        resultado = cursor.fetchone()

        if resultado:
            puestos_descifrados = int(fernet.decrypt(resultado[0]).decode())

            if puestos_descifrados > 0:
                nuevos_puestos = str(puestos_descifrados - 1).encode()
                puestos_cifrados = fernet.encrypt(nuevos_puestos)
                cursor.execute(
                    "UPDATE data_servicios SET puestos = %s WHERE id_prestador = %s",
                    (puestos_cifrados, id_prestador),
                )
                conexion.commit()
            else:
                raise Exception("No hay puestos disponibles.")
        else:
            raise Exception("Servicio no encontrado.")

    except Exception as e:
        print(f"Error al reducir puestos: {e}")
        raise

    finally:
        conexion.close()
