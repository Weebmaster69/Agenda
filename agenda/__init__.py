from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='KEY',
        DATABASE_HOST='localhost',
        DATABASE_USER='root',
        DATABASE_PASSWORD='deathassasin1',
        DATABASE='agenda',
    )

    from . import midb

    midb.init_app(app)

    from . import auth
    from . import contact


    app.register_blueprint(auth.bp)
    app.register_blueprint(contact.bp)

    @app.route("/hola")
    def hola():
        return 'hola mundo'
    return app