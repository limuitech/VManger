from . import app, db
from flask import request, render_template, redirect, url_for, session, make_response
from views.Models import test




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

#查看项目列表
@app.route('/projectlist', methods=['get','post'])
def Projectlist():
    return render_template('project-list.html')

#新建项目
@app.route('/projectadd', methods=['get','post'])
def Projectadd():
    if request.method == 'GET':
        return render_template('project-add.html')
    else:
        s = ['添加成功']
        t = {}
        t['msg'] = s
        return json.dumps(t,ensure_ascii=False)
#资产列表
@app.route('/assetslist',methods=['get'])
def Assetslist():
    return render_template('assets-list.html')

#报告列表
@app.route('/presentationlist',methods=['get'])
def Presentationlist():
    return render_template('presentation-list.html')

#编写报告
@app.route('/presentationadd',methods=['get'])
def Presentationadd():
    return render_template('presentation-add.html')

#模板管理
@app.route('/templatemanagement',methods=['get'])
def Templatemanagement():
    return render_template('template-management.html')

#添加漏洞
@app.route('/vulnerabilityadd',methods=['get','post'])
def Vulnerabilityadd():
    return render_template('vulnerability-add.html')


@app.route('/test',methods=['get','post'])
def Test():
    db.create_all()
    tests=test(222,'test1')
    db.session.add(tests)
    db.session.commit()

    #user = test.query.filter_by(name='test1').first()
    #print(user)
    return render_template('login.html')
