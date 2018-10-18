from flask import Blueprint

mod = Blueprint('admin', __name__)

@mod.route('/admin')
def admin():
    return 'hello'