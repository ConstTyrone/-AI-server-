#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
from auth_util import gen_sign_headers
import time

URI_require = '/api/v1/task_submit'
DOMAIN_require = 'api-ai.vivo.com.cn'
METHOD_require = 'POST'

def submit(img_require_message,APP_ID,APP_KEY):
    params = {}
    data =img_require_message

    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD_require, URI_require, params)
    headers['Content-Type'] = 'application/json'

    url = 'http://{}{}'.format(DOMAIN_require, URI_require)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(response.status_code, response.text)
        return response.json()


#----------------------------------------------------------------
import requests
import base64
import json
from auth_util import gen_sign_headers

URI_get = '/api/v1/task_progress'
DOMAIN_get = 'api-ai.vivo.com.cn'
METHOD_get = 'GET'
	
def progress(Task_id,APP_ID,APP_KEY):
    params = {
        'task_id': Task_id
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD_get, URI_get, params)

    uri_params = ''
    for key, value in params.items():
        uri_params = uri_params + key + '=' + value + '&'
    uri_params = uri_params[:-1]

    url = 'http://{}{}?{}'.format(DOMAIN_get, URI_get, uri_params)
    print('Try to get from url:\n', url)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    
    else:
        print('GET error:', response.status_code) 
        print(response.text)
        return {'result':{'finished':'Error'}}
        

#----------------------------------------------------------------

#img_message遵循比赛官网的请求参数；
# 例如：
# {
#     'height': 768,
#     'width': 576,
#     'prompt': '一只梵高画的猫',
#     'styleConfig': '55c682d5eeca50d4806fd1cba3628781'
#     }
def askVivo_for_img(img_message,APP_ID,APP_KEY):
    require=submit(img_message,APP_ID,APP_KEY)
    if(require['code']==200):
        #这里不用设置请求次数避免死循环，查询超限后会自动break
        while True:
            time.sleep(3)
            get_result = progress(require['result']['task_id'],APP_ID,APP_KEY)
            if(get_result['result']['finished'] == True):
                print(get_result['result']['images_url'])
                print(json.dumps(get_result['result']['images_url']))
                break
            elif(get_result['result']['finished'] == 'Error'):
                print('向vivo查询次数超限')
                return {'result':{'images_url':'ERROR: MAX REQUIREMENT'}}
        return get_result['result']['images_url']


    