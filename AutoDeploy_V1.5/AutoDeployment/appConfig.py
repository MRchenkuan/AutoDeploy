#coding:utf-8
from fabric.colors import *
from fabric.operations import *
from AutoDeployment.tools import getDigit
from AutoUploadConf.PropertiesClass import Properties

class AppConfig():
    '''V1.5:app配置类，完成app的配置、更新等操作。'''
    
    def __init__(self, getConfPath, rulesPath, appList, templatePath):
        self.getConfPath = getConfPath
        self.rulesPath = rulesPath 
        self.appList = appList 
        self.templatePath = templatePath
    
    
    def _appOperate(self, app, ip, port, templatePath, toPath, instId):
        with settings(host_string=ip):
            prop = Properties(templatePath)
    
            prop.set("sys.home", "../../logs")
            prop.set("sys.runmode", "develop")
            prop.set("sys.encoding", "UTF-8")
            prop.set("application.name", "%s" % app.upper())
            prop.set("server.name", "%s" % app)
            prop.set("instance.id", "%s_%s" % (app.upper(), instId))
            prop.set("log.level", "DEBUG")
            prop.set("log.limits_lines", "20")

            prop.set("redis.host", "182.92.170.189")
            prop.set("memcache.server", "182.92.170.189:11211")
            print "###%s###"%port
            prop.set("dubbo.port", "%s" % port)
            prop.set("dubbo.host", ip)
            prop.set("dubbo.registry", "zookeeper://182.92.170.189:2181")
            if "web" in app.lower():
                prop.set("dubbo.name", "%s-consumer" % app)
                prop.set("mesrvAddr", "")
            else:    
                prop.set("dubbo.name", "%s-provider" % app)
                prop.set("mesrvAddr", "182.92.170.189:9876")
            prop.close()
    
            # 上传到目的路径
            run('mkdir -p %s' % toPath)
            put(templatePath, toPath + 'server.properties')
            
    def _appSingle(self):
        print "程序列表："
        print "--------------------"
        i = 1
        for app in self.appList:
            print "%d. %s"%(i, app)
            i += 1 
        # 程序编号
        appCount = range(1, i)
        while True:
            opt = None
            # 选择程序
            print "请选择要配置的【程序】！"
            slct = getDigit(appCount)
            app = self.appList[slct-1]
            print "当前选择的程序为：%s，开始配置..." % app
            rules = self.getConfPath(self.rulesPath, app)
            for rule in rules:
                instId = rule[0]
                ip = rule[1]
                port = rule[2]
                toPath = rule[3] + app + '/conf/'
                self._appOperate(app, ip, port, self.templatePath, toPath, instId)

            print "操作完成：继续【部署程序】请按1，返回【主页】请按其余数字。"
            nextOpt = getDigit()
            if nextOpt == 1:
                continue
            else:
                break  
    
    def _appBat(self):
        pass 
            
    def main(self):
        while True:
            print "请选择操作项！"
            print "--------------------"
            print "1. 配置单个程序"
            print "2. 批量配置程序"
            print "0. 退出"
            print "--------------------"

            slct = getDigit([0, 1, 2])
            if (slct == 0):
                print "输入%d,选择【退出】"%slct
                break 
            elif (slct == 1):
                print "输入%d,选择【配置单个程序】"%slct
                self._appSingle()
            elif (slct == 2):
                print "输入%d,选择：【批量配置程序】"%slct
                self._appBat()
            else:
                print red("xxxxxxxx出现未知错误，请检查！xxxxxxxx")
                break 
            
#             local("clear")
            print "已返回到启动【主页】"  
            
