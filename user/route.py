from flask import Blueprint

mod = Blueprint('user', __name__)

@mod.route('/user')
def user():
    return render_template('user.html')