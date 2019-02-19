from . import app, db,tmppath
from flask import request, render_template, redirect, url_for, session,make_response, jsonify
from views.Models import Project,People,Ip,Domain,Plugin
import json
import string
import re
from tld import get_tld
from IPy import IP
import time
import uuid
import datetime
import random
from werkzeug.utils import secure_filename
from docxtpl import DocxTemplate

db.create_all()


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
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Project).order_by(Project.id.desc()).paginate(
    page, per_page=10, error_out=False)
    project = pagination.items
    return render_template('project-list.html',project=project,pagination=pagination)

#查看资产情况
@app.route('/getassets/<int:pid>',methods=['get'])
def Getassets(pid):
    project = db.session.query(Project).filter(Project.id == pid).one()

    return render_template('getassets.html',project=project)

#新建项目
@app.route('/projectadd', methods=['get','post'])
def Projectadd():
    if request.method == 'GET':
        peoples = db.session.query(People).filter(People.state == 1).all()
        return render_template('project-add.html',peoples=peoples)
    else:

        projectName = request.form.get('projectname')
        ips = request.form.get('ips')
        domains = request.form.get('domains')
        projectNumber = request.form.get('projectnumber')
        peoples = request.form.getlist('peoples[]')


        domains = domains.split(',')
        domainbad=[]
        for domain in domains:
            try:
                domainbad.append(get_tld(domain))
            except Exception as e:
                pass

        ips = ips.split(',')
        if projectNumber == '':
            projectNumber = '合同签订中'

        project = Project(projectname=projectName, projectnumber=projectNumber, state=1)
        for id in peoples:
            people = db.session.query(People).filter(People.id == id and People.state == 1).one()
            project.peoples.append(people)
        iplistbad = []
        ipcode = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        for ip in ips:
            if ip.rfind('-')!=-1 or ip.rfind('/')!=-1:
                for ipl in IP(IP(ip, make_net=True)):
                   iplistbad.append(str(ipl))
            elif ipcode.match(ip):
                iplistbad.append(ip)
        for i in list(set(iplistbad)):
            project.ips.append(Ip(ip=i,type=1))
        for i in list(set(domainbad)):
            project.domains.append(Domain(domain=i,type=i.count('.')))
        db.session.add(project)
        db.session.commit()
        t={}
        t['success'] = True
        return json.dumps(t,ensure_ascii=False)


#项目编辑
@app.route('/projectedit/<int:pid>', methods=['get','post'])
def Projectedit(pid):

    project = db.session.query(Project).filter(Project.id == pid).one()
    if request.method == 'GET':
        peoples = db.session.query(People).filter(People.state == 1).all()
        return render_template('project-edit.html', project=project,peoples=peoples)
    else:

        projectName = request.form.get('projectname')
        ips = request.form.get('ips')
        domains = request.form.get('domains')
        projectNumber = request.form.get('projectnumber')
        peoples = request.form.getlist('peoples[]')

        domains = domains.split(',')
        domainbad = []
        for domain in domains:
            try:
                domainbad.append(get_tld(domain))
            except Exception as e:
                pass
        ips = ips.split(',')
        if projectNumber == '':
            projectNumber = '合同签订中'


        project = Project(projectname=projectName, projectnumber=projectNumber, state=1)
        project.id=pid
        for id in peoples:
            people = db.session.query(People).filter(People.id == id and People.state == 1).one()
            project.peoples.append(people)
        iplistbad = []
        ipcode = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        for ip in ips:
            if ip.rfind('-') != -1 or ip.rfind('/') != -1:
                for ipl in IP(IP(ip, make_net=True)):
                    iplistbad.append(str(ipl))
            elif ipcode.match(ip):
                iplistbad.append(ip)
        for i in list(set(iplistbad)):
            project.ips.append(Ip(ip=i, type=1))
        for i in list(set(domainbad)):
            project.domains.append(Domain(domain=i,type=i.count('.')))
        db.session.merge(project)
        db.session.commit()
        t = {}
        t['success'] = True
        return json.dumps(t, ensure_ascii=False)


#漏洞扫描插件
@app.route('/pluginlist',methods=['get'])
def Pluginlist():
    page = request.args.get('page', 1, type=int)
    plugins = db.session.query(Plugin).order_by(Plugin.id.desc()).paginate(
        page, per_page=10,
        error_out=False
    )

    return render_template('plugin-list.html', plugins=plugins)

@app.route('/pluginadd-json',methods=['get','post'])
def Pluginadd_json():
    if request.method == 'GET':
        return render_template('plugin-add-json.html')

@app.route('/pluginadd-script',methods=['get','post'])
def Pluginadd_script():
    if request.method == 'GET':
        return render_template('plugin-add-script.html')

