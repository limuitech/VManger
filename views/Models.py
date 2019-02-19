from . import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
#项目模型

project_people = db.Table('project_people',
                       db.Column('project_id',db.Integer,db.ForeignKey('project.id'),primary_key=True),
                       db.Column('people_id',db.Integer,db.ForeignKey('people.id'),primary_key=True)
                       )
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    projectname = db.Column(db.String(200))
    projectnumber = db.Column(db.String(100))
    starttime = db.Column(db.DateTime, default=datetime.datetime.now)
    stoptime = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    peoples = db.relationship('People',secondary=project_people,backref=db.backref('project'))
    domains = db.relationship('Domain',backref=db.backref('domains'), lazy="dynamic")
    ips = db.relationship('Ip', backref=db.backref('ips'), lazy="dynamic")

    def __init__(self, projectname,projectnumber, state):
        self.projectname = projectname
        self.projectnumber = projectnumber
        self.state = state

    def __repr__(self):
        return '<Project %r>' % self.projectName

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(5))
    phone = db.Column(db.String(11))
    state = db.Column(db.Integer)

    def __init__(self, name, phone, state):
        self.name = name
        self.phone = phone
        self.state = state
    def __repr__(self):
        return '<People %r>' %self.name


domain_plugin = db.Table('domain_plugin',
                       db.Column('plugin_id',db.Integer,db.ForeignKey('plugin.id'),primary_key=True),
                       db.Column('domain_id',db.Integer,db.ForeignKey('domain.id'),primary_key=True)
                       )
class Domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    domain = db.Column(db.String(200))
    type = db.Column(db.Integer)
    port = db.Column(db.Integer)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    vullist = db.relationship('Plugin', secondary=domain_plugin, backref=db.backref('plugin'))
    def __init__(self, domain, type, port):
        self.domain = domain
        self.type = type
        self.port = port

    def __repr__(self):
        return'<Domain %r>'%self.domain

class Ip(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    ip = db.Column(db.String(20))
    type = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, ip, type):
        self.ip = ip
        self.type = type


    def __repr__(self):
        return '<Ip %r>'%self.ip


#漏洞扫描插件
class Plugin(db.Model):
    __tablename__ = 'plugin'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(200))
    info = db.Column(db.String(200))
    rank = db.Column(db.String(5))
    type = db.Column(db.String(200))
    author = db.Column(db.String(20))
    url = db.Column(db.String(200))
    keyword = db.Column(db.String(200))
    source = db.Column(db.Integer) #来源
    addtime = db.Column(db.DateTime, default=datetime.datetime.now)
    filename = db.Column(db.String(200))

    def __init__(self, name, info, rank, type, author, url, keyword, source,filename):
        self.name = name
        self.filename = filename
        self.type = type
        self.rank = rank
        self.author =author
        self.url = url
        self.info =info
        self.keyword = keyword
        self.source = source

    def __repr__(self):
        return '<Plugin %r>' % self.name













