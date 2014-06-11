from flask import Blueprint, current_app


mod = Blueprint('api', __name__)


@mod.route('/document/<doc_id>')
def document_view(doc_id):
    pass
