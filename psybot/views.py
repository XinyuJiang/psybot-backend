import datetime
import os
import random
import time

import numpy as np
import pandas as pd
import math
from math import *
import jieba
import json

from django.db.models import Avg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from psybot.models import Userinfo, Activityinfo, Speechinfo, Emotioninfo, Mingxianginfo
from psybot.utils.NlpUtils import *
from psybot.utils.OpenidUtils import *
from psybot.utils.Const import *
import matplotlib.pyplot as plt


def index(request):
    return HttpResponse("Hello, world. You're at the Psybot index.")


def calculate(request):
    formula = request.GET['formula']
    try:
        result = eval(formula, {})
    except:
        result = 'Error formula'
    return HttpResponse(result)


@csrf_exempt
def register(request):
    mcode = request.GET['code']
    mopenid = OpenidUtils(mcode).get_openid()
    # iddict[mcode] = mopenid #将code：openid键值对
    mnickname = request.GET['nickname']
    mportrait = request.GET['portrait']
    try:
        muser = Userinfo.objects.get(openid=mopenid)
        print(muser.nickname, "登录成功")
        code = '1'
    except:
        muser = Userinfo(openid=mopenid, nickname=mnickname, portrait=mportrait)
        muser.save()
        print("注册成功")
        code = '0'
    mactivityinfo = Activityinfo(user=muser)
    mactivityinfo.save()
    result = {"code": code, "msg": "success", "data": [{"openid": mopenid}]}
    return HttpResponse(json.dumps(result))


@csrf_exempt
def setspeech(request):
    mtext = request.GET['text']
    mlabel = request.GET['label']
    mopenid = request.GET['openid']
    print(mtext)
    muser = Userinfo.objects.get(openid=mopenid)
    mspeechinfo = Speechinfo(user=muser, text=mtext, label=mlabel)
    mspeechinfo.save()
    print("文本存储成功")
    code = '0'
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


# 根据效价判断是否需要干预
@csrf_exempt
def emotionevaluate(request):
    mefficient = request.GET['efficient']
    mopenid = request.GET['openid']

    muser = Userinfo.objects.get(openid=mopenid)
    memotioninfo = Emotioninfo(user=muser, efficient=mefficient)
    memotioninfo.save()
    print("情绪信息存储成功")

    if int(mefficient) < 4:
        code = '1'  # 需要干预
    else:
        code = '0'  # 不需要干预
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


