from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['UPLOAD_FOLDER'] = 'app/static/images/upload'


db = SQLAlchemy(app)
ckeditor = CKEditor(app)


from . import views
from . import admin