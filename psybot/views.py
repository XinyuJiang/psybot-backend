import numpy as np
import pandas as pd
import math
from math import *
import jieba
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from psybot.models import Userinfo, Activityinfo, Speechinfo, Emotioninfo


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def calculate(request):
    formula = request.GET['formula']
    try:
        result = eval(formula, {})
    except:
        result = 'Error formula'
    return HttpResponse(result)


@csrf_exempt
def register(request):
    mopenid = request.GET['openid']
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
    result = {"code": code, "msg": "success", "data": []}
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


#根据效价判断是否需要干预
@csrf_exempt
def emotionevaluate(request):
    mefficient = request.GET['efficient']
    if int(mefficient) < 4:
        code = '1'    #需要干预
    else:
        code = '0'    #不需要干预
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))


#文本分类
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

    mfile = 'E:\\study\\program\\Psybot\\data.json'
    data = loadfile(mfile)

    l0 = 13
    l1 = 13
    l2 = 13
    l3 = 13
    l4 = 13
    l5 = 13
    l6 = 13
    l7 = 13

    def tokenizer(text):
        stopwords_file = "E:\\study\\data\\停用词表stopwords\\哈工大停用词表.txt"
        stop_f = open(stopwords_file, "r", encoding='utf-8')
        stop_words = []
        for line in stop_f.readlines():
            line = line.strip()
            if not len(line):
                continue
            stop_words.append(line)
        stop_f.close
        # print("length of stop_words:",len(stop_words))

        return_list = []
        for each in text:
            outstr = ''
            seg_list = jieba.cut(each, HMM=False)
            for word in seg_list:
                if word not in stop_words:
                    return_list.append(word)
        #                 if word != '\t':
        #                     outstr += word
        #                     outstr += " "
        #         #seg_list = " ".join(seg_list)
        #         #print(outstr.strip())
        #         return_list.append(outstr.strip())
        return return_list

    def fileextraction(data):
        # 存储对应label的邮件的words分布
        label0dict = {}
        label1dict = {}
        label2dict = {}
        label3dict = {}
        label4dict = {}
        label5dict = {}
        label6dict = {}
        label7dict = {}

        for i in range(len(data)):
            temp = tokenizer(data[i])
            textset = set(temp)
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
        return [label0dict, label1dict, label2dict, label3dict, label4dict, label5dict, label6dict, label7dict]

    labeldict = fileextraction(data)

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
        # print(email)
        # 采用1-Laplace变换
        # 取对数来避免下溢的问题
        seg_list = jieba.cut(text, HMM=False)
        for word in seg_list:
            if word in labeldict[0].keys():
                # if returnlist[1][email[i]] < 1500 and email[i] in returnlist[3] and returnlist[3][email[i]] < 1500:
                # print(returnlist[1][email[i]])
                # if word in labeldict.keys():
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

        #         plabel0 = -p1
        #         plabel1 = -p3
        #         #print(plabel0, plabel1)
        #         if plabel0 > plabel1 and email[0] != '0':
        #             miss += 1
        #         elif plabel0 < plabel1 and email[0] != '1':
        #             miss += 1
        # print(p0,p1,p2,p3,p4,p5,p6)
        # pi = [0,1,2,3,4,5,6,7]
        a = {"0": p0, "1": p1, "2": p2, "3": p3, "4": p4, "5": p5, "6": p6, "7": p7}
        return sort_by_value(a)

    text = request.GET['text']
    result = {"code": 0, "msg": "success", "data": predicttext(text)}
    return HttpResponse(json.dumps(result))


#建立用户本次交流的情绪信息表
@csrf_exempt
def setemotion(request):
    mopenid = request.GET['openid']
    mefficient = request.GET['efficient']
    mawake = request.GET['awake']
    mbelief = request.GET['belief']
    mcontent = request.GET['content']
    muser = Userinfo.objects.get(openid=mopenid)
    memotioninfo = Emotioninfo(user=muser, awake=mawake, belief=mbelief, content=mcontent, efficient=mefficient)
    memotioninfo.save()
    print("情绪信息存储成功")
    code = '0'
    result = {"code": code, "msg": "success", "data": []}
    return HttpResponse(json.dumps(result))