# 文本分类---信念判断
@csrf_exempt
def classifytext(request):
    def loadfile(mfile):
        rtndata = []
        with open(mfile, 'r') as load_f:
            load_data = json.load(load_f)
            for k in range(0, 8):
                # print(k)
                rtndata.append([item for item in load_data[k].keys()])
        return rtndata

    mfile = trainbeliefdata
    data = loadfile(mfile)

    l0 = 13
    l1 = 13
    l2 = 13
    l3 = 13
    l4 = 13
    l5 = 13
    l6 = 13
    l7 = 13

    def fileextraction(data):
        # 存储对应label的词的words分布
        label0dict = {}
        label1dict = {}
        label2dict = {}
        label3dict = {}
        label4dict = {}
        label5dict = {}
        label6dict = {}
        label7dict = {}

        # print("data", data)

        for i in range(len(data)):
            temp = tokenizer(data[i])
            # 扁平化操作
            textset = []
            for sentence in temp:
                for word in sentence:
                    textset.append(word)
            textset = set(textset)
            # print("textset:", textset)
            for word in textset:
                if i == 0:
                    if word in label0dict:
                        label0dict[word] += 1
                    else:
                        label0dict[word] = 1
                if i == 1:
                    if word in label1dict:
                        label1dict[word] += 1
                    else:
                        label1dict[word] = 1
                if i == 2:
                    if word in label2dict:
                        label2dict[word] += 1
                    else:
                        label2dict[word] = 1
                if i == 3:
                    if word in label3dict:
                        label3dict[word] += 1
                    else:
                        label3dict[word] = 1
                if i == 4:
                    if word in label4dict:
                        label4dict[word] += 1
                    else:
                        label4dict[word] = 1
                if i == 5:
                    if word in label5dict:
                        label5dict[word] += 1
                    else:
                        label5dict[word] = 1
                if i == 6:
                    if word in label6dict:
                        label6dict[word] += 1
                    else:
                        label6dict[word] = 1
                if i == 7:
                    if word in label7dict:
                        label7dict[word] += 1
                    else:
                        label7dict[word] = 1
        # print("label1dict:", label1dict)
        return [label0dict, label1dict, label2dict, label3dict, label4dict, label5dict, label6dict, label7dict]

    labeldict = fileextraction(data)
    print("labeldict:", labeldict)

    def sort_by_value(d):
        items = d.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort()
        return [backitems[i][1] for i in range(0, len(backitems))]

    def predicttext(text):
        # 首先计算属于label0的概率：
        sumlen = sum([l0, l1, l2, l3, l4, l5, l6, l7])
        p0 = math.log(sumlen / l0)
        p1 = math.log(sumlen / l1)
        p2 = math.log(sumlen / l2)
        p3 = math.log(sumlen / l3)
        p4 = math.log(sumlen / l4)
        p5 = math.log(sumlen / l5)
        p6 = math.log(sumlen / l6)
        p7 = math.log(sumlen / l7)

        # p1 = 1
        # 采用1-Laplace变换
        # 取对数来避免下溢的问题
        seg_list = jieba.cut(text, HMM=False)
        for word in seg_list:
            # print("word:", word)
            if word in labeldict[0].keys():
                p0 += math.log(1.0 * (len(labeldict[0])) / (labeldict[0][word] + 1))
            else:
                p0 += math.log(len(labeldict[0]))

            if word in labeldict[1].keys():
                p1 += math.log(1.0 * (len(labeldict[1])) / (labeldict[1][word] + 1))
            else:
                p1 += math.log(len(labeldict[1]))

            if word in labeldict[2].keys():
                p2 += math.log(1.0 * (len(labeldict[2])) / (labeldict[2][word] + 1))
            else:
                p2 += math.log(len(labeldict[2]))

            if word in labeldict[3].keys():
                p3 += math.log(1.0 * (len(labeldict[3])) / (labeldict[3][word] + 1))
            else:
                p3 += math.log(len(labeldict[3]))

            if word in labeldict[4].keys():
                p4 += math.log(1.0 * (len(labeldict[4])) / (labeldict[4][word] + 1))
            else:
                p4 += math.log(len(labeldict[4]))

            if word in labeldict[5].keys():
                p5 += math.log(1.0 * (len(labeldict[5])) / (labeldict[5][word] + 1))
            else:
                p5 += math.log(len(labeldict[5]))

            if word in labeldict[6].keys():
                p6 += math.log(1.0 * (len(labeldict[6])) / (labeldict[6][word] + 1))
            else:
                p6 += math.log(len(labeldict[6]))

            if word in labeldict[7].keys():
                p7 += math.log(1.0 * (len(labeldict[7])) / (labeldict[7][word] + 1))
            else:
                p7 += math.log(len(labeldict[7]))

        a = {"0": p0, "1": p1, "2": p2, "3": p3, "4": p4, "5": p5, "6": p6, "7": p7}
        return sort_by_value(a)

    text = request.GET['text']
    result = {"code": 0, "msg": "success", "data": predicttext(text)}
    return HttpResponse(json.dumps(result))


# 建立用户本次交流的情绪信息表
@csrf_exempt
def setemotion(request):
    mopenid = request.GET['openid']
    mefficient = request.GET['efficient']
    mawake = request.GET['awake']
    mbelief = request.GET['belief']
    mactivity = request.GET['activity']
    mmind = request.GET['mind']
    mcontenta = request.GET['ContentA']
    mcontentb = request.GET['ContentB']
    mcontentm = request.GET['ContentM']

    muser = Userinfo.objects.get(openid=mopenid)
    memotioninfo = Emotioninfo(user=muser, awake=mawake, belief=mbelief, efficient=mefficient, activity=mactivity, mind=mmind, contenta=mcontenta, contentb=mcontentb, contentm=mcontentm)
    memotioninfo.save()
    print("情绪信息存储成功")
    code = '0'
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


# 冥想反馈
@csrf_exempt
def setmind(request):
    mopenid = request.GET['openid']
    mtype = request.GET['type']
    mbegintime = request.GET['awake']
    mendtime = request.GET['belief']
    mresponse = request.GET['content']
    # muser = Userinfo.objects.get(openid=mopenid)
    # memotioninfo = Emotioninfo(user=muser, awake=mawake, belief=mbelief, content=mcontent, efficient=mefficient)
    # memotioninfo.save()
    print("情绪信息存储成功")
    code = '0'
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


