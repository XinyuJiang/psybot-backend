import datetime
import os
import random
import time

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
from psybot.models import Userinfo, Activityinfo, Speechinfo, Emotioninfo, Mingxianginfo, Opinioninfo
from psybot.utils.NlpUtils import *
from psybot.utils.OpenidUtils import *
from psybot.utils.Const import *
import matplotlib.pyplot as plt
import matplotlib as  mpl



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
    result = {"code": code, "msg": "success", "data": {"openid": mopenid}}
    return HttpResponse(json.dumps(result))


@csrf_exempt
def setspeech(request):
    mtext = request.GET['text']
    mlabel = request.GET['label']
    #print(mtext)
    muser = Userinfo.objects.get(id=request.GET['user_id'])
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


# 判断文本积极或消极
@csrf_exempt
def biclassifyemotion(request):
    def predicttext(text):
        neg_dict = loadfile(neg_emotiondict)
        pos_dict = loadfile(pos_emotiondict)
        neg_count = 0
        pos_count = 0
        #print("dict:", neg_dict, pos_dict)
        # print(tokenizer(text)[0])
        for item in tokenizer(text)[0]:
            #print("item:", item)
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
    s = SnowNLP(text)
    data = 0
    if s.sentiments > 0.5:
        data = 1
    else:
        data = 0
    result = {"code": 0, "msg": "success", "data": data}
    #print(text)
    #result = {"code": 0, "msg": "success", "data": predicttext([text])}
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
    mpl.rcParams[u'font.sans-serif'] = ['simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    rlist = [0,0,0,0,0,0,0]
    mtype = ["呼吸冥想", "晚间冥想", "晨间冥想", "行走冥想", "乘车冥想", "正念减肥", "缓解焦虑"]
    mlist = ["break", "night", "morning", "walk", "riding", "lose weight", "relax"]
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    mset = Mingxianginfo.objects.filter(user=muser)
    for t in range(len(mtype)):
        itemset = mset.filter(mingxiang_type=mtype[t])
        #print(len(itemset))
        for item in itemset:
            print(item.mingxiang_end, item.mingxiang_start)
            rlist[t] += (item.mingxiang_end-item.mingxiang_start).seconds
    plt.bar(mlist,rlist,0.4)
    plt.xlabel("time")
    plt.ylabel("efficient")
    name=time.strftime('%Y%m%d%H%M%S_',time.localtime(time.time()))+request.GET['user_id']
    if not os.path.exists("./media/temp/mingxiang/"):
        os.makedirs("./media/temp/mingxiang/")
    plt.savefig("./media/temp/mingxiang/"+name+".png")
    plt.close('all')
    return HttpResponse(json.dumps({"code":0,"msg":"success","data":{"url":"https://xinyujiang.cn/media/temp/mingxiang/"+name+".png"}}))

    # code = '0'
    # result = {"code": code, "msg": "success", "data": rlist}
    # return HttpResponse(json.dumps(result))


#返回效价统计信息
@csrf_exempt
def user_stat(request):
    print(request.GET["user_id"])
    if "user_id" not in request.GET:
        return HttpResponse(json.dumps({"code":-1, "msg":"unexpected params!", "data":[]}))
    # info = Emotioninfo.objects.filter(user_id=request.GET['user_id']).values('create_time','efficient')
    info = Emotioninfo.objects.filter(user_id=request.GET['user_id'], efficient__gte=0).values('create_time').annotate(avg=Avg('efficient')).values('create_time','avg')
    #print("info",info)
    time_list=[rst['create_time'].strftime("%Y-%m-%d") for rst in info]
    #print("time_list:",time_list)
    efficient_list = [rst['avg'] for rst in info]
    rt = [[rst['create_time'].strftime("%Y-%m-%d"),rst['avg']] for rst in info]
    #print("efficient_list:",efficient_list)
    # plt.plot(time_list,efficient_list)
    # plt.xlabel("time")
    # plt.ylabel("efficient")
    # name=time.strftime('%Y%m%d%H%M%S_',time.localtime(time.time()))+request.GET['user_id']
    # if not os.path.exists("./media/temp/efficient/"):
    #     os.makedirs("./media/temp/efficient/")
    # plt.savefig("./media/temp/efficient/"+name+".png")
    # plt.close('all')

    #return HttpResponse(json.dumps({"code":0,"msg":"success","data":{"url":"https://xinyujiang.cn/media/temp/efficient/"+name+".png"}}))
    return HttpResponse(json.dumps({"code":0,"msg":"success","data":rt}))

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


#意见反馈接口
@csrf_exempt
def setopinion(request):
    mtext = request.GET['text']
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    mtitle = request.GET['title']
    #print(mtext)
    mopinioninfo = Opinioninfo(user=muser, text=mtext, title=mtitle)
    mopinioninfo.save()
    print("文本存储成功")
    code = '0'
    result = {"code": code, "msg": "store opinion successful", "data": []}
    return HttpResponse(json.dumps(result))


#得到用户输入的所有文本
@csrf_exempt
def getusertext(request):
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    #print(mtext)
    print(muser.id)
    mspeechinfo = Speechinfo.objects.filter(user=muser).filter(label=request.GET['label'])
    text = []
    for item in mspeechinfo:
        #print(item.text)
        text.append(item.text)
    code = '0'
    result = {"code": code, "msg": "output text successful", "data": text}
    return HttpResponse(json.dumps(result))

#得到用户输入的所有意见
@csrf_exempt
def getopinion(request):
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    #print(mtext)
    print(muser.id)
    mopinioninfo = Opinioninfo.objects.filter(user=muser)
    text = []
    for item in mopinioninfo:
        #print(item.text)
        text.append(item.text)
    code = '0'
    result = {"code": code, "msg": "get opinion successful", "data": text}
    return HttpResponse(json.dumps(result))


#得到各类冥想次数
@csrf_exempt
def mingxiang_stat(request):
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    #print(mtext)
    print(muser.id)
    mmingxianginfo = Mingxianginfo.objects.filter(user=muser)
    #print(mmingxianginfo)
    count = {"呼吸冥想":0,"晚间冥想":0,"晨间冥想":0,"行走冥想":0,"乘车冥想":0,"正念减肥":0,"缓解焦虑":0}
    for item in mmingxianginfo:
        #print("1",item.mingxiang_type)
        if item.mingxiang_type in count.keys():
            count[item.mingxiang_type] += 1
    code = '0'
    result = {"code": code, "msg": "get mingxianginfo successful", "data": count}
    #print(result)
    return HttpResponse(json.dumps(result))


#得到使用时长，天数信息
@csrf_exempt
def daysrecord(request):
    muser = Userinfo.objects.get(id=request.GET['user_id'])
    #print(mtext)
    #print(muser.id)
    signinfo = Activityinfo.objects.filter(user=muser)
    #print(signinfo[0])
    a = datetime.datetime.now()
    b = datetime.datetime(a.year,a.month,a.day)
    c = datetime.datetime(signinfo[0].open_time.year,signinfo[0].open_time.month,signinfo[0].open_time.day)
    #print(b,c)
    #print((b-c).days)
    #print(datetime.datetime.now()-item.open_time)
    #print((datetime.datetime.now()-item.open_time).days)
    data = [(b-c).days]
    code = '0'
    result = {"code": code, "msg": "get daysrecord successful", "data": data}
    return HttpResponse(json.dumps(result))


#文章接口
@csrf_exempt
def paper_list(request):
    count = []
    count.append({'id':0,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.3.31','image':'https://xinyujiang.cn/media/paper/image/0.jpg','src':'https://mp.weixin.qq.com/s/1_HXUsO72xbTPhJ_ieQ4Ew'})
    count.append({'id':1,'title':'微博上线「仅半年可见」功能：现代人究竟在隐藏什么','time':'2019.4.6','image':'https://xinyujiang.cn/media/paper/image/1.jpg','src':'https://mp.weixin.qq.com/s/IBiHytiXPTTkanHX5qEiwQ'})
    count.append({'id':2,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.4.12','image':'https://xinyujiang.cn/media/paper/image/2.jpg','src':'https://mp.weixin.qq.com/s/QFSFgAXXKlUWGBb0YWqg2g'})
    count.append({'id':3,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.4.16','image':'https://xinyujiang.cn/media/paper/image/3.jpg','src':'https://mp.weixin.qq.com/s/qxEbeAlE3sbET4252JEHEg'})
    count.append({'id':4,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.4.20','image':'https://xinyujiang.cn/media/paper/image/4.jpg','src':'https://mp.weixin.qq.com/s/Nnm8OunFfHROJK283OS_IQ'})
    count.append({'id':5,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.4.25','image':'https://xinyujiang.cn/media/paper/image/5.jpg','src':'https://mp.weixin.qq.com/s/ckAq9iOEDc8CbHi6go8vmA'})
    count.append({'id':6,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.4.30','image':'https://xinyujiang.cn/media/paper/image/6.jpg','src':'https://mp.weixin.qq.com/s/YIcvFt79VE6c8sEJIgYhkQ'})
    count.append({'id':7,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.5.6','image':'https://xinyujiang.cn/media/paper/image/7.jpg','src':'https://mp.weixin.qq.com/s/GUpA-4SRfFy43fRnJUA88A'})
    count.append({'id':8,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.5.24','image':'https://xinyujiang.cn/media/paper/image/8.jpg','src':'https://mp.weixin.qq.com/s/8cdOPjls-3Lwlk4TK_oB0g'})
    count.append({'id':9,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.6.3','image':'https://xinyujiang.cn/media/paper/image/9.jpg','src':'https://mp.weixin.qq.com/s/-QFCsYOhEONUyEDaK0_GZw'})
    count.append({'id':10,'title':'都2019年了，你还以为心理咨询就是闲聊天？','time':'2019.6.10','image':'https://xinyujiang.cn/media/paper/image/10.jpg','src':'https://mp.weixin.qq.com/s/2wls4rZ7cdW1l13cNnWuJw'})    
    code = '0'
    result = {"code": code, "msg": "get paperlist successful", "data": count}
    return HttpResponse(json.dumps(result))

#冥想接口
@csrf_exempt
def mingxiang_list(request):
    count = []
    count.append({'id':1,'picture':'https://xinyujiang.cn/media/background/1.jpg','music':'https://xinyujiang.cn/static/mingxiang/1.mp3','title':'呼吸冥想','content':'呼吸冥想 | 调节呼吸帮助你进行放松'})
    count.append({'id':2,'picture':'https://xinyujiang.cn/media/background/2.jpg','music':'https://xinyujiang.cn/static/mingxiang/2.mp3','title':'晚间冥想','content':'晚间冥想 | 陪伴你在入睡前进行放松'})
    count.append({'id':3,'picture':'https://xinyujiang.cn/media/background/3.jpg','music':'https://xinyujiang.cn/static/mingxiang/3.mp3','title':'晨间冥想','content':'晨间冥想 | 适用于起床后帮助你提高注意力'})
    count.append({'id':4,'picture':'https://xinyujiang.cn/media/background/4.jpg','music':'https://xinyujiang.cn/static/mingxiang/4.mp3','title':'行走冥想','content':'行走冥想 | 适用于出行时的碎片时间训练'})
    count.append({'id':5,'picture':'https://xinyujiang.cn/media/background/5.jpg','music':'https://xinyujiang.cn/static/mingxiang/5.mp3','title':'乘车冥想','content':'乘车冥想 | 合理利用乘车碎片时间进行冥想'})
    count.append({'id':6,'picture':'https://xinyujiang.cn/media/background/6.jpg','music':'https://xinyujiang.cn/static/mingxiang/6.mp3','title':'正念减肥','content':'正念减肥 | 用于缓解食欲管住嘴'})
    count.append({'id':7,'picture':'https://xinyujiang.cn/media/background/7.jpg','music':'https://xinyujiang.cn/static/mingxiang/7.mp3','title':'缓解焦虑','content':'缓解焦虑 | 焦虑时强烈建议进行这一训练'})
  
    code = '0'
    result = {"code": code, "msg": "get mingxianglist successful", "data": count}
    return HttpResponse(json.dumps(result))


#每日推荐接口
@csrf_exempt
def dailyrecommend(request):
    count = []
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/1.jpg','text':'生活中其实没有绝境，绝境在于你自己的心没有打开。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/2.jpg','text':'快乐源于每天的自我感觉良好，生活充实就不会胡思乱想。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/3.jpg','text':'放弃凡事争个明白的傻念头吧，真正的智者从不会为小事斤斤计较，他们总是坚持走自己的路，不管别人怎样评说，而时间最后总会证明他们是正确的。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/4.jpg','text':'有时候，我们追寻更多的东西，却忘了我们已经拥有的一切。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/5.jpg','text':'我从不担心我努力了不优秀，只担心优秀的人都比我更努力。决定你高度的是你对自己的要求。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/6.jpg','text':'如果说犯错是成长付出的代价，那么改错就是成熟的过程。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/7.jpg','text':'不要畏惧结束，所有的结局都是一个新的开端。人生如圆，终点亦是起点。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/8.jpg','text':'不管外面的风风雨雨，惊涛骇浪。不管世事变幻沧海桑田。给生活以一丝坦然，给生命一份真实，给自已一份感激，给他人一份宽容。淡淡的生活。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/9.jpg','text':'心若改变，你的态度跟着改变;态度改变，你的习惯跟着改变;习惯改变，你的性格跟着改变;性格改变，你的人生跟着改变。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/10.jpg','text':'也许身边的人越来越少，可是我知道留下来的都是最重要的。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/11.jpg','text':'一些事，闯进生活，高兴的，痛苦的，时间终将其消磨变淡。经历的多了，心就坚强了，路就踏实了。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/12.jpg','text':'生活的智慧就是如何让自己从梦想活回现实，让从容成为一种习惯。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/13.jpg','text':'人生由淡淡的悲伤和淡淡的幸福组成，在小小的期待、偶尔的兴奋和沉默的失望中度过每一天，然后带着一种想说却又说不出来的“懂”，作最后的转身离开。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/14.jpg','text':'任何打击都不应该成为你堕落的借口，你改变不了这个世界，但你可以改变自己，选择一条正确的路，坚定的走下去'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/15.jpg','text':'人心之所以不安，就是把自己寄托在那些不稳定和不真实的东西上。你把房子盖在流沙上，却渴望一个永远安定的窝。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/16.jpg','text':'若时时原谅自己，必常常迷失自己;若处处善待自己，必屡屡失却自己。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/17.jpg','text':'若将人生一分为二，前半段叫“不犹豫”，后半段叫“不后悔”。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/18.jpg','text':'最大的淡定，是看透人生以后依然能够热爱生活。拿得起，有担当，不推诿，不逃避，直面凛冽的人生。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/19.jpg','text':'人生有如三道茶，第一道苦如生命，第二道甜似爱情，第三道淡如微风!----三毛'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/20.jpg','text':'生活总是这样，不能叫人处处都满意。但我们还要热情地活下去。人活一生，值得爱的东西很多，不要因为一个不满意，就灰心。——路瑶'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/21.jpg','text':'人的心只容得下一定程度的绝望，海绵已经吸够了水，即使大海从它上面流过，也不能再给它增添一滴水了。——维克多·雨果'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/22.jpg','text':'有可以浪掷的东西，也有很想珍惜的人，有追寻，也有坠落，醉过一场，也清醒地看过人间色相，人生才不是空中鸟迹，飞过不留痕。───张小娴'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/23.jpg','text':'人，有了物质才能生存;人，有了理想才谈得上生活。脚步不能达到的地方，眼光可以到达;眼光不能到达的地方，精神可以飞到。——雨果'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/24.jpg','text':'生活不是高速公路，哪来的一路畅通。这一个转角，即使没有遇到谁，至少可以遇到焕然一新的自己。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/25.jpg','text':'一个不知道自己是怎么成功的成功的人，远比一个知道自己是怎么失败的失败的人来的更可悲，因为前者只是一个美丽的误会，而后者必将占领成功的高地。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/26.jpg','text':'你只知道你走了很多弯路，你不知道你多看了很多风景。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/27.jpg','text':'每一个伟大，多会有争议;每一次完美，都有无穷的缺憾。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/28.jpg','text':'我希望自已也是一颗星星：如果我会发光，就不必害怕黑暗。如果我自己是那么美好，那么一切恐惧就可以烟消云散。——王小波'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/29.jpg','text':'一个养花的人告诉我们，几乎是所有的白花都很香，愈是颜色艳丽的花愈是缺乏芬芳。他的结论是：人也一样，愈朴素单纯的人，愈有内在的芳香。'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/30.jpg','text':'人之所以痛苦，在于追求错误的东西。如果你不给自己烦恼，别人也永远不可能给你烦恼。因为你自己的内心，你放不下。好好的管教你自己，不要管别人。——路遥'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/31.jpg','text':'别人怎么看你，或者你自己如何地探测生活，都不重要。重要的是你必须要用一种真实的方式，度过在手指缝之间如雨水一样无法停止下落的时间，你要知道自己将会如何生活。——安妮宝贝'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/32.jpg','text':'在最深的绝望里，遇见最美丽的风景。—— 几米'})
    count.append({'photo_url':'https://xinyujiang.cn/media/daily/pic/33.jpg','text':'即使全世界的人都不爱你，你也要好好的自己爱自己。—— 果果'})
    
    code = '0'
    result = {"code": code, "msg": "get dailyrecommend successful", "data": count}
    return HttpResponse(json.dumps(result))
