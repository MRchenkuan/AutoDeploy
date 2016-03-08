#coding:utf-8
from fabric.colors import *
from fabric.operations import *
from AutoDeployment.tools import getDigit
class AppDeploy():
    '''    V1.5:app部署类，完成app的安装、卸载、更新、强制更新等操作。'''
    
    def __init__(self, getConfPath, rulesPath, appList):
        self.getConfPath = getConfPath
        self.rulesPath = rulesPath 
        self.appList = appList 
        
    def _appOperate(self, ip, app, operate):
        if operate.upper() == 'I':
            operate = 'install'
        elif operate.upper() == 'D':
            operate = 'remove'
        elif operate.upper() == 'U':
            operate = 'update'
        elif operate.upper() == 'F':
            operate = 'reinstall'
        else:
            print red("_appOperate出现未知错误，请检查！")
        with settings(host_string=ip):
            try:
                run('yum -y %s %s'%(operate, app))
            except:
                print red("xxxxxxxx远程命令执行错误，请检查！xxxxxxxx\n\n")

    
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
            print "请选择要操作的【程序】！"
            slct = getDigit(appCount)
            app = self.appList[slct-1]
            print "当前选择的程序为：%s" % app
            # 选择操作
            while True:
                appOpt = raw_input("请选择操作：安装【I】，卸载【D】，更新【U】，强制更新【F】，重新选择【P】")
                rules = self.getConfPath(self.rulesPath, app)
                if appOpt.upper() in ['I', 'D', 'U', 'F']:
                    for rule in rules:
                        self._appOperate(rule[1], app, appOpt)
                elif appOpt.upper() == 'P':
                    opt = 'P'
                else:
                    print red("输入错误，请重新选择操作！")
                    continue
                # 操作完成，跳出操作选择
                break
            if opt == 'P':
                continue
            print "操作完成：继续【部署程序】请按1，返回【主页】请按其余数字。"
            nextOpt = getDigit()
            if nextOpt == 1:
                continue
            else:
                break 
    
    def _appBat_Sub(self, appSubList):
        # 选择操作
        appOpt = raw_input("请选择操作：安装【I】，卸载【D】，更新【U】，强制更新【F】")
        if appOpt.upper() not in ['I', 'D', 'U', 'F']:
            print red("输入错误，终止本次操作！")
            return 1
        for app in appSubList:
            print "######当前操作的程序为：%s######" % app
            while True:
                rules = self.getConfPath(self.rulesPath, app)
                for rule in rules:
                    self._appOperate(rule[1], app, appOpt)
                # 操作完成，跳出操作选择
                break
            
    def _appBat(self):
        # app分类
        webList = [] 
        serviceList = [] 
        gatewayList = []
        for app in self.appList:
            if "-web-" in app:
                webList.append(app)
            elif "-service-" in app:
                serviceList.append(app)
            elif "-gateway-" in app:
                gatewayList.append(app)
            else:
                print "未知程序类型，请检查：%s" % app
                
        print "请选择操作项！"
        print "--------------------"
        print "1.批量部署所有WEB应用"
        print "2.批量部署所有Service"
        print "3.批量部署所有Gateway"
        print "0.批量部署所有应用"
        print "--------------------"
        slct = getDigit([0,1,2,3])
        if slct == 1:
            self._appBat_Sub(webList) 
        elif slct == 2:
            self._appBat_Sub(serviceList) 
        elif slct == 3:
            self._appBat_Sub(gatewayList) 
        elif slct == 0:
            self._appBat_Sub(self.appList) 
        else:
            print red("未知错误，请检查！")  
    
    def main(self):
#         local("clear")
#         print AppControl.__doc__
        while True:
            print "请选择操作项！"
            print "--------------------"
            print "1. 部署单个程序"
            print "2. 批量部署程序"
            print "0. 退出"
            print "--------------------"

            slct = getDigit([0, 1, 2])
            if (slct == 0):
                print "输入%d,选择【退出】"%slct
                break 
            elif (slct == 1):
                print "输入%d,选择【部署单个程序】"%slct
                self._appSingle()
            elif (slct == 2):
                print "输入%d,选择：【批量部署程序】"%slct
                self._appBat()
            else:
                print red("xxxxxxxx出现未知错误，请检查！xxxxxxxx")
                break 
            
#             local("clear")
            print "已返回到启动【主页】"  
            
    def tomcat(self):
        opt = raw_input("请选择操作：安装【install】，卸载【remove】")
        if opt.lower() == "install":
            opt = "install"
            optInfo = "安装"
        elif opt.lower() == "remove":
            opt = "remove"
            optInfo = "卸载"
        else:
            print "输入错误，退出程序"
            return 0
        print "你选择的是给所有WEB服务器【%s】TOMCAT"%optInfo
        sure = raw_input("请再次确认：确认【Y】取消【任意键】")
        if sure.upper() == "Y":
            pass
        else:
            return 0
        print "开始给所有WEB服务器【%s】TOMCAT。。。"%optInfo
        for app in self.appList:
            rules = self.getConfPath(self.rulesPath, app)
            for rule in rules:
                with settings(host_string=rule[1]):
                    try:
                        run('yum -y %s %s'%(opt, app))
                    except:
                        print red("xxxxxxxx远程命令执行错误，请检查！xxxxxxxx\n\n")
                            
                            
                            