# coding:utf-8
import ConfigParser
import os, re
from fabric.colors import *


def getFiles(filePath, sourcePath):
    list = os.listdir(sourcePath)
    filelist = []
    for i in range(0, len(list)):
        path = os.path.join(sourcePath, list[i])
        if os.path.isfile(path):
            filelist.append((list[i], path))
    return filelist


# @filePath 映射表
# @warName 比较的文件名
def matchFile(filePath, warName):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(filePath)
        # 遍历正则
        sections = cf.sections()
        for section in sections:
            rex = cf.get(section, 'regx')
            if (re.search(rex, warName)):
                items = cf.items(section)
                hosts = []
                for item in items:
                    if (item[0][:5] == 'host_'):
                        hosts.append((warName,) + eval(item[1]))
                return (section, hosts)
            else:
                continue
    except Exception, e:
        print e
    return False


def initAddressInfo(filePath, sourcePath):
    packages = getFiles(filePath, sourcePath)
    infos = {}
    for package in packages:
        warName = package[0]
        pPath = package[1]
        hosts = matchFile(filePath, warName)
        if (hosts):
            infos[hosts[0]] = hosts[1]
        else:
            print yellow("警告：文件 <<%s>> 没有设置对应的部署规则" % package[0])
    return infos


class MapRuleParser():
    """docstring for MapruleParser"""

    def __init__(self, filePath, sourcePath):
        self.ruleListForJson = initAddressInfo(filePath, sourcePath)

    def getTargetsOf(self, warType):
        targets = []
        target = {}
        if (self.ruleListForJson.has_key(warType)):
            return self.ruleListForJson[warType]
        else:
            print yellow(u'警告:Resource 中并没有找到符合规则 %s 的war包 ' % warType)
            return False


# 获取配置文件目标地址的方法
def getConfPath(filePath, warType):
    cf = ConfigParser.ConfigParser()
    cf.read(filePath)
    items = cf.items(warType);
    hosts = []
    for item in items:
        if (item[0][:5] == 'host_'):
            hosts.append((item[0][5:],) + eval(item[1]))
    return hosts
