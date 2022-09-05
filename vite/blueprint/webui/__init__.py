from flask import Blueprint
<<<<<<< HEAD
=======
from .view import index 
>>>>>>> 40d5a4dfbdb5a680953d97914c87a26445eb52d7

from .view import index

<<<<<<< HEAD
bp = Blueprint('webui', __name__, template_folder='templates')

bp.add_url_rule('/', view_func=index)
=======
bp = Blueprint("webui",__name__,template_folder="templates")
bp.add_url_rule("/", view_func=index)
>>>>>>> 40d5a4dfbdb5a680953d97914c87a26445eb52d7


def init_app(app):
    app.register_blueprint(bp)
