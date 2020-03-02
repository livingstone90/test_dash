"""
Contain main imports and the app instance.
Register the blueprints
"""
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']='7daf12b8731868c589b15b625907dd7b'

from webdash.Neosum.routes import Neosum

app.register_blueprint(Neosum, url_prefix='/templates')