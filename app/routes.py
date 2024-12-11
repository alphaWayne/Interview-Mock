import random, string,datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user,login_required, current_user
from app.utils import *
from app.database import *
from extentions.emailSend import send_captche_email
from app.LoginForm import *
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'p@ssw0rd'

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    conn, cursor = create_dict_cursor('userDatabase')
    cursor.execute('SELECT * FROM users WHERE _id = ?', (user_id,))
    user_row=dict(cursor.fetchone())
    conn.close()
    if user_row:
        return User(
            user_id=user_row['_id'],
            username=user_row['username'],
            email=user_row['email'],
            password=user_row['password_hash']
        )
    return None

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('base_box.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn, cursor = create_dict_cursor('userDatabase')
        cursor.execute('SELECT * FROM users WHERE username = ?', (form.username.data,))
        user=dict(cursor.fetchone())
        conn.close()
        print(user)
        if user:
            if check_password_hash(user['password_hash'], form.password.data):
                # 临时用户
                temp_user = temp_LoginForm(id=user['_id'], username=user['username'], email=user['email'],
                                           password=user['password_hash'])
                login_user(temp_user)
                return redirect(url_for('index'))
        flash('登陆失败, 请检查你的账号或密码')
    return render_template('login.html', form=form)

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('validate_on_submit')
        username = form.username.data
        hashed_password = generate_password_hash(form.password.data)
        captcha = form.captcha.data
        receiver = username + '@uibe.edu.cn'
        # 检查验证码是否有效
        if check_captcha_expiration(receiver, 'register') and check_captcha(receiver, captcha, 'register'):
            # 验证码有效，检查用户是否已存在
            conn, cursor = create_connection('userDatabase')
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                flash('该学号已被注册', 'danger')
            else:
                # 注册新用户
                register_user(username, hashed_password, receiver)
                flash('注册成功', 'success')
                return redirect(url_for('login'))
        else:
            flash('验证码错误或已过期', 'danger')
    return render_template('register.html',form=form)

# 退出
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/getCaptche", methods=['POST', 'GET'])
def get_captche():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return jsonify({'status': 'error', 'message': '用户名不能为空'}), 400
        receiver = f"{username}@uibe.edu.cn"
        # 检查是否有未过期的验证码
        if check_captcha_expiration(receiver, 'register'):
            return jsonify({'status': 'success', 'message': '有未过期验证码'})
        # 生成新的6位数字验证码
        captcha_code = ''.join(random.choices(string.digits, k=6))
        # 发送验证码到用户的邮箱
        send_captche_email(receiver, captcha_code)
        # 插入或更新验证码记录
        insert_or_update_captcha(receiver, 'register', captcha_code, datetime.datetime.now())
        return jsonify({'status': 'success', 'message': '验证码已发送'})
    return jsonify({'status': 'error', 'message': '请求方法不支持'}), 405