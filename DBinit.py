from views import db
import json
def initVulnerabilityClass():
    from views.Models import VulnerabilityClass
    from views.Models import Vulnerability
    with open("./pentest_nsfocus_tree.json",'r',encoding='UTF-8') as json_list:
        dict_list = json.load(json_list)

        for i in dict_list['tree']['item']['item']:
            vulnerabilityclass = VulnerabilityClass(type=i['text'])
            db.session.add(vulnerabilityclass)
            db.session.flush()
            id = vulnerabilityclass.id
            db.session.commit()
            print(i['text'])
            print(id)
            for j in i['item']:

                suggest = j.get('description','')+"||"+j.get('repair_recom','')
                describe = j.get('risk_analysis','')
                vulnerability = Vulnerability(title=j['text'],type=id,suggest=suggest,describe=describe,rank=2)

                db.session.add(vulnerability)


                db.session.commit()

db.create_all()
