# coding=utf-8

import time
import os
import sys
import json
import threading

import urllib.request
import re
import hashlib
sys.path.append(sys.path[0]+'/vuldb')
sys.path.append(sys.path[0]+"/../")
from views import db
from views.Models import Domain,Plugin
db.create_all()
PLUGIN_DB = {}

PASSWORD_DIC = []
TIME_OUT = 10
THREAD_NUM = 50
class VulScan(threading.Thread):

    def __init__(self,domain,plugin):
        threading.Thread.__init__(self)
        self.domain = domain
        self.plugin = plugin
        self.result_info = ''
        self.json_code ={}

        self.scan()


    def scan(self):

        if '.json' in self.plugin.filename:  # 标示符检测模式
            try:
                self.load_json_plugin()  # 读取漏洞标示
                self.set_request()  # 标示符转换为请求
                self.poc_check()  # 检测
            except:
                pass
        else:  # 脚本检测模式
            plugin_filename = self.plugin.filename
            if self.plugin.filename not in PLUGIN_DB:
                plugin_res = __import__(plugin_filename)
                setattr(plugin_res, "PASSWORD_DIC", PASSWORD_DIC)  # 给插件声明密码字典
                PLUGIN_DB[plugin_filename] = plugin_res
                #PLUGIN_DB['filename'] = plugin_filename
            try:
                self.result_info = PLUGIN_DB[plugin_filename].check(str(self.domain.domain), int(self.domain.port),
                                                                    TIME_OUT)

            except:
                return
        self.save_request()  # 保存结果


    def load_json_plugin(self):
        json_plugin = open(sys.path[0] + '/vuldb/' + self.plugin.filename).read()
        self.json_code['plugin'] = json.loads(json_plugin)['plugin']

    def set_request(self):

        url = 'http://' + self.domain.domain + ":" + str(self.domain.port) + self.json_code['plugin']['url']
        if self.json_code['plugin']['method'] == 'GET':
            request = urllib.request.Request(url)
        else:
            request = urllib.request.Request(url, self.json_code['plugin']['data'])
        self.poc_request = request

    def get_code(self, header, html):
        try:
            m = re.search(r'<meta.*?charset=(.*?)"(>| |/)', html, flags=re.I)
            if m: return m.group(1).replace('"', '')
        except:
            pass
        try:
            if 'Content-Type' in header:
                Content_Type = header['Content-Type']
                m = re.search(r'.*?charset=(.*?)(;|$)', Content_Type, flags=re.I)
                if m: return m.group(1)
        except:
            pass

    def poc_check(self):

        try:
            res = urllib.request.urlopen(self.poc_request, timeout=30)
            res_html = res.read(204800)
            header = res.headers

            # res_code = res.code
        except(urllib.request.HTTPError) as e:
            # res_code = e.code
            header = e.headers
            res_html = e.read(204800)
        except( Exception) as e:

            return
        try:
            html_code = self.get_code(header, res_html).strip()
            if html_code and len(html_code) < 12:
                res_html = res_html.decode(html_code).encode('utf-8')
        except:
            pass
        an_type = self.json_code['plugin']['analyzing']
        vul_tag = self.json_code['plugin']['tag']
        analyzingdata = self.json_code['plugin']['analyzingdata']
        if an_type == 'keyword':
            # print poc['analyzingdata'].encode("utf-8")
            if analyzingdata.encode("utf-8") in res_html: self.result_info = vul_tag
        elif an_type == 'regex':
            if re.search(analyzingdata, res_html, re.I): self.result_info = vul_tag
        elif an_type == 'md5':
            md5 = hashlib.md5()
            md5.update(res_html)
            if md5.hexdigest() == analyzingdata: self.result_info = vul_tag

    def save_request(self):
        print(self.result_info)
        if self.result_info:
            try:
                print(self.result_info)
            # self.wx_send(w_vul)  # 自行定义漏洞提醒
            except(Exception) as e:
                pass

def init():
    script_plugin = []
    json_plugin = []
    plugin_list = db.session.query(Plugin).filter().all()
    file_list = os.listdir(sys.path[0]+'/vuldb')

    for filename in file_list:
        try:
            if filename.split('.')[1]=='py':
                script_plugin.append(filename.split('.')[0])
            if filename.split('.')[1] == 'json':
                json_plugin.append(filename)
        except :
            pass
    if len(plugin_list) == len(script_plugin)+len(json_plugin):

        for plugin in plugin_list:
            db.session.delete(plugin)
        db.session.commit()

        for plugin_name in script_plugin:

            try:
                res_tmp = __import__(plugin_name)
                plugin_info = res_tmp.get_plugin_info()
                plugin = Plugin(name=plugin_info['name'],info=plugin_info['info'],rank=plugin_info['level'],type=plugin_info['type'],author=plugin_info['author'],url=plugin_info['url'],keyword=plugin_info['keyword'],source=plugin_info['source'],filename=plugin_name)

                db.session.add(plugin)
                db.session.commit()

            except (Exception) as e:
                pass
        for plugin_name in json_plugin:
            try:
                json_text = open(sys.path[0]+"/vuldb/"+plugin_name,'r').read()
                plugin_info = json.loads(json_text)
                plugin = Plugin(name=plugin_info['name'], info=plugin_info['info'], rank=plugin_info['level'],
                            type=plugin_info['type'], author=plugin_info['author'], url=plugin_info['url'],
                            keyword=plugin_info['keyword'], source=plugin_info['source'], filename=plugin_name)

                db.session.add(plugin)
                db.session.commit()
            except:
                pass

if __name__ == '__main__':
    init()
    pid = sys.argv[1]
    domains = db.session.query(Domain).filter(Domain.project_id==pid).all()
    plugins = db.session.query(Plugin).all()


    if PLUGIN_DB:
            #del sys.modules[PLUGIN_DB]  # 清理插件缓存
        PLUGIN_DB = []
    threads = []
    for domain in domains:
        for plugin in plugins:

            while True:
                if threading.activeCount() < THREAD_NUM:
                    thread = VulScan(domain,plugin)

                    thread.start()
                    threads.append(thread)

                    break
                else:
                    time.sleep(2)



            print(domain.domain+'-------'+plugin.name)



