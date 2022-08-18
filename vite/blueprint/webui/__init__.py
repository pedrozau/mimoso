from flask import Blueprint
from vite.blueprint.webui.view import auth 
from .view import index 


bp = Blueprint("webui",__name__,template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/auth",view_func=auth)

def init_app(app):
    app.register_blueprint(bp)
    
