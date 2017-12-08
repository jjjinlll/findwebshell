#!/usr/bin/env python
#coding=utf8

import glob, os
from optparse import OptionParser
from filterShell import FilterShell
from getFileTime import getFileTime
from scanShell import *
from createHtml import createHtml

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path",
        help="input web directory filepath", metavar="PATH")
    parser.add_option("-o", "--output", dest="output",
        help="create a html report")
    parser.add_option("-e", "--ext", dest="ext",
        help="define what's file format to scan", metavar="php|asp|aspx|jsp|all")

    (options, args) = parser.parse_args()

    #黑名单列表
    #名字字典
    fileList = {}
    #结果列表
    resList =  []

    #检测是否输入合法的路径和要扫描的类型
    if options.ext == None or options.path == None:
        parser.error("输入的参数不正确!")

    #获取文件绝对路径
    for root, dirs, files in os.walk(options.path):
        for filename in files:
            if filename[-4:]==('.'+options.ext):
                fullpath = os.path.join(root, filename)
                fileList[fullpath] = filename

    #过滤类
    FilterShell = FilterShell()

    #文件名过滤
    for fullpath in fileList.keys():
        filename = fileList.get(fullpath)
        res = FilterShell.filename(options.ext, filename)
        if res:
            #获取后门类型，文件修改时间，文件路径
            mtime = getFileTime(fullpath)
            filemode = "cheak by filename"
            resList.append([fullpath, filemode, mtime])
        else:
            if os.path.getsize(fullpath) < 500000:
                with open(fullpath, "rb") as fp:
                    ctent = fp.read()
                    filemode = FilterShell.content(options.ext, ctent)
                    #获取后门类型，文件修改时间，文件路径
                    if filemode:
                        mtime = getFileTime(fullpath)
                        resList.append([fullpath, filemode, mtime])
                    else:
                        resp=scan(ctent, options.ext)
                        if resp:
                            filetime = getFileTime(fullpath)
                            resList.append([fullpath, resp, filetime])
    #处理后门列表
    l = len(resList)
    if l:
        for i in xrange(l):
            resList[i][0] = os.path.abspath(resList[i][0])
            print resList[i]
