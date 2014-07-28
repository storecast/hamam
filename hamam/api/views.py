from flask import request, Blueprint, current_app, jsonify, send_from_directory
from barrel_reaktor.document.models import Document
from holon import ReaktorAuthError, ReaktorArgumentError
from ..configs.default import DOCUMENT_PATH_PREFIX
from ..session import SessionStore


mod = Blueprint('api', __name__)


@mod.route('/document/<doc_id>/')
def document_view(doc_id):
    cookie_name = current_app.config['SESSION_COOKIE_NAME']
    session_id = request.cookies.get(cookie_name)
    session = SessionStore.load(session_id)
    token = session['reaktor_token']
    try:
        document = Document.get_by_id(token, doc_id)
        path = request.script_root + \
            '/api' + \
            DOCUMENT_PATH_PREFIX + \
            Document.get_doc_path(token, doc_id, document.is_user)
    except ReaktorAuthError: return jsonify(), 403
    except ReaktorArgumentError: return jsonify(), 404
    return jsonify(extracted_epub_path=path), 200, {
        # Allow loading contents from https to http and vice versa.
        'Access-Control-Allow-Origin': ' '.join(
            [p + request.host for p in ['http://', 'https://']])
    }


@mod.route(DOCUMENT_PATH_PREFIX + '/<path:path>')
def serve_document_asset(path):
    return send_from_directory('/', path)
