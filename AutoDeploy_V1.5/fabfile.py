# coding:utf-8
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.colors import *

from AutoDeployment.tools import *
from AutoDeployment.MapRuleParserClass import MapRuleParser
from AutoDeployment.MapRuleParserClass import getConfPath
from AutoUploadConf.PropertiesClass import Properties
# V1.5版本
from AutoDeployment.appControl import AppControl
from AutoDeployment.appDeploy import AppDeploy 
from AutoDeployment.appConfig import AppConfig

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
env.user = 'root'
env.password = 'xxxxxxxx'
env.hosts = []

# 默认app配置单
applist = ['gigold-gateway-alipay', 
            'gigold-gateway-cardpos', 
            'gigold-gateway-htfFund', 
            'gigold-gateway-pospBusiness', 
            'gigold-gateway-pospManage', 
            'gigold-gateway-smsBC', 
            'gigold-gateway-trade', 
            'gigold-gateway-unionpay', 
            'gigold-gateway-weixin', 
            'gigold-service-account', 
            'gigold-service-billCenter', 
            'gigold-service-cardpos', 
            'gigold-service-cashier', 
            'gigold-service-chargeUp', 
            'gigold-service-customer', 
            'gigold-service-dispatchingCenter', 
            'gigold-service-fdc', 
            'gigold-service-fdcBatch', 
            'gigold-service-foundation', 
            'gigold-service-foundationBatch', 
            'gigold-service-fundBatch', 
            'gigold-service-industrypay', 
            'gigold-service-merchant', 
            'gigold-service-posp', 
            'gigold-service-repeat', 
            'gigold-service-runManager', 
            'gigold-service-trade', 
            'gigold-web-batchMonitor', 
            'gigold-web-cashier', 
            'gigold-web-dispatchingCenter', 
            'gigold-web-fdc', 
            'gigold-web-foundation', 
            'gigold-web-htfFund', 
            'gigold-web-industrypay', 
            'gigold-web-runManager', 
            'gigold-web-trade', 
            'gigold-web-upload']

tomcatList = ['tomcat-gigold-web-batchMonitor',
            'tomcat-gigold-web-cashier',
            'tomcat-gigold-web-dispatchingCenter',
            'tomcat-gigold-web-fdc',
            'tomcat-gigold-web-foundation',
            'tomcat-gigold-web-htfFund',
            'tomcat-gigold-web-industrypay',
            'tomcat-gigold-web-runManager',
            'tomcat-gigold-web-trade',
            'tomcat-gigold-web-upload']

######################
# 安装、卸载TOMCAT程序 #
######################
def tomcatDep():
    '''V1.5:WEB项目第一次部署时必须安装TOMCT'''
    local("clear")
    print tomcatDep.__doc__
    appObj = AppDeploy(getConfPath, rulesPath, tomcatList)
    appObj.tomcat()
    
######################
# 启动、停止、重启程序 #
######################
def appCtl():
    '''V1.5:程序控制入口:可【运行，停止，重启】程序'''
    local("clear")
    print appCtl.__doc__
    appObj = AppControl(getConfPath, rulesPath, applist)
    appObj.main()
    

######################
# 安装、卸载、更新、强制更新程序 #
######################
def appDep():
    '''V1.5:程序部署入口:可【安装、卸载、更新、强制更新】程序'''
    local("clear")
    print appDep.__doc__
    appObj = AppDeploy(getConfPath, rulesPath, applist)
    appObj.main() 
    
