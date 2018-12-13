from . import app
from flask import request, render_template, redirect, url_for, session, make_response
import Models

@app.route('/')
def Index():
    return render_template('index.html')


#登录 用户名和密码从config 内匹配
@app.route('/login', methods=['get', 'post'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == app.config.get('USERNAME') and password == app.config.get('PASSWORD'):
            session['login'] = True
            return redirect(url_for('Index'))
        else:
            return redirect(url_for('Login', message='登录失败'))
