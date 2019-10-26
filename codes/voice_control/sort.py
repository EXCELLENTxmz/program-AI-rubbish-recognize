# -*- coding: utf-8 -*

import requests
import json

#a=u'小拉，我要扔骨头'
#tmp = a[a.index(u'扔')+1:]

#bak = '{"code":200,"msg":"success","newslist":[{"name":"香蕉皮","type":2,"aipre":0,"explain":"厨余垃圾是指居民日常生活及食品加工、饮食服务、单位供餐等活动中产生的垃圾。","contain":"常见包括菜叶、剩菜、剩饭、果皮、蛋壳、茶渣、骨头等","tip":"纯流质的食物垃圾、如牛奶等，应直接倒进下水口。有包装物的湿垃圾应将包装物去除后分类投放、包装物请投放到对应的可回收物或干垃圾容器"}]}'
def sort(tmp):
    url = 'http://api.tianapi.com/txapi/lajifenlei/?key=ce06af298c5c6bcaecf0f05fc1253629&word='+tmp
    req = requests.get(url)
    
    # if req.status_code == 200:
    #         print(req.text)
    jsonStr = req.text
    jsonRes = json.loads(jsonStr)
    if jsonRes['msg'] == 'success':
        result = jsonRes['newslist'][0]['explain'][0:jsonRes['newslist'][0]['explain'].index(u'圾')+1]
        print(result)
        return result
    else:
        return 0
    
    
    


