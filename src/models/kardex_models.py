# nos permite hacer la conexion  a la bd desde otro archivo
from database.db import get_connection
from .entities.kardex import Kardex
from flask import request


class Kardex_model():

    @classmethod
    def get_carrito(self): # este metodo nos permite ver los productos agregados a el carrito
        try:
            connection = get_connection()  # obtenemos la conexion a la base de datos

            carritos = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT codigo, nombre, descripcion,precio,cantidad FROM carrito")
                resultset = cursor.fetchall()  # para obtener todos los resultados

                for row in resultset:
                    carrito = Kardex(row[0], row[1], row[2], row[3], row[4])
                    carritos.append(carrito.to_json())

            connection.close()  # para cerrar la conexion
            return carritos
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def vista_carrito(self): # ver  las cantidades disponibles
        try:
            connection = get_connection()  

            with connection.cursor() as cursor:
                cursor.execute(""" SELECT p.codigo, p.stock, ca.cantidad,
                                            CASE
                                                WHEN p.stock = 0 THEN 'Stock en 0'
                                                WHEN p.stock - ca.cantidad < 0 THEN 'Stock insuficiente'
                                                ELSE 'Stock suficiente'
                                            END AS estado
                                        FROM productos p
                                        JOIN carrito ca ON p.codigo = ca.codigo;"""
                               )
                connection.commit()
                resultados = cursor.fetchall()
                productos = []
                for row in resultados:
                    producto = {
                        "codigo": row[0],
                        "stock": row[1],
                        "cantidad": row[2],
                        "estado": row[3]
                    }
                    productos.append(producto)
            connection.close()  
            cursor.close()

            return productos

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def post_carrito(self): # metodo para ingresar los productos a el carrito
        try:
            connection = get_connection()  

            with connection.cursor() as cursor:
                cursor.execute(""" INSERT INTO carrito (codigo, nombre, descripcion,precio,cantidad)
                                    SELECT codigo, nombre, descripcion,precio,stock
                                    FROM productos
                                    WHERE codigo = %s;""",(request.json['id'])
                               )
                connection.commit()

                cursor.execute(""" UPDATE carrito  SET  cantidad= %s
                                   WHERE codigo = %s;""",(request.json['cantidad'], request.json['id'])
                               )
                connection.commit()

            connection.close()  
            cursor.close()

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def put_carrito(self): # metodo para ingresar los productos a el carrito
        try:
            connection = get_connection()  

            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE productos p
                                            JOIN carrito ca ON p.codigo = ca.codigo
                                            SET 
                                                p.stock = CASE
                                                    WHEN p.stock - ca.cantidad >= 0 THEN p.stock - ca.cantidad  -- Si hay suficiente stock, se resta
                                                    ELSE p.stock  -- Si no hay suficiente stock, no se cambia el valor de stock
                                                END;"""
                               )
                connection.commit()

                connection.close()  
                cursor.close()

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def del_carrito(self, codigo):# metodo para borrar productos del carrito
        try:
            connection = get_connection()  
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM carrito WHERE codigo = %s;",(codigo))
                connection.commit()
            connection.close()  
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def delete_carrito(self):# metodo para limpiar la tabla del carrito
        try:
            connection = get_connection()  
            with connection.cursor() as cursor:
                cursor.execute(
                    "TRUNCATE TABLE carrito;")
                connection.commit()
            connection.close()  
        except Exception as ex:
            print(ex)
            raise Exception(ex)
