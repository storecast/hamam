from flask import request, Blueprint, current_app, jsonify, abort
from barrel_reaktor.document.models import Document
from holon import ReaktorAuthError, ReaktorArgumentError
from ..session import SessionStore


mod = Blueprint('api', __name__)


@mod.route('/document/<doc_id>')
def document_view(doc_id):
    cookie_name = current_app.config['SESSION_COOKIE_NAME']
    session_id = request.cookies.get(cookie_name)
    session = SessionStore(session_id).load()
    token = session['reaktor_token']
    try:
        document = Document.get_by_id(token, doc_id)
        path = Document.get_doc_path(token, doc_id, document.is_user)
    except ReaktorAuthError: abort(403)
    except ReaktorArgumentError: abort(404)
    return jsonify(extracted_epub_path=path)
