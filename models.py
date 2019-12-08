from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

##系统管理员
class Admin(db.Model):
    ##管理员id
    a_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    ##管理员姓名
    a_name = db.Column(db.String(20),unique=True,nullable=False)
    ##管理员密码
    a_passwd = db.Column(db.String(50),nullable=False)

    __tablename__ = 'admin'

    def __init__(self,a_name,a_passwd):
        self.a_name = a_name
        self.a_passwd = a_passwd

    def save(self):
        db.session.add(self)
        db.session.commit()


##班级
class Grade(db.Model):
    ##班级id
    g_id = db.Column(db.Integer,autoincrement=True,primary_key=True)

    ##班级名
    g_name = db.Column(db.String(20),unique=True)

    ##班级创建时间
    g_create_time = db.Column(db.DATETIME,default=datetime.now())

    ##建立一对多的关系
    students = db.relationship('Student',backref='grade')

    ##班主任
    g_mainteacher = db.Column(db.Integer,db.ForeignKey('teacher.t_id'))

    ##老师
    teachers = db.relationship('Teacher', backref='grade')

    ##自定义表名
    __tablename__ = 'grade'

    def __init__(self,g_name,g_mainteacher):
        self.g_name = g_name
        self.g_mainteacher = g_mainteacher

    # def __repr__(self):
    #     return self.__dict__()
    def keys(self):
        return ('g_id','g_name','g_mainteacher','g_create_time','students','teachers')

    def __getitem__(self, item):
        return getattr(self, item)

    def save(self):
        db.session.add(self)
        db.session.commit()

##学生
class Student(db.Model):
    ##学生id
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    ##学生名
    s_name = db.Column(db.String(20))

    ##学生密码
    s_pwd = db.Column(db.String(50))

    ##学生照片
    s_pic = db.Column(db.String(50))

    ##学生性别
    s_sex = db.Column(db.Integer)

    ##学生年纪
    s_age = db.Column(db.Integer)

    ##学生出生年月
    s_birthday = db.Column(db.Date)

    ##学生父亲
    s_father = db.Column(db.String(10))

    ##学生母亲
    s_mother = db.Column(db.String(10))

    ##学生父亲电话
    s_fatherphone = db.Column(db.String(20))

    ##学生母亲电话
    s_motherphone = db.Column(db.String(20))

    ##家庭住址
    s_addr = db.Column(db.String(80))

    ##关联班级
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.g_id'))

    ##自定义表名
    __tablename__ = 'student'

    def __init__(self,s_name,s_pwd,s_pic,s_sex,s_age,s_birthday,s_father,s_mother,s_fatherphone,s_motherphone,s_addr,grade_id):
        self.s_name = s_name
        self.s_pwd = s_pwd
        self.s_pic = s_pic
        self.s_sex = s_sex
        self.s_age = s_age
        self.s_birthday = s_birthday
        self.s_father = s_father
        self.s_mother = s_mother
        self.s_fatherphone = s_fatherphone
        self.s_motherphone = s_motherphone
        self.s_addr = s_addr
        self.grade_id = grade_id

    def keys(self):
        return ('s_id','s_name','s_pic','s_addr','s_father','s_fatherphone','s_mother','s_motherphone','s_birthday','s_age')

    def __getitem__(self, item):
        return getattr(self, item)

    def save(self):
        db.session.add(self)
        db.session.commit()


##班级与老师一对多
grade_teacher=db.Table('grade_teacher',db.Column('g_id',db.Integer,db.ForeignKey('grade.g_id'),primary_key=True),db.Column('t_id',db.Integer,db.ForeignKey('teacher.t_id'),primary_key=True))


##教师
class Teacher(db.Model):
    ##教师id
    t_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    ##教师名
    t_name = db.Column(db.String(20))

    ##教师密码
    t_pwd = db.Column(db.String(50))

    ##老师照片
    t_pic = db.Column(db.String(50))

    ##教师性别
    t_sex = db.Column(db.Integer)

    ##所教学科
    t_subject = db.Column(db.Integer,db.ForeignKey('subject.sub_id'))

    ##毕业院校
    t_university = db.Column(db.String(50))

    ##主管班级
    mgrade = db.relationship('Grade', backref='mainteacher')

    ##教学班级
    grades = db.relationship('Grade', secondary=grade_teacher, backref=db.backref('teacher', lazy=True))

    __tablename__ = 'teacher'

    def __init__(self,t_name,t_pwd,t_pic,t_sex,t_subject,t_university):
        self.t_name = t_name
        self.t_pwd = t_pwd
        self.t_pic = t_pic
        self.t_sex = t_sex
        self.t_subject = t_subject
        self.t_university = t_university

    def keys(self):
        return ('t_id','t_name','t_sex','t_pic','t_university','t_subject','mgrade','grades')

    def __getitem__(self, item):
        return getattr(self, item)

    def save(self):
        db.session.add(self)
        db.session.commit()

##课程
class Subject(db.Model):
    ##课程id
    sub_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    ##课程名称
    sub_name = db.Column(db.String(20),nullable=False)

    def __init__(self,sub_name):
        self.sub_name = sub_name

    def save(self):
        db.session.add(self)
        db.session.commit()


