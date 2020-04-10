# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pypinyin import pinyin, lazy_pinyin,load_phrases_dict
import pypinyin
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DuoYinDict(object):
	def __init__(self,dict_file):
		dy_dict=creat_dict(dict_file)		
		load_phrases_dict(dy_dict)


def creat_dict(dict_file):
	with open(dict_file,'r')as f1:
	 	py_dict = {}
		for line in f1.readlines():
			l = line.strip().split(' ')
			key = l[0]
			py = l[1:]
			py = np.reshape(py,[-1,1])
			py = py.tolist()
			py_dict[key] = py

	return py_dict



if __name__=="__main__":
	
	DuoYinDict('units/revise_dict.txt')
	
	words = '调大'
	unicode_txt =words# unicode(txt,"utf-8").replace(' ','')
	py_shengmu = pinyin(unicode_txt,style=pypinyin.TONE3)
	print py_shengmu
	py_shengmu = pinyin(unicode_txt, style=pypinyin.INITIALS,strict=False)
	print py_shengmu
	py_yunmu = pinyin(unicode_txt, style=pypinyin.FINALS)
	print py_yunmu