######################
# 配置文件 #
######################
def appConf():
    '''V1.5:程序配置入口:可配置【单个、批量、所有】程序'''
    local("clear")
    print appConf.__doc__
    # 配置文件模板路径
    templatePath = "./AutoUploadConf/model/server.properties.template"
    appObj = AppConfig(getConfPath, rulesPath, applist, templatePath)
    appObj.main() 



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
    i = 1
    for app in applist:
        print "%s. %s" % (i, app)
        i += 1
    print "9. 全部"
    print "0. 退出"
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
    print "---------------------"
    print "请选择要备份还原的内容:"
    print ""
    print "1. ↓↓ 备份所有机器的 应用 配置文件"
    print "2. ↑↑ 还原所有机器的 应用 配置文件"
    print "3. ↓↓ 备份所有机器的 Tomcat 配置文件"
    print "4. ↑↑ 还原所有机器的 Tomcat 配置文件"
    print "0. 退出"
    print ""
    print "---------------------"
    while True:
        # try:
        slct = int(input("需要备份的内容: "))
        if (slct == 0):
            print "已选择：退出"
            return True
        if (slct == 1):
            conf_bak()
            break
        if (slct == 2):
            local("cd ./confBak/ && ls conf*.tar")
            print ""
            tar_name = raw_input("请输入需要还原的tar包全名: ")
            conf_rst(tar_name)
            break
        if (slct == 3):
            tomcat_xml_bak()
            break
        if (slct == 4):
            local("cd ./confBak/ && ls tom*.tar")
            print ""
            tar_name = raw_input("请输入需要还原的tar包全名: ")
            tomcat_xml_rst(tar_name)
            break
        else:
            print "找不到选项:%s" % slct
            # except:
            #     print"选择类型错误,请输入有效选项..."
            #     continue


######################
# 应用配置文件的备份部分#
######################
def conf_bak():
    print blue("开始备份所有配置文件...")
    for app in applist:
        instList = getConfPath(rulesPath, app)
        for inst in instList:
            inst_no = inst[0]
            ip = inst[1]
            port = inst[2]
            rmtPath = inst[3] + '../conf/*'
            with settings(host_string=ip):
                localPath = "%s/apps/%s/conf-%s-%s-%s" % (confBakPath, app, app, inst_no, port)
                local("mkdir -p %s" % localPath)
                get(rmtPath, localPath)
    backTarName = 'confs-' + time.strftime('%Y%m%d%H%m%S', time.localtime(time.time()))
    local("cd %s&&tar -rf %s.tar ./apps/* && rm -rf ./apps" % (confBakPath, backTarName))
    print blue("备份完毕：\n %s.tar 保存在：%s 中" % (backTarName, confBakPath))


######################
# 应用配置文件的还原部分#
######################
def conf_rst(tar_name):
    if os.path.exists("/data/oper/confBak/%s" % tar_name):
        print blue(">>>>解包配置文件...")
        local("cd /data/oper/confBak && rm -rf apps && tar -xvf %s" % tar_name)
        for app in applist:
            instList = getConfPath(rulesPath, app)
            for inst in instList:
                inst_no = inst[0]
                ip = inst[1]
                port = inst[2]
                rmtPath = inst[3] + '../conf/'
                with settings(host_string=ip):
                    localPath = "%s/apps/%s/" % (confBakPath, app)
                    local_folder_name = "conf-%s-%s-%s" % (app, inst_no, port)
                    # 个性化各台机器配置 - 可选
                    mod_sigle_inst(app, ip, port, localPath + local_folder_name, "server.properties", inst_no)
                    mod_sigle_inst(app, ip, port, localPath + local_folder_name, "system.properties", inst_no)
                    # 建立远程路径
                    run("mkdir -p %s" % inst[3])
                    run("cd %s../ && mkdir -p ./conf/" % (inst[3]))
                    put(localPath + local_folder_name + "/*", rmtPath)
        local("cd /data/oper/confBak && rm -rf apps")
        print blue("还原完毕!")
    else:
        print "并没有找到包 %s" % tar_name


##########################
# tomecat配置文件的备份部分 #
##########################
def tomcat_xml_bak():
    print blue("开始备份所有配置文件...")
    for app in applist:
        instList = getConfPath(rulesPath, app)
        for inst in instList:
            inst_no = inst[0]
            ip = inst[1]
            port = inst[2]
            rmtPath = inst[3] + '../tomcat/conf/server.xml'
            with settings(host_string=ip):
                localPath = "%s/tomcats/%s/" % (confBakPath, app)
                local_name = "server.xml-%s-%s-%s" % (app, inst_no, port)
                local("mkdir -p %s" % localPath)
                get(rmtPath, localPath + local_name)
    backTarName = 'tomcs-' + time.strftime('%Y%m%d%H%m%S', time.localtime(time.time()))
    local("cd %s&&tar -rf %s.tar ./tomcats/* && rm -rf ./tomcats" % (confBakPath, backTarName))
    print blue("备份完毕：\n %s.tar 保存在：%s 中" % (backTarName, confBakPath))


