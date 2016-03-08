# coding:utf-8
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.colors import *
import time

# add by dengqy
def getDigit(params=None):
    '''
    作用：从键盘获取一个数字，并做规范性检查
    参数：params列表或元组，为可选，如果给出，则输入的数字必须在params内。
    '''
    while True:
        num_str = raw_input("请输入一个有效数字：")
        if num_str.isdigit():
            num_int = int(num_str)
            if isinstance(params, (tuple, list)) and len(params) > 0:
                if num_int in params:
                    break
                else:
                    print red("输入的不是一个有效选项！")
            else:
                break
        else:
            print red("输入的不是一个数字！")
    return num_int 
    
# add by liuzhiguo
# 等待服务端口开启
def waitPortStart(hostPort):
    pidN = run("lsof -i:%s | awk {'print $2'} | tail -n 1" % hostPort)
    if (not isProtExist(hostPort)):
        while pidN.strip() is '':
            print blue('waiting for tomcat server up...')
            time.sleep(1)
            pidN = run("lsof -i:%s | awk {'print $2'} | tail -n 1" % hostPort)
    print blue('finished!........!tomcat已启动，PID：%s' % pidN)


# add by liuzhiguo
# 判断端口是否开启
def isProtExist(hostPort):
    pidN = run("lsof -i:%s | awk {'print $2'} | tail -n 1" % hostPort)
    print hostPort
    if pidN.strip() is '':
        return False
    else:
        return True


# add by liuzhiguo
# 停止应用
def shutdownTomcat(hostPort, hostPath, workPath):
    pidN = run("lsof -i:%s | awk {'print $2'} | tail -n 1" % hostPort)
    if (isProtExist(hostPort)):
        run('sh %s/bin/shutdown.sh' % workPath)
        print blue('正在尝试关闭tomecat...')
        print 'sleep 3'
        time.sleep(1)
        print 'sleep 2'
        time.sleep(1)
        print 'sleep 1...'
        time.sleep(1)
        print 'sleep checking...'

        if (isProtExist(hostPort)):
            print red('关闭失败...强行停止...')
            run('kill -9 %s' % pidN)
            time.sleep(3)
        else:
            print blue('tomcat服务已经被关闭')
    try:
        print red('kill -9 %s' % pidN)
        run('kill -9 %s' % pidN)
    except:
        print 'pidn:%s is not exist' % pidN


# add by liuzhiguo
# 启动应用
def startupTomcat(hostPort, hostPath, workPath):
    if (not isProtExist(hostPort)):
        print red("删除缓存文件...")
        run('rm -rf %s/work/*' % workPath)
        run('set -m; sh %s/bin/startup.sh' % workPath)
        waitPortStart(hostPort)
