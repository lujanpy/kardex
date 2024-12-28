from flask import Blueprint, jsonify

# importamos los modelos
from models.kardex_models import Kardex_model

main = Blueprint('kardex_blueprint', __name__)


@main.route('/carrito', methods=['GET']) #ver los productos agregados a el carrito
def get_carrito():
    try:
        producto = Kardex_model.get_carrito()
        return jsonify(producto)
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": str(ex)}), 500


@main.route('/verificar', methods=['GET']) # ver que productos tiene stock suficiente 
def vista_carrito():
    try:
        producto = Kardex_model.vista_carrito()
        return jsonify(producto)
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": str(ex)}), 500


@main.route('/registro', methods=['POST']) # ingresar los productos a el carrito
def post_carritos():
    try:
        Kardex_model.post_carrito()
        return jsonify({"mensaje": "productos ingresados a el carrito"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": str(ex)}), 500


@main.route('/ventas', methods=['PUT']) # aceptar y comprar los productos 
def put_carrito():
    try:
        Kardex_model.put_carrito()
        return jsonify({"mensaje": "productos comprados"},)
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": str(ex)}), 500


@main.route('/delete/<codigo>', methods=['DELETE']) # borrar un elemento del carrito
def del_carritos(codigo):
    try:
        Kardex_model.del_carrito(codigo)
        return jsonify({'mensaje': "producto borrado."})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@main.route('/borrar/todo', methods=['DELETE']) # limpiar la tabla carrito
def delet_carritos():
    try:
        Kardex_model.delete_carrito()
        return jsonify({'mensaje': "tabla borrado."})
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({"mensaje": "Error interno del servidor"}), 500
