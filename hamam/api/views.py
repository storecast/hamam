from barrel_reaktor.document.models import Document
from flask import request, Blueprint, current_app, jsonify, send_from_directory
from holon import ReaktorAuthError, ReaktorArgumentError
from ..configs.default import DOCUMENT_PATH_PREFIX, DOCUMENT_ROOT
from ..session import SessionStore
import logging


mod = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@mod.route('/document/<doc_id>/')
def document_view(doc_id):
    cookie_name = current_app.config['SESSION_COOKIE_NAME']
    try:
        session_id = request.cookies[cookie_name]
    except KeyError:
        logger.warn("No cookies for %s" % cookie_name)
        return jsonify(), 403
    session = SessionStore(session_id).load()
    try:
        token = session['reaktor_token']
    except KeyError:
        logger.warn("No reaktor_token in %s" % repr(session))
        return jsonify(), 403
    try:
        document = Document.get_by_id(token, doc_id)
        document_file_path = Document.get_doc_path(token, doc_id,
                                                   document.is_user)
        path = request.script_root + \
            '/api' + \
            DOCUMENT_PATH_PREFIX + \
            document_file_path[len(DOCUMENT_ROOT)-1:]
    except ReaktorAuthError: return jsonify(), 403
    except ReaktorArgumentError: return jsonify(), 404
    return jsonify(extracted_epub_path=path), 200, {
        # Allow loading contents from https to http and vice versa.
        'Access-Control-Allow-Origin': ' '.join(
            [p + request.host for p in ['http://', 'https://']])
    }


@mod.route(DOCUMENT_PATH_PREFIX + '/<path:path>')
def serve_document_asset(path):
    f = send_from_directory(DOCUMENT_ROOT, path)
    if path.endswith('.html'):
        f.mimetype = 'application/xhtml+xml'
    return f
