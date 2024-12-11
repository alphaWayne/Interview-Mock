from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from flask_login import current_user,UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = str(user_id)  # Flask-Login要求用户ID为字符串形式
        self.username = username
        self.email = email
        self.password = password

class temp_LoginForm(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password_hash = password
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.id
    def get_username(self):
        return self.username

class LoginForm(FlaskForm):
    username = StringField(u'学号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登陆')

class RegisterForm(FlaskForm):
    username = StringField(u'学号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    confirm_password = PasswordField(u'确认密码',validators=[DataRequired(), EqualTo('password')])
    captcha = StringField(u'邮箱验证码', validators=[DataRequired()])
    submit = SubmitField(u'注册')
