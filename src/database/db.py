from decouple import config

import pymysql
import traceback

# funcion para la conexion


def get_connection():
    try:
        # esto es lo que permite conectarnos a la base de datos
        return pymysql.connect(
            host=config('PGSQL_HOST'),
            user=config('PGSQL_USER'),
            password=config('PGSQL_PASSWORD'),
            db=config('PGSQL_DATABASE')
        )
    except Exception as ex:
        # Imprimir el error con más detalles para depurar
        print("Error al conectar a la base de datos:")
        traceback.print_exc()
        return None
