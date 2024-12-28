from flask import Blueprint, jsonify

# importamos los modelos
from models.usuario_models import Usuario_model

main = Blueprint('user_blueprint', __name__)


@main.route('/', methods=['GET']) # para ver usuarios
def get_usuarios():
    try:
        usuario = Usuario_model.get_usuario()
        return jsonify(usuario)
    except Exception:
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/<idd>', methods=['GET']) #para ver un solo usuario
def get_usuario(idd): 
    try:
        usuario = Usuario_model.get_one_user(idd)
        return jsonify(usuario)
    except Exception as ex:
        print(f"Error al obtener el usuario con código {idd}: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/registro', methods=['POST']) # para ingresar usuarios
def POST_usuario():
    try:
        Usuario_model.post_user()
        return jsonify({'mensaje': "usuario registrado."})
    except Exception as ex:
        print(f"Error al ingresar el usuario con código : {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/update/<idus>', methods=['PUT']) # para actualizar usuarios
def put_usuario(idus):
    try:
        Usuario_model.update_usuario(idus)
        return jsonify({"mensaje": "usuario_actualizado"})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/delete/<idg>', methods=['DELETE']) # para borrar usuarios
def del_usuario(idg):
    try:
        Usuario_model.del_user(idg)
        return jsonify({'mensaje': "usuario borrado."})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500
