# coding:utf-8
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.colors import *

from AutoDeployment.tools import *
from AutoDeployment.MapRuleParserClass import MapRuleParser
from AutoDeployment.MapRuleParserClass import getConfPath
from AutoUploadConf.PropertiesClass import Properties

import time, os

# TomCatPath
orgPath = '/data/apache-tomcat-8.0.26'
workPath = '/tomcat/'

# resourcePath
resourcePath = '/data/Resource/'
confModPath = "./AutoUploadConf/model/"
confBakPath = "./confBak/"

# 部署规则表地址
rulesPath = './AutoDeployment/Mapping.ini'

# 解析文件
pathMap = MapRuleParser(rulesPath, resourcePath)

# 服务器账号
env.user = 'oper'
env.password = '123654'
env.hosts = []

# 默认app配置单
applist = ["foundation", "batch", "fund", "trade", "cashier", "repeat", "fdc", "runman"]


########
# 入口 #
########
def dep():
    local("clear")
    print "已有文件：-----------"
    local("ls /data/Resource/")
    print ""
    print "--------------------"
    print "请选择要部署的应用:"
    print "1.foundation"
    print "2.batch"
    print "3.fund"
    print "4.trade"
    print "5.cashier"
    print "6.repeat"
    print "7.fdc"
    print "8.runman"
    print "9.全部"
    print "0.退出"
    print ""
    print "---------------------"
    while True:
        try:
            slct = int(input("请选择要部署的应用: "))
            if (slct == 0):
                print "已选择：退出"
                return True
            if (slct == 9):
                print "已选择：部署全部"
                depAll()
                return True
            print "已选择部署：" + applist[int(slct) - 1]
            upload_allHost(applist[int(slct) - 1])
            break
        except:
            print"选择类型错误,请输入有效选项..."
            continue


def bak():
    local("clear")
    print "请选择要备份的内容:"
    print ""
    print "1.所有机器的配置文件"
    print "0.退出"
    print ""
    print "---------------------"
    while True:
        try:
            slct = int(input("需要备份的内容: "))
            if (slct == 0):
                print "已选择：退出"
                return True
            if (slct == 1):
                confBak()
                break
            else:
                print "找不到选项:%s" % slct
        except:
            print"选择类型错误,请输入有效选项..."
            continue


####################
# 配置文件的备份部分 #
####################
def confBak():
    print blue("开始备份所有配置文件...")
    confs = {}
    for app in applist:
        instList = getConfPath(rulesPath, app)
        for inst in instList:
            ip = inst[1]
            port = inst[2]
            rmtPath = inst[3] + '../conf/*'
            with settings(host_string=ip):
                localPath = "%s/confs/%s/conf-%s-%s" % (confBakPath, app, ip, port)
                local("mkdir -p %s" % localPath)
                get(rmtPath, localPath)
    backTarName = 'confs-' + time.strftime('%Y%m%d%H%m%S', time.localtime(time.time()))
    local("cd %s&&tar -rf %s.tar ./confs/* && rm -rf ./confs" % (confBakPath, backTarName))
    print blue("备份完毕：\n %s.tar 保存在：%s 中" % (backTarName, confBakPath))


##############
# 手动上传部分 #
##############
def upto(fr, ip, to):
    with settings(host_string=ip):
        put(fr, to)


####################
# 配置文件的上传部分 #
####################
def confAll(applist=applist):
    for app in applist:
        confByApp(app, "system.properties")
        confByApp(app, "server.properties")


def confByApp(app, fName):
    rules = getConfPath(rulesPath, app)
    # [('1', '10.10.1.9', 8080, '/data/foundation/ver/'), ('2', '10.10.1.8', 8080, '/data/foundation/ver/')]
    print rules
    for rule in rules:
        instId = rule[0]
        ip = rule[1]
        port = rule[2]
        toPath = rule[3] + '../conf/'
        confByInst(app, ip, port, confModPath, fName, toPath, instId)


def confByInst(app, ip, port, fromPath, fName, toPath, instId):
    with settings(host_string=ip):
        # 修改文件
        # fdsfsafafafdpas
        prop = Properties(fromPath + fName)

        if (fName == "system.properties"):
            prop.set("sys.home", "/data/%s/" % app)
            prop.set("sys.runmode", "product")
            prop.set("sys.encoding", "UTF-8")
            prop.set("server.name", "%s" % app.upper())
            prop.set("application.name", "USRAPP")
            prop.set("instance.id", "%s_%s" % (app.upper(), instId))
            prop.set("log.level", "DEBUG")
            prop.set("log.limits_lines", "20")
            prop.close()
        if (fName == "server.properties"):
            prop.set("server.port", "%s" % port)
            prop.set("dubbo.host", ip)
            prop.set("dubbo.name", "%s-provider" % app)
            prop.close()

        # 上传到目的路径
        run('mkdir -p %s' % toPath)
        put(fromPath + fName, toPath)


