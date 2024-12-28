# nos permite hacer la conexion  a la bd desde otro archivo
from database.db import get_connection
from .entities.producto import Producto
from flask import request


class Producto_model():

    @classmethod
    def get_producto(self): # metodo para ver los productos 
        try:
            connection = get_connection()  # obtenemos la conexion a la base de datos

            productos = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT codigo, nombre, descripcion,precio,stock FROM productos")
                resultset = cursor.fetchall()  # para obtener todos los resultados

                for row in resultset:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4])
                    productos.append(producto.to_json())

            connection.close()  # para cerrar la conexion
            return productos

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_one_product(self, codigo):# metodo para ver un solo producto
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT codigo, nombre, descripcion,precio,stock FROM productos WHERE codigo = %s",(codigo))
                resultset = cursor.fetchone()

                if resultset != None:
                    producto = {
                        "codigo": resultset[0],
                        "nombre": resultset[1],
                        "descripcion": resultset[2],
                        "precio": resultset[3],
                        "stock": resultset[4]
                    }
                    return producto
                else:
                    return None

            connection.close()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def post_producto(self): # metodo para ingresar los productos

        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM productos WHERE codigo = %s;", (request.json['codigo']))
                resultado = cursor.fetchone()
                if resultado[0] > 0:# verificamos si el id del producto ya existe
                    return True
                else:
                    cursor.execute(
                        """INSERT INTO productos (codigo, nombre, descripcion,precio,stock)
                            VALUES (%s,%s,%s,%s,%s);""", (request.json['codigo'],
                                                          request.json['nombre'],
                                                          request.json['descripcion'],
                                                          request.json['precio'],
                                                          request.json['stock'])
                    )
                    connection.commit()

            connection.close()
            cursor.close()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_producto(self, idu):# metodo para actualizar productos
        try:
            connection = get_connection()
            print(request.json)
            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE productos  SET  precio = %s, stock = stock + %s
                                   WHERE codigo = %s;""",(
                    request.json['precio'],
                    request.json['stock'],
                    idu)
                )
                connection.commit()

            connection.close()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def del_producto(self, idp):# metodo para borrar los productos
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM productos WHERE codigo = %s;", (idp))
                connection.commit()
            connection.close()
        except Exception as ex:
            print(ex)
            raise Exception(ex)