# 判断文本积极或消极
@csrf_exempt
def biclassifyemotion(request):
    def predicttext(text):
        neg_dict = loadfile(neg_emotiondict)
        pos_dict = loadfile(pos_emotiondict)
        neg_count = 0
        pos_count = 0
        print("dict:", neg_dict, pos_dict)
        # print(tokenizer(text)[0])
        for item in tokenizer(text)[0]:
            print("item:", item)
            if item in neg_dict:
                neg_count += 1
            if item in pos_dict:
                pos_count += 1
        print("pos:neg", pos_count, neg_count)
        # 0表示负数
        if neg_count > pos_count:
            return 0
        if pos_count > neg_count:
            return 1
        # 相等则随机判断
        return random.choice('01')

    text = request.GET['text']
    print(text)
    result = {"code": 0, "msg": "success", "data": predicttext([text])}
    return HttpResponse(json.dumps(result))


# 情绪分析报告生成
@csrf_exempt
def emotion_analyze(request):
    mopenid = request.GET['openid']
    muser = Userinfo.objects.get(openid=mopenid)
    #找到近五天的数据
    i = datetime.datetime.now()-datetime.timedelta(days=5)
    q = Emotioninfo.objects.filter(
        user=muser
    ).filter(create_time__gte=datetime.date(i.year, i.month, i.day))
    #输出近五天的记录的效价
    rlist = []
    tlist = []
    for item in q:
        rlist.append(item.efficient)
        tlist.append(item.create_time)
    result = {"code": 0, "msg": "success", "data": [rlist, tlist]}
    return HttpResponse(json.dumps(result))

# 建立用户的冥想信息表
@csrf_exempt
def setmingxiang(request):
    mopenid = request.GET['openid']
    mstart = request.GET['mingxiang_start']
    mend = request.GET['mingxiang_end']
    mtype = request.GET['mingxiang_type']
    mresponse = request.GET['mingxiang_response']

    muser = Userinfo.objects.get(openid=mopenid)
    mmingxianginfo = Mingxianginfo(user=muser, mingxiang_start=mstart, mingxiang_end=mend, mingxiang_type=mtype, mingxiang_response=mresponse)
    mmingxianginfo.save()
    print("冥想信息存储成功")
    code = '0'
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


# 统计指定用户的平均冥想时间
@csrf_exempt
def calcmingxiang(request):
    mopenid = request.GET['openid']

    rlist = [0,0,0,0,0,0,0]
    mtype = ["呼吸练习", "晚间冥想", "晨间冥想", "行走冥想", "乘车冥想", "正念减肥", "缓解焦虑"]
    muser = Userinfo.objects.get(openid=mopenid)
    mset = Mingxianginfo.objects.filter(user=muser)
    for t in range(len(mtype)):
        itemset = mset.filter(mingxiang_type=mtype[t])
        #print(len(itemset))
        for item in itemset:
            #print(item.mingxiang_end, item.mingxiang_start)
            rlist[t] += (item.mingxiang_end-item.mingxiang_start).days
    code = '0'
    result = {"code": code, "msg": "success", "data": rlist}
    return HttpResponse(json.dumps(result))


#返回效价统计信息
@csrf_exempt
def user_stat(request):
    print(request.GET["user_id"])
    if "user_id" not in request.GET:
        return HttpResponse(json.dumps({"code":-1, "msg":"unexpected params!", "data":[]}))
    # info = Emotioninfo.objects.filter(user_id=request.GET['user_id']).values('create_time','efficient')
    info = Emotioninfo.objects.filter(user_id=request.GET['user_id']).values('create_time').annotate(avg=Avg('efficient')).values('create_time','avg')
    #print(info)
    time_list=[rst['create_time'].strftime("%Y-%m-%d") for rst in info]
    efficient_list = [rst['avg'] for rst in info]
    #print(time_list)
    plt.plot(time_list,efficient_list)
    plt.xlabel("time")
    plt.ylabel("efficient")
    name=time.strftime('%Y%m%d%H%M%S_',time.localtime(time.time()))+request.GET['user_id']
    if not os.path.exists("./media/temp/"):
        os.makedirs("./media/temp/")
    plt.savefig("./media/temp/"+name+".png")
    return HttpResponse(json.dumps({"code":0,"msg":"success","data":{"url":"https://xinyujiang.cn/media/temp/"+name+".png"}}))


#返回userid
@csrf_exempt
def getuserid(request):
    #print(request.GET["user_id"])

    if "openid" not in request.GET:
        return HttpResponse(json.dumps({"code":-1, "msg":"unexpected params!", "data":[]}))
    mopenid = request.GET['openid']
    muser = Userinfo.objects.get(openid=mopenid)
    user_id = muser.id
    code = '0'
    result = {"code": code, "msg": "success", "data": user_id}
    return HttpResponse(json.dumps(result))