def tomcat_xml_rst(tar_name):
    if os.path.exists("/data/oper/confBak/%s" % tar_name):
        print blue(">>>>解包配置文件...")
        local("cd /data/oper/confBak && rm -rf tomcats && tar -xvf %s" % tar_name)
        for app in applist:
            instList = getConfPath(rulesPath, app)
            for inst in instList:
                inst_no = inst[0]
                ip = inst[1]
                port = inst[2]
                rmtPath = inst[3] + '../tomcat/conf/'
                with settings(host_string=ip):
                    localPath = "%s/tomcats/%s/" % (confBakPath, app)
                    local_name = "server.xml-%s-%s-%s" % (app, inst_no, port)
                    # 建立远程路径
                    run("mkdir -p %s" % inst[3])
                    run("cd %s../ && mkdir -p ./tomcat/conf/" % (inst[3]))
                    put(localPath + local_name, rmtPath + "server.xml")
        local("cd /data/oper/confBak && rm -rf tomcats")
        print blue("还原完毕!")
    else:
        print "并没有找到包 %s" % tar_name


##############
# 手动上传部分 #
##############
def upto(fr, ip, to):
    with settings(host_string=ip):
        put(fr, to)


####################
# 配置文件按模板的上传部分 #
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

        if fName == "system.properties":
            prop.set("sys.home", "/data/%s/" % app)
            prop.set("sys.runmode", "product")
            prop.set("sys.encoding", "UTF-8")
            prop.set("server.name", "%s" % app.upper())
            prop.set("application.name", "USRAPP")
            prop.set("instance.id", "%s_%s" % (app.upper(), instId))
            prop.set("log.level", "DEBUG")
            prop.set("log.limits_lines", "20")
            prop.close()
        if fName == "server.properties":
            prop.set("server.port", "%s" % port)
            prop.set("dubbo.host", ip)
            prop.set("dubbo.name", "%s-provider" % app)
            prop.close()

        # 上传到目的路径
        run('mkdir -p %s' % toPath)
        put(fromPath + fName, toPath)


def mod_sigle_inst(app, ip, port, fromPath, fName, instId):
    # 修改文件
    prop = Properties(fromPath +"/"+ fName)

    if fName == "system.properties":
        # prop.set("sys.home", "/data/%s/" % app)
        prop.set("sys.runmode", "product")  # ?????????????????????
        # prop.set("sys.encoding", "UTF-8")
        # prop.set("server.name", "%s" % app) #小写应用名
        # prop.set("application.name", "%s" %app.upper()) # 大写应用名
        prop.set("instance.id", "%s_%s" % (app.upper(), instId))
        prop.set("log.level", "DEBUG")  # ?????????????????????
        # prop.set("log.limits_lines", "20")
        prop.close()
    if fName == "server.properties":
        prop.set("server.port", "%s" % port)
        prop.set("dubbo.host", ip)
        prop.set("memcache.server", "10.10.1.11:11211")  # ?????????????????????
        prop.set("dubbo.registry", "zookeeper://10.10.1.11:2181")  # ?????????????????????
        # prop.set("dubbo.name", "%s-provider" % app)
        prop.close()


#######################
# 服务器tomcat 启停部分 #
#######################
def rest():
    local("clear")
    print "--------------------"
    print "请选择要重启的应用:"
    i = 1
    for app in applist:
        print "%s. %s" % (i, app)
        i += 1
    print "9. 全部"
    print "0. 退出"
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
                print "..."
                time.sleep(1)
                print "怎么能启全部,万一卡了呢?"
                time.sleep(1)
                return True
            print "已选择重启：" + applist[int(slct) - 1]
            print red("关闭 %s 服务中..." % applist[int(slct) - 1])
            stopAllHostOf(applist[int(slct) - 1])
            print green("启动 %s 服务中..." % applist[int(slct) - 1])
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
