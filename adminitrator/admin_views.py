from flask import Blueprint,render_template
from flask import redirect,session
from flask import request
from flask import url_for
from flask import jsonify
from utils.functions import is_login
from models import Admin,Grade,Student,Subject,Teacher,db

admin_blueprint = Blueprint('admin',__name__)

@admin_blueprint.route('/login.html',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('adminitrator/admin_login.html',msg='')
    else:
        admin_name = request.form.get("admin_name")
        admin_passwd = request.form.get("admin_passwd")
        session['admin_name'] = admin_name
        session['authority'] = 2
        login_admin = Admin.query.filter_by(a_name=admin_name, a_passwd=admin_passwd).first()
        if login_admin:
            return redirect(url_for('admin.index'))
        else:
            return render_template('adminitrator/admin_login.html',msg='验证失败，请重试！')

@admin_blueprint.route('loginOut.html',methods=['GET'])
def loginOut():
    session.clear()
    return redirect(url_for('admin.login'))


@is_login
@admin_blueprint.route('/index.html',methods=['GET'])
def index():
    name = session.get('admin_name')
    return render_template('adminitrator/index.html',name=name)

'''
    班级管理
'''
@is_login
@admin_blueprint.route('/gradeManger.html',methods=['GET'])
def gradeManger():
    page = int(request.args.get('page', 1))
    page_num = int(request.args.get('page_num', 5))
    paginate = Grade.query.order_by('g_id').paginate(page, page_num)
    grades = paginate.items
    return render_template('adminitrator/gradePage.html',grades=grades,paginate=paginate)



@is_login
@admin_blueprint.route('/getGradeById.html',methods=['GET'])
def getGradeById():
    id = int(request.args.get('id'))
    grade = Grade.query.filter_by(g_id =id).first()
    return render_template('adminitrator/gradeEditPage.html',grade=grade)


@is_login
@admin_blueprint.route('/delGradeById.html',methods=['POST'])
def delGradeById():
    if request.method == 'POST':
        id = int(request.form.get('id'))
        grade = Grade.query.filter_by(g_id =id).first()
        try:
            Grade.remove(grade)
            db.session.commit()
            msg = '删除成功!'
        except:
            msg = '删除失败!'
        return msg


    else:
        redirect(url_for('admin.gradeManger'))

@is_login
@admin_blueprint.route('/editGrade.html',methods=['POST'])
def editGrade():
    id = int(request.args.get('id'))


'''
    学生管理
'''

@is_login
@admin_blueprint.route('/studentMenage.html',methods=['GET'])
def studentMenage():
    page = int(request.args.get('page', 1))
    page_num = int(request.args.get('page_num', 5))
    paginate = Student.query.order_by('s_id').paginate(page, page_num)
    students = paginate.items
    return render_template('adminitrator/studentPage.html', students=students, paginate=paginate)


'''
    教师管理
'''
@is_login
@admin_blueprint.route('/teacherMenage.html',methods=['GET'])
def teacherMenage():
    page = int(request.args.get('page', 1))
    page_num = int(request.args.get('page_num', 5))
    paginate = Teacher.query.order_by('t_id').paginate(page, page_num)
    teachers = paginate.items
    return render_template('adminitrator/teacherPage.html', teachers=teachers, paginate=paginate)