'''
#报告列表
@app.route('/presentationlist',methods=['get'])
def Presentationlist():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Project).order_by(Project.id.desc()).paginate(
        page, per_page=10,
        error_out=False
    )

    project = pagination.items

    return render_template('presentation-list.html', project=project, pagination=pagination)


#编写报告
@app.route('/presentationadd/<int:pid>', methods=['get', 'post'])
def Presentationadd(pid):

        project = db.session.query(Project).filter(Project.id == pid).one()
        targets = db.session.query(Target).outerjoin(Project, Target.pid == Project.id).filter(Project.id == pid)
        vulnerabilityClass = db.session.query(VulnerabilityClass).order_by(VulnerabilityClass.id.desc()).all()
        return render_template('presentation-add.html',project=project,targets=targets,vulnerabilityClass=vulnerabilityClass)


#模板管理
@app.route('/templatemanagement',methods=['get'])
def Templatemanagement():
    return render_template('template-management.html')


#添加漏洞
@app.route('/vulnerabilityadd/<int:pid>/<int:vclassid>/<int:tid>',methods=['get','post'])
def Vulnerabilityadd(vclassid, tid, pid):
    if request.method == 'GET':
        db.create_all()
        #V_list = db.session.query(Vulnerability).filter(Vulnerability.type == vclassid).all()
        VC_list = db.session.query(VulnerabilityClass).order_by(VulnerabilityClass.id.desc()).all()
        vclass = db.session.query(VulnerabilityClass).filter(VulnerabilityClass.id == vclassid).order_by(VulnerabilityClass.id.desc()).one()
        return render_template('vulnerability-add.html',VC_list=VC_list,vclass=vclass, tid=tid, pid=pid)
    else:

        vultype = request.form.get('vultype')
        vulname = request.form.get('vulname')
        rank = request.form.get('rank')
        info = request.form.get('info')
        sugess = request.form.get('sugess')
        tagvul = Tagvul(vultype=vultype, vulname=vulname, rank=rank, info=info, sugess=sugess, tagid=tid, pid=pid)
        db.session.add(tagvul)
        db.session.commit()
        t = {}
        t['success'] = True
        return json.dumps(t, ensure_ascii=False)


#导出报告
@app.route('/exportword/<int:pid>',methods=['get'])
def ExportWord(pid):
    project = db.session.query(Project).filter(Project.id == pid).one()

    for i in project.targetList:

        pass
    peopless = project.implementerPerson.split(',')
    peoples = []

    for people in peopless:
        tmp = {'name':people.split(":")[0],
               'phone':people.split(":")[1]}
        peoples.append(tmp)
    targets = project.targetList
    for i in targets:
        for j in i.tagvul:
            print(j.info)
    #auth = peoples[0].split(':')[0]
    vulnum = db.session.query(Tagvul).filter(Tagvul.pid == pid).count()
    high = db.session.query(Tagvul).filter(Tagvul.pid == pid).filter( Tagvul.rank == "高").count()
    secondary = db.session.query(Tagvul).filter(Tagvul.pid == pid ).filter(  Tagvul.rank == "中").count()
    low = db.session.query(Tagvul).filter(Tagvul.pid == pid ).filter(  Tagvul.rank == "低").count()





    doc = DocxTemplate(tmppath+"Penetration_test_report_template.docx")
    context = {'title': project.projectName,
               'onetime': project.startTime.strftime('%Y')+'年'+project.startTime.strftime('%m')+'月',
               'twetime': project.startTime.strftime('%Y-%m-%d'),
               'auth': peoples[0]['name'],
               'peoples': peoples,
               'targets': targets,
               'tongji':"本次渗透测试共测试"+str(len(targets))+"个系统，发现"+str(vulnum)+"个漏洞，其中包括"+str(high)+"个高危漏洞、"+str(secondary)+"个中危漏洞和"+str(low)+"个低危漏洞",
               }
    doc.render(context)
    doc.save(tmppath+"tmp/"+"generated_doc.docx")


    t = {}
    t['success'] = True
    return json.dumps(t, ensure_ascii=False)


















#文件上传
@app.route('/imgupload',methods=['post'])
def imgupload():
    UPLOAD_FOLDER = 'static\\upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    basedir = os.path.abspath(os.path.dirname(__file__))
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['upload_file']
    if f and ('.' in f.filename and f.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
        fname = secure_filename(f.filename)

        ext = fname.rsplit('.', 1)[1]
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100

        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)


        new_filename = str(uuid.uuid1()) + '.' + ext
        file_dir = file_dir+"\\"+uniqueNum
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        path = os.path.join(file_dir, new_filename)
        file_path = "/"+UPLOAD_FOLDER +uniqueNum+new_filename
        print(path)
        f.save(path)

        return jsonify({"success": 0, "msg": "上传成功", "file_path":file_path})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})







'''
#资产列表
@app.route('/assetslist',methods=['get'])
def Assetslist():

    return render_template('assets-list.html')

#时间格式调整
@app.template_filter('timetmp')  #括号里面是自己给过滤器起的名字
def timetmp(time):
    return time.strftime('%Y-%m-%d ')
