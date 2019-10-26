import requests
import base64
import re
import json
import os
def takePhoto():
    os.system('raspistill -t 500 -o /home/pi/mPython/imgs/test.jpg')
    
def getAPI():
    url = 'http://api.tianapi.com/txapi/imglajifenlei/'

    f = open(r'imgs/test.jpg', 'rb')
    encode = base64.b64encode(f.read())
    f.close()

    body = {
        "key": "ce06af298c5c6bcaecf0f05fc1253629",
        "img": str(encode, encoding='utf8')
    }
    headers = {'content-type': "application/x-www-form-urlencoded"}

    response = requests.post(url, data=body, headers=headers)
    '''
    if response.status_code == 200:
        print(response.text)
    else:
        raise Exception
    '''
    jsonStr = response.text
    jsonRes = json.loads(jsonStr)
    lajitip = jsonRes['newslist'][0]['lajitip']
    'print(lajitip)'
    '''
    利用正则匹配垃圾类型
    '''
    reStr = '(?<=是).*垃圾'
    result = re.findall(reStr,lajitip)
    if not len(result) == 0 :
        print(result[0])
    else:
        raise Exception

if __name__ == '__main__':
    takePhoto()
    getAPI()
    