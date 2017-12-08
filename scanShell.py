#!/usr/bin/env python
#coding=utf8

import os, glob, sys
import time
from filterShell import FilterShell
from getFileTime import getFileTime

#插件列表
plusArr = [] 

#加载插件
def loadPlus(ext="all"):
	plusTmp = glob.glob('plugins/*-plugin.py')
	if ext == "all":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
    			__import__("plugins." + plusname)
			plusArr.append(plusname)
	elif ext == "php":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("php") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	elif ext == "asp":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("aps") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	elif ext == "aspx":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("apsx") == 0:
				__import__("plugins." + plusname)
				plusArr.append( plusname)
	elif ext == "jsp":
		for plus in plusTmp:
			plusname = plus.split('/')[-1][:-3]
			if plusname.find("jps") == 0:
				__import__("plugins." + plusname)
				plusArr.append(plusname)
	else:
		print "error args!"
		exit()

#通过加载插件扫描
def scan(fileCtent, ext):
    loadPlus(ext)
	#获取绝对路径
    for plus in plusArr:
        res = sys.modules["plugins." + plus].judgeBackdoor(fileCtent)
        if res:
            return res
            break
        else:
            pass
