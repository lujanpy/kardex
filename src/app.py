from flask import Flask
from config import config
from routes import usuarios_routes, productos_routers, kardex_routes
app = Flask(__name__)


def pagina_no_encontrada(error):
    return "<h1>pagina_no_encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['develoment'])
    # blueprints
    app.register_blueprint(usuarios_routes.main, url_prefix='/api/user')
    app.register_blueprint(productos_routers.main, url_prefix='/api/products')
    app.register_blueprint(kardex_routes.main, url_prefix='/api/kardex')
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
