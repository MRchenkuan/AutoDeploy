#coding:utf-8
from fabric.colors import *
from fabric.operations import *
from AutoDeployment.tools import getDigit
class AppControl():
	'''	V1.5:app控制类，完成app的启动，停止，重启等操作。'''
	
	def __init__(self, getConfPath, rulesPath, appList):
		self.getConfPath = getConfPath
		self.rulesPath = rulesPath 
		self.appList = appList 
	

	def _start(self, ip, app):
		appPath = self._getAppPath(app) 
		print "%s start"%appPath
		with settings(host_string=ip):
			try:
				run('%s start'%appPath)
			except:
				print red("xxxxxxxx远程命令执行错误，请检查！xxxxxxxx\n\n")

	def _stop(self, ip, app):
		appPath = self._getAppPath(app) 
		with settings(host_string=ip): 
				try:
					run('%s stop'%appPath)
				except:
					print red("xxxxxxxx远程命令执行错误，请检查！xxxxxxxx\n\n")

	def _restart(self, ip, app):
		appPath = self._getAppPath(app)
		with settings(host_string=ip):  
				try:
					run('%s restart'%appPath)
				except:
					print red("xxxxxxxx远程命令执行错误，请检查！xxxxxxxx\n\n")

	def _getAppPath(self, app):
		if "-web-" in app:
			appPath = '/data/deploy/%s/apache-tomcat/bin/tomcat.sh'%app 
		elif "-service-" in app or "-gateway-" in app:
			appPath = '/data/deploy/%s/ROOT/bin/service.sh'%app 
		else:
			print red("出现未知程序类型，请检查：%s" % app)
		return appPath  
	
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
				appOpt = raw_input("请选择操作：启动【L】，停止【S】，重启【R】，重新选择【P】")
				rules = self.getConfPath(self.rulesPath, app)
				if appOpt.upper() == 'L':
					for rule in rules:
						self._start(rule[1], app)
				elif appOpt.upper() == 'S':
					for rule in rules:
						self._stop(rule[1], app)
				elif appOpt.upper() == 'R':
					for rule in rules:
						self._restart(rule[1], app) 
				elif appOpt.upper() == 'P':
					opt = 'P'	   
				else:
					print red("输入错误，请重新选择操作！")
					continue
				# 操作完成，跳出操作选择
				break
			if opt == 'P':
				continue
			print "操作完成：继续【选择程序】请按1，返回【主页】请按其余数字。"
			nextOpt = getDigit()
			if nextOpt == 1:
				continue
			else:
				break
				
			
	def _appBat_Sub(self, appSubList):
		# 选择操作
		appOpt = raw_input("请选择操作：启动【L】，停止【S】，重启【R】")
		if appOpt.upper() not in ['L', 'S', 'R']:
			print red("输入错误，终止本次操作！")
			return 1
		for app in appSubList:
			print "######当前操作的程序为：%s######" % app
			while True:
				rules = self.getConfPath(self.rulesPath, app)
				if appOpt.upper() == 'L':
					for rule in rules:
						self._start(rule[1], app)
				elif appOpt.upper() == 'S':
					for rule in rules:
						self._stop(rule[1], app)
				elif appOpt.upper() == 'R':
					for rule in rules:
						self._restart(rule[1], app) 	   
				else:
					print red("输入错误，终止本次操作！")
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
				print red("未知程序类型，请检查：%s" % app)
				
		print "请选择操作项！"
		print "--------------------"
		print "1.批量操作所有WEB应用"
		print "2.批量操作所有Service"
		print "3.批量操作所有Gateway"
		print "0.批量操作所有应用"
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
# 		local("clear")
# 		print AppControl.__doc__
		while True:
			print "请选择操作项！"
			print "--------------------"
			print "1. 操作单个程序"
			print "2. 批量操作程序"
			print "0. 退出"
			print "--------------------"

			slct = getDigit([0, 1, 2])
			if (slct == 0):
				print "输入%d,选择【退出】"%slct
				break 
			elif (slct == 1):
				print "输入%d,选择【操作单个程序】"%slct
				self._appSingle()
			elif (slct == 2):
				print "输入%d,选择：【批量操作程序】"%slct
				self._appBat()
			else:
				print red("xxxxxxxx出现未知错误，请检查！xxxxxxxx")
				break
			
# 			local("clear")
			print "已返回到启动【主页】"

