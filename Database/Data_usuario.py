from .database import crear_conexion

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