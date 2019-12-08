import os
from flask import Flask,render_template,redirect,request
from adminitrator.admin_views import admin_blueprint
from student.student_view import student_blueprint
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from models import db
## 自定义装换器类
from werkzeug.routing import BaseConverter

BASEDIR = os.path.dirname(__file__)

staticfolder = os.path.join(BASEDIR,'static')
templatePage = os.path.join(BASEDIR,'templates')

app = Flask(__name__,static_folder=staticfolder,template_folder=templatePage)

class RegexConverter(BaseConverter):
    def __init__(self,regex,url_map):
        super(RegexConverter,self).__init__(url_map)
        self.regex = regex

app.url_map.converters['re'] = RegexConverter

db.init_app(app=app)

migrate = Migrate(app,db)

manage = Manager(app=app)

manage.add_command('db',MigrateCommand)


@app.route("/index.html",methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/getCurrentUser.html")
def getCurrentUser():
    return 'aaa'

@app.errorhandler(404)
def errorhandler404(err):
    return render_template('404handler.html',err=err)

@app.errorhandler(500)
def errorhandler500(err):
    return render_template('500handler.html',err=err)

app.config.from_pyfile("config.cfg")

app.register_blueprint(blueprint=student_blueprint,url_prefix='/student')
app.register_blueprint(blueprint=admin_blueprint,url_prefix='/admin')


if __name__ == '__main__':

    manage.run()



