from flask import Flask, request, jsonify
from session.models import db
from session.session_stores import DbSessionStore


app = Flask(__name__)
app.config.from_object('configs.default')
app.config.from_envvar('HAMAM_SETTINGS', silent=True)

db.init_app(app)


@app.route('/session/')
def session():
    cookie_name = app.config['SESSION_COOKIE_NAME']
    session_id = request.cookies.get(cookie_name)
    if not session_id:
        return jsonify()
    session_store = DbSessionStore(db, session_id)
    session = session_store.load()
    return jsonify(session)


if __name__ == '__main__':
    app.run()
