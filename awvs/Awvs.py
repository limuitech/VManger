from Config import Config
import urllib.request
import ssl
import json


class Awvs():
    def __init__(self):

        self.url = Config.AWVS_URL
        self.user = Config.AWVS_USERNAME
        self.password = Config.AWVS_PASSWORD
        self.headers = ''
        self.set_token()

    def set_token(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        url_login = self.url+"/api/v1/me/login"
        send_headers_login = {
            'Host': 'localhost:3443',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8'
        }

        data_login = '{"email":"' + self.user + '","password":"' + self.password + '","remember_me":false}'

        req_login = urllib.request.Request(url_login, headers=send_headers_login)
        response_login = urllib.request.urlopen(req_login, data_login)
        xauth = response_login.headers['X-Auth']
        COOOOOOOOkie = response_login.headers['Set-Cookie']
        self.headers = {
            'Host': 'localhost:3443',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Auth': xauth,
            'Cookie': COOOOOOOOkie
        }

    #添加扫描任务
    def add_exec_scan(self,target):
        url = self.url+"/api/v1/targets"
        try:


            target_url = i.strip()
            data = '{"description":"222","address":"' + target_url + '","criticality":"10"}'
            # data = urllib.urlencode(data)由于使用json格式所以不用添加
            req = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(req, data)
            jo = json.loads(response.read())
            target_id = jo['target_id']  # 获取添加后的任务ID


            url_scan = "https://localhost:3443/api/v1/scans"

            data_scan = '{"target_id":' + '\"' + target_id + '\"' + ',"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"66666666666666666666666666666666"}'
            req_scan = urllib.request.Request(url_scan, headers=self.headers)
            response_scan = urllib.request.urlopen(req_scan, data_scan)

            # 以上代码实现批量加入扫描

        except(Exception) as e:
            pass

    #获取扫描任务扫描结果
    def get_scan_result(self):
        pass

    #删除扫描任务

    def del_targets(self):
        url_info = "https://localhost:3443/api/v1/targets"
        req_info = urllib.request.Request(url_info, headers=self.headers)
        response_info = urllib.request.urlopen(req_info)
        all_info = json.loads(response_info.read())
        for website in all_info.get("targets"):
            if (website.get("description")) == "222":
                url_scan_del = "https://localhost:3443/api/v1/targets/" + str(website.get("target_id"))
                req_del = urllib.request.Request(url_scan_del, headers=self.headers)
                req_del.get_method = lambda: 'DELETE'
                response_del = urllib.request.urlopen(req_del)
