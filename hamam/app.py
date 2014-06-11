from flask import Flask
from session.models import db
from session.views import mod as session_blueprint
from api.views import mod as api_blueprint


app = Flask(__name__)
# relative imports are not supported
app.config.from_object('hamam.configs.default')
app.config.from_envvar('HAMAM_SETTINGS', silent=True)

db.init_app(app)
app.register_blueprint(session_blueprint, url_prefix='/session')
app.register_blueprint(api_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run()