#######################
# 服务器tomcat 启停部分 #
#######################
def rest():
    local("clear")
    print "--------------------"
    print "请选择要重启的应用:"
    print "1.foundation"
    print "2.batch"
    print "3.fund"
    print "4.trade"
    print "5.cashier"
    print "6.repeat"
    print "7.fdc"
    print "8.runman"
    print "9.全部"
    print "0.退出"
    print ""
    print "---------------------"
    while True:
        try:
            slct = int(input("请选择要部署的应用: "))
            if (slct == 0):
                print "已选择：退出"
                return True
            if (slct == 9):
                print "已选择：重启全部"
                depAll()
                return True
            print "已选择重启：" + applist[int(slct) - 1]
            print red("关闭 %s 服务中..."%applist[int(slct) - 1])
            stopAllHostOf(applist[int(slct) - 1])
            print green("启动 %s 服务中..."%applist[int(slct) - 1])
            time.sleep(1)
            startAllHostOf(applist[int(slct) - 1])
            break
        except:
            print"选择类型错误,请输入有效选项..."
            continue

# 停止
def stopAll(applist=applist):
    for app in applist:
        stopAllHostOf(app)


def stopAllHostOf(app):
    targets = getConfPath(rulesPath, app)
    if (targets and len(targets) >= 0):
        for target in targets:
            stopSingleHost(target)


def stopSingleHost(target):
    try:
        index = target[0]
        hostIp = target[1]
        hostPort = target[2]
        hostPath = target[3]
    except Exception, e:
        print red('解析目标地址失败！')
        print red(target)
    # 切换上下文环境
    with settings(host_string=hostIp):
        try:
            shutdownTomcat(hostPort, hostPath, hostPath + '../' + workPath)
        except Exception, e:
            print e

# 启动
def startAll(applist=applist):
    for app in applist:
        startAllHostOf(app)


def startAllHostOf(app):
    targets = getConfPath(rulesPath, app)
    if (targets and len(targets) >= 0):
        for target in targets:
            startSingleHost(target)


def startSingleHost(target):
    try:
        index = target[0]
        hostIp = target[1]
        hostPort = target[2]
        hostPath = target[3]
    except Exception, e:
        print red('解析目标地址失败！')
        print red(target)
    # 切换上下文环境
    with settings(host_string=hostIp):
        try:
            startupTomcat(hostPort, hostPath, hostPath + '../' + workPath)
        except Exception, e:
            print e


################
# war包部署部分 #
###############
def depRunman():
    upload_allHost('runman')


def depFoundation():
    upload_allHost('foundation')


def depBatch():
    upload_allHost('batch')


def depTrade():
    upload_allHost('trade')


def depCashier():
    upload_allHost('cashier')


def depFund():
    upload_allHost('fund')


def depRepeat():
    upload_allHost('repeat')


def depFdc():
    upload_allHost('fdc')


def depAll():
    execute(depFoundation)
    execute(depBatch)
    execute(depTrade)
    execute(depCashier)
    execute(depFund)
    execute(depRepeat)
    execute(depRunman)
    execute(depFdc)


def upload_allHost(app):
    targets = pathMap.getTargetsOf(app)
    if (targets and len(targets) >= 0):
        warName = ''  # 源文件名
        for target in targets:
            upload_singleHost(target)
            warName = target[0]  # 获取源文件名
        # 删除包
        print "删除原始文件 x %s..." % warName
        local('rm -rf %s' % (resourcePath + warName))
        return True
    else:
        return False


def upload_singleHost(target):
    try:
        warname = target[0]
        hostIp = target[1]
        hostPort = target[2]
        hostPath = target[3]
    except Exception, e:
        print red('解析目标地址失败！')
        print red(target)

    print yellow('\n' + warname + 'is Begin!------->')
    # 切换上下文环境
    with settings(host_string=hostIp):
        print green('* -->%s:%s/%s' % (hostIp, hostPort, hostPath))
        try:
            shutdownTomcat(hostPort, hostPath, hostPath + '../' + workPath)
            # 删除解压文件
            run('rm -rf %s*' % hostPath)

            # 上传到目的路径
            run('mkdir -p %s' % hostPath)
            warnameVer = warname + '-' + time.strftime('%Y%m%d%H%m%S', time.localtime(time.time()))
            put(resourcePath + warname, hostPath + warname);

            # 拷贝到备份路径
            run('mkdir -p %s../backup' % hostPath)
            run('cd %s && cp ./%s ../backup/%s' % (hostPath, warname, warnameVer))
            # 启动tomecat
            startupTomcat(hostPort, hostPath, hostPath + '../' + workPath)
            print green("成功启动：%s : %s" % (hostIp, hostPort))
        except Exception, e:
            print e
    print green(warname + 'is Done!--------<')
