import jieba
from psybot.utils.Const import *

#加载文件
def loadfile(file):
    f = open(file, "r", encoding='utf-8')
    words = []
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        words.append(line)
    f.close()
    return words

#中文分词
def tokenizer(text):
    stop_words = loadfile(stopwords_file)

    return_list = []
    for each in text:
        outstr = ''
        seg_list = jieba.cut(each, HMM=False)
        for word in seg_list:
            if word not in stop_words:
                #return_list.append(word)
                if word != '\t':
                    outstr += word
                    outstr += " "
            #seg_list = " ".join(seg_list)
        #print("outstr:", outstr.split())
        return_list.append(outstr.split())
    return return_list

