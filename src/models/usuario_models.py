# nos permite hacer la conexion  a la bd desde otro archivo
from database.db import get_connection
from .entities.usuario import Usuario
from flask import request
from passlib.context import CryptContext

class Usuario_model():
    
    

    @classmethod
    def get_usuario(self): # metodo para ver usuarios
        try:
            connection = get_connection()  # obtenemos la conexion a la base de datos

            usuarios = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, password FROM user")
                resultset = cursor.fetchall()  # para obtener todos los resultados

                for row in resultset:
                    usuario = Usuario(row[0], row[1], row[2])
                    usuarios.append(usuario.to_json())

            connection.close()  # para cerrar la conexion
            return usuarios

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_one_user(self, idd): # metodo para ver un solo usuario
        try:
            connection = get_connection()  

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password FROM user WHERE id =%s",(idd))
                resultset = cursor.fetchone()  

                if resultset != None:
                    usuario = {
                        "id": resultset[0],
                        "usarname": resultset[1],
                        "password": resultset[2]
                    }
                    return usuario
                else:
                    return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def post_user(self): # metodo para ingresar usuarios
        
        # cifrar contraseña
        contexto = CryptContext(                     
            schemes=["bcrypt", "argon2"],
            default="bcrypt",  # Algoritmo por defecto
            bcrypt__rounds=12  # Configuración específica
        )
        try:
            con_crypt = contexto.hash(request.json['password'])
            
            connection = get_connection()  
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO user (id,username,password)
                        VALUES (%s,%s,%s);""",(request.json['id'],
                                                            request.json['username'], con_crypt,))
                connection.commit()

            connection.close()  
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_usuario(self, idus):# metodo para actualizar un usuario 
        try:
            contexto = CryptContext(
            schemes=["bcrypt", "argon2"],
            default="bcrypt",  # Algoritmo por defecto
            bcrypt__rounds=12  # Configuración específica
        )
            new_con_crypt = contexto.hash(request.json['password'])
            
            connection = get_connection()  
            
            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE user  SET username = %s, password = %s
                                   WHERE id = %s""",(request.json['username'],
                                                             new_con_crypt,
                                                             idus)
                               )
                connection.commit()

            connection.close() 
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def del_user(self, idg):# metodo para borrar usuarios
        try:
            connection = get_connection()  
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM user WHERE id=%s;",(idg))
                connection.commit()
            connection.close()  
        except Exception as ex:
            print(ex)
            raise Exception(ex)
