import mysql.connector


def crear_conexion():
    """Crear la conexion a la base de dato."""

    return mysql.connector.connect(
        host="localhost", user="root", password="", database="servicio_gestion"
    )
