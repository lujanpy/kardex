from flask import Blueprint, jsonify

# importamos los modelos
from models.productos_models import Producto_model

main = Blueprint('producto_blueprint', __name__)


@main.route('/', methods=['GET'])# para ver los productos
def get_productos():
    try:
        producto = Producto_model.get_producto()
        return jsonify(producto)
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": str(ex)}), 500


@main.route('/<codigo>', methods=["GET"]) # para ver un solo producto
def get_one_producto(codigo):
    try:
        producto = Producto_model.get_one_product(codigo)
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({'mensaje': "producto no encontrado"}), 404

    except Exception as ex:
        print(f"Error al obtener el producto con código {codigo}: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/registro', methods=["POST"]) # para ingresar los productos
def post_producto():
    try:
        if Producto_model.post_producto():
            return jsonify({'mensaje': "el producto ya existe"})
        else:
            Producto_model.post_producto()
            return jsonify({'mensaje': "producto registrado"})

    except Exception as ex:
        print(f"Error al ingresar el usuario con código : {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/update/<idu>', methods=['PUT'])#para actualizar los productos
def put_producto(idu):
    try:
        Producto_model.update_producto(idu)
        return jsonify({"mensaje": "producto_actualizado"})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/delete/<idp>', methods=['DELETE']) # para borrar producto
def del_producto(idp):
    try:
        Producto_model.del_producto(idp)
        return jsonify({'mensaje': "producto borrado."})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500
