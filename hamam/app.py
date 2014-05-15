from flask import Flask
from session.models import db
from session.views import mod as session_blueprint


app = Flask(__name__)
app.config.from_object('configs.default')
app.config.from_envvar('HAMAM_SETTINGS', silent=True)

db.init_app(app)
app.register_blueprint(session_blueprint, url_prefix='/session')


if __name__ == '__main__':
    app.run()
