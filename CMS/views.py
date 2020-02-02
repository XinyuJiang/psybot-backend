from django.shortcuts import render
import datetime
import sys
import os
sys.path.append('/home/ubuntu/program/Psybot_backend/CMS')
import random
import time
import requests
import random
import pickle
import numpy as np
import pandas as pd
import math
from math import *
import jieba
from snownlp import SnowNLP
import json

from django.db.models import Avg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from CMS.models import Userinfo, Loginfo
# from psybot.utils.NlpUtils import *
# from psybot.utils.OpenidUtils import *
# from psybot.utils.Const import *
import matplotlib.pyplot as plt
import matplotlib as  mpl
from matplotlib.font_manager import FontProperties

############# ner组件 ###############
import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
from collections import OrderedDict
from LtpParser import LtpParser
#####################################
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Psybot index.")

@csrf_exempt
def register(request):
    musername = request.GET['username']
    mpassword = request.GET['password']
    mphonenumber = request.GET['phonenumber']
    mauthority = request.GET['authority']
    #mportrait = request.GET['portrait']
    try:
        muser = Userinfo.objects.get(username=musername)
        if muser.password == mpassword:
            print(muser.username, "登录成功")
            code = '1'
            msg = "login successful"
            data = {"name":muser.username,"authority":muser.authority}
        else:
            print(muser.username, "密码错误")
            code = '-1'
            msg = "wrong password"
            data = {}
    except:
        muser = Userinfo(username=musername, password=mpassword, phonenumber=mphonenumber, authority=mauthority)
        muser.save()
        print("注册成功")
        code = '0'
        msg = "register successful"
        data = {"name":muser.username,"authority":muser.authority}
    result = {"code": code, "msg": msg, "data": data}
    response = HttpResponse(json.dumps(result))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@csrf_exempt
def setlog(request):
    mcontentid = request.GET['contentid']
    maction = request.GET['action']
    #print(mtext)
    muser = Userinfo.objects.get(username=request.GET['username'])
    mloginfo = Loginfo(user=muser, action=maction, contentid=mcontentid)
    mloginfo.save()
    print("日志存储成功")
    result = {"code": maction, "msg": "success", "data": []}
    #调取图文服务接口
    url='http://imgtext.psyhack.top/service/articles/update'
    resource = {'rstatus':maction}
    if maction == '1001':
        try:
            mcategory1 = request.GET['category1']
        except:
            print("没有修改category1")
        else:
            resource['category1'] = mcategory1
        try:
            mcategory2 = request.GET['category2']
        except:
            print("没有修改category2")
        else:
            resource['category2'] = mcategory2

    elif maction == '3002':
        mlabel = request.GET['label']        
        resource = {'rstatus':maction, 'label':mlabel}
    else:
        resource = {'rstatus':maction}
    data = {'id':mcontentid,'update':json.dumps(resource)}
    req = requests.post(url,data)
    print(req.json())

    response = HttpResponse(json.dumps(result))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@csrf_exempt
def ner(request):
    mtext = request.GET['text']
    mtag = request.GET['tag']
    ltp = LtpParser()
    words, postags = ltp.parser_process(mtext)

    NER_1 = OrderedDict()
    for index, tag in enumerate(postags):
        if tag == 'ni' and len(words[index]) > 1: #组织名
            NER_1.setdefault('ORG', set()).add(words[index])
        elif tag == 'nh' and len(words[index]) > 1:#人名
            NER_1.setdefault('PER', set()).add(words[index])
        elif tag == 'ns' and len(words[index]) > 1:#地名
            NER_1.setdefault('LOC', set()).add(words[index])
    msg = -1
    if mtag == '0': #return 人名
        msg = "get person name successful"
        data = list(NER_1['PER'])
    if mtag == '1': #return 机构名
        msg = "get organization name successful"
        data = list(NER_1['ORG'])
    if mtag == '2': #return 地名
        msg = "get location name successful"
        data = list(NER_1['LOC'])
    print(data)
    result = {"code": mtag, "msg": msg, "data": data}

    response = HttpResponse(json.dumps(result, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response