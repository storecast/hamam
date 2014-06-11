from flask import Blueprint, request, jsonify, current_app
from . import SessionStore


mod = Blueprint('session', __name__)


@mod.route('/')
def session():
    cookie_name = current_app.config['SESSION_COOKIE_NAME']
    session_id = request.cookies.get(cookie_name)
    if not session_id:
        return jsonify()
    session = SessionStore(session_id).load()
    return jsonify(session)
