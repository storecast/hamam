from flask import Flask, g
from session.db.models import db
from session.views import mod as session_blueprint
from api.views import mod as api_blueprint


app = Flask(__name__)
app.config.from_object('configs.default')
app.config.from_envvar('HAMAM_SETTINGS', silent=True)

db.init_app(app)
app.register_blueprint(session_blueprint, url_prefix='/session')
app.register_blueprint(api_blueprint, url_prefix='/api')


@app.teardown_appcontext
def close_store(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, '_session_store') and hasattr(g._session_store, 'close'):
        g._session_store.close()


if __name__ == '__main__':
    app.run()
