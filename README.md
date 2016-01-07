12月31日 更
***
**以后备份脚本简化为两条命令：**

> $fab bak: 备份功能
> $fab dep: 部署功能


**```$fab bak ```**
![替代文字](https://wt-prj.oss.aliyuncs.com/95e8fcec74c047c787b20aeb2fb05e0c/e1c64073-1dc1-4c2b-8113-dddaf0f4c769.png)
![替代文字](https://wt-prj.oss.aliyuncs.com/95e8fcec74c047c787b20aeb2fb05e0c/c0b1539d-b85c-4f9d-b3ec-1eddaf6d8bb5.png)

**```$fab dep ```**
![替代文字](https://wt-prj.oss.aliyuncs.com/95e8fcec74c047c787b20aeb2fb05e0c/fca786ec-0500-40f8-9673-7c89b95dcf2d.png)

***** 12月31日更新 ***** 界面化部署脚本

**mapping 规则文件说明**
![替代文字](https://wt-prj.oss.aliyuncs.com/95e8fcec74c047c787b20aeb2fb05e0c/4e1dd107-8781-4f36-b127-9b52803e289c.png)

***
**格式说明**
```* [???]：```应用的名字，[foundation] 表示 foudation 应用的部署规则
```* regx：```正则表达式，在 脚本地址/Resource 下，文件名符合当条正则的文件，均会采用当条部署规则
```* host_1,host_2：```当条规则下的文件部署地址，数量没有限制
> * 键名格式为host_?
> * 键值格式为 ('目标ip',目标端口,'目标文件地址')


***
**流程**
1.根据各规则对应的正则格式，命名war包
2.将文件上传到 脚本地址/Resource 文件夹下
3.在脚本所在地址执行部署命令

***
**命令说明**
``` $fab depFoundation ``` : 部署 foundation 应用
```$fab depBatch ```: 部署 batch 应用
```$fab depTrade ```: 部署 trade 应用
...
```$fab depAll ```: 部署所有应用

***
```$fab confAll ```: 给所有应用生成所有配置文件 

```$fab confByApp ```: 给指定应用生成指定配置文件
> * $ fab confByApp : app="foundation",fName="system.properties"

```$fab confByInst ```: 给指定应用的指定实例生成配置文件
> * $ fab confByApp:app="foundation",ip="10.10.1.9",fromPath="./model/",fName="system.properties",toPath="/data/foundation/conf/",instId="3"
