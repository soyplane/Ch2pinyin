# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pypinyin import pinyin, lazy_pinyin,load_phrases_dict
import pypinyin
from revise_dict import DuoYinDict
import re
#init dictinary_char_to_labelictinary
import dictinary_no_tone
import sys

sys.setdefaultencoding('utf-8')


#################################################################################
# pypinyin 版本为0.35.1,对于一些错的音的标注，需要自定义词典来解决,DuoYinDict模块
#################################################################################
DuoYinDict('revise_dict.txt')
units_file = 'units.txt'
units_no_tone_file = 'units_no_tone_deploy.txt'


dictinary_char_to_label,dictinary_label_to_char = dictinary_no_tone.init_dictinary(units_no_tone_file)
w = open("keep12.txt","w")


def oov(tem_shenmu,tem_yunmu,dic,py_shenmu,py_yunmu,txt):
    shenmu = tem_shenmu
    yunmu = tem_yunmu
    if shenmu not in dic:
        shenmu = 'oov'
    if yunmu not in dic:
        yunmu = 'oov'
    if yunmu == 'oov' or shenmu == 'oov':
        print txt
        print py_shenmu
        print py_yunmu
        print tem_shenmu
        print tem_yunmu
        w.write(txt)
        w.write('\n')
        w.write(str(py_shenmu)+'\n')
        w.write(str(py_yunmu)+'\n')
    return shenmu,yunmu


def change_yunmu(yunmu):
    if yunmu[-1] != '1' and yunmu[-1] != '2' and yunmu[-1] != '3' and yunmu[-1] != '4':
        yunmu = yunmu+'0'

    return yunmu


def get_pinyin_label(txt):
    #txt.decode('utf-8')
    char = re.sub(r'\*\*','',txt)
    char = re.sub(r'\*','',char)
    char = re.sub(r'<FIL/>','',char)
    char = re.sub(r'<NON/>','',char)
    char = re.sub(r'<NPS/>','',char)
    char = re.sub(r'<SPK/>','',char)
    char = re.sub(r'<STA/>','',char)
    char = re.sub(r'<UNK>','',char)
    char = re.sub(r'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]', '',char)
    char = re.sub(r'   ','',char)
    char = re.sub(r'  ','',char)
    txt = re.sub(r' ','',char)

#    print txt
    #unicode_txt = unicode(txt,"utf-8").replace(' ','')
    unicode_txt = txt.replace(' ','')
#    shengyunmu = pinyin(unicode_txt,style=pypinyin.TONE3)
#    print shengyunmu
    py_shenmu = pinyin(unicode_txt, style=pypinyin.INITIALS)
   # print py_shenmu
    #py_yunmu = pinyin(unicode_txt, style=pypinyin.FINALS_TONE3,strict=False)
    py_yunmu = pinyin(unicode_txt, style=pypinyin.FINALS_TONE3)
    py_yunmu = pinyin(unicode_txt, style=pypinyin.FINALS)
   # print py_yunmu
    labels =[]
    length = len(py_shenmu)
    for i in range(length):
        #mean are normal pinyin
        #py_yunmu[i][0] = change_yunmu(py_yunmu[i][0])
        #tmp_ = change_yunmu(py_yunmu[i][0])
        #py_yunmu[i][0] = tmp_[0:-1] 
        #print py_yunmu[i][0]
        if py_shenmu[i][0] != "":
            if py_shenmu[i][0] in dictinary_char_to_label and py_yunmu[i][0] in dictinary_char_to_label:
                labels = labels + [dictinary_char_to_label[py_shenmu[i][0]]] + [dictinary_char_to_label[py_yunmu[i][0]]]

            else: #oov record
                tem_shenmu = py_shenmu[i][0]
                tem_yunmu = py_yunmu[i][0]
                tem_shenmu,tem_yunmu = oov(tem_shenmu,tem_yunmu,dictinary_char_to_label,py_shenmu,py_yunmu,txt)
                labels = labels + [dictinary_char_to_label[tem_shenmu]] + [dictinary_char_to_label[tem_yunmu]]

        else:
                #pdb.set_trace()
            if py_yunmu[i][0] in dictinary_char_to_label:
                tem_shenmu = py_yunmu[i][0][0] + py_yunmu[i][0][0]
                tem_shenmu,tem_yunmu = oov(tem_shenmu,py_yunmu[i][0],dictinary_char_to_label,py_shenmu,py_yunmu,txt)
                #add labels
                labels = labels + [dictinary_char_to_label[tem_shenmu]] + [dictinary_char_to_label[tem_yunmu]]

            elif py_yunmu[i][0][0] == "i" or py_yunmu[i][0][0] == "u":
                tem_shenmu = py_yunmu[i][0][0] + py_yunmu[i][0][0]
                tem_yunmu = py_yunmu[i][0][1:]
                tem_shenmu,tem_yunmu = oov(tem_shenmu,tem_yunmu,dictinary_char_to_label,py_shenmu,py_yunmu,txt)
                #add labels
                labels = labels + [dictinary_char_to_label[tem_shenmu]] + [dictinary_char_to_label[tem_yunmu]]

            elif py_yunmu[i][0][:-1] == "n":
                tem_shenmu = "ee"
                tem_yunmu = "en"+py_yunmu[i][0][-1]
                #add labels
                labels = labels + [dictinary_char_to_label[tem_shenmu]] + [dictinary_char_to_label[tem_yunmu]]

            else:
                print "fuck!"
                tem_shenmu,tem_yunmu = oov(py_shenmu[i][0],py_yunmu[i][0],dictinary_char_to_label,py_shenmu,py_yunmu,txt)
                #add labels
                labels = labels + [dictinary_char_to_label[tem_shenmu]] + [dictinary_char_to_label[tem_yunmu]]

    return labels


def id_to_char(id_list):
    char_list = []
    i = 0
    for index,item in enumerate(id_list):
        if index==0 and item>0:
            char_list.append(dictinary_label_to_char[item])
            if item>0 :
                i = i + 1
            else:
                char_list.append(' ')
        else:
            if item>0 :
               if item > 0:
                   char_list.append(dictinary_label_to_char[item])
                   i = i + 1
                   if i%2 == 0:
                       char_list.append(' ')
               else:
                   char_list.append(' ')
                   char_list.append(dictinary_label_to_char[item])
                   char_list.append(' ')

    return ' '.join(char_list).replace('   ',' ')


def id_to_char_2d(id_list_2d):
        char_list=[]
        for id_list in id_list_2d:
                char_list.append(id_to_char(id_list))
        return char_list


if __name__=="__main__":
    with open('vocab.txt','r') as f:
        for line in f.readlines():
            print "txt: ",line.strip()
            a = line.strip()
            ids = get_pinyin_label(a)
            print ids
            print "id_to_char(ids):"
            print id_to_char(ids)
