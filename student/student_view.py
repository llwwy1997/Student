from flask import Blueprint

student_blueprint = Blueprint('student',__name__)

@student_blueprint.route('/index.html',methods=['GET'])
def index():
    return "This student route!"