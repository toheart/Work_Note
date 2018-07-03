# Fabric的使用教程

## 1、注意一定要安装

​	fabric == 1.14.0 版本！



##2、初步使用

​	从hello_world开始。

```python
def hello(name="world"):
    print("hello %s"%name)
```

​	在命令行下直接执行：

```shell
fab -f xxx.py hello:name=tly
输出：
hello tly

Done.
```

fab 是fabric的一个shell命令用来执行函数， -f 指定是哪个文件，默认是fabfile.py  



## 3、函数的使用

### 3.1、local

​	local函数：本地执行的shell命令

```python
from fabric.api import local

def prepare_deploy():
    local('uname -s')
```

执行如下：

```shell
$ fab -f fabfile_2.py prepare_deploy
[localhost] local: uname -s
Linux

Done.
```

### 3.2、run

​	远程服务器执行命令

```python
run('ls -l')
```



### 3.3、cd

```python
def execute_ls():
    with cd('/etc'):
        run('uname -s')
        run('ls -l')
```

进入文件夹，且保存上下文环境。一定要使用with



### 3.4、lcd

​	切换本地文件夹，操作如上

###3.5、put

​	上传本地文件到远程服务器

```python
def execute_put():
    with cd('/root'):
        put('/home/tly/project/fibric_demo/aaa', 'aaa')

```

结果如下：

```shell
$ fab -f fabfile_3.py execute_put
[root@192.200.41.231:22] Executing task 'execute_put'
[root@192.200.41.231:22] put: /home/tly/project/fibric_demo/aaa -> /root/aaa

Done.
Disconnecting from root@192.200.41.231... done.
```

###3.6、get

​	下载本地文件到远程服务器

```python
def execute_get():
    get('/root/aaa', '%(path)s')
```

结果如下：

```python
$ fab -f fabfile_3.py execute_get
[root@192.200.41.233:22] Executing task 'execute_get'
[root@192.200.41.233:22] download: /home/tly/project/fibric_demo/aaa <- /root/aaa

Done.
```

###3.7、prompt

###3.8、reboot

​	重启远程服务器

###3.9、@task

###3.10、@runs_ones

## 4、环境的使用

​	需要访问远程服务器的话，那么我们需要填入一些基本的信息，host，user，password等信息。

​	fabric中是通过设置env上下文管理器来管理的。

​	如下：

```python
from fabric.api import *

env.hosts = ['192.200.41.233'，'192.200.41.232']  #添加多台服务器的域名
env.user = 'root'		#服务器的用户名
env.password = '1'		#服务器的密码

def execute_ls():
    with cd('/virus'):
    	run('ls')
    	run('uname -s')
```

执行如下：

```shell
(fabric) tly@tly-dev:~/project/fibric_demo$ fab -f fabfile_3.py execute_ls
[192.200.41.233] Executing task 'execute_ls'
[192.200.41.233] run: ls
[192.200.41.233] out: anaconda-ks.cfg  api.tar  docker  perl5  saas-setup  saas-setup.tar.gz

[192.200.41.233] run: uname -s
[192.200.41.233] out: Linux

[192.200.41.232] Executing task 'execute_ls'
[192.200.41.232] run: ls
[192.200.41.232] out: anaconda-ks.cfg  authority.tar	zabbix-release-3.4-2.el7.noarch.rpm

[192.200.41.232] run: uname -s
[192.200.41.232] out: Linux


Done.
Disconnecting from 192.200.41.233... done.
Disconnecting from 192.200.41.232... done.
```

如果多个服务器，有多个不同的命令该怎么写？

使用env.passwords来配置。代码如下：

```python
from fabric.api import *

env.hosts = ['192.200.41.233', '192.200.41.231']
env.user = 'root'
env.passwords = {
    'root@192.200.41.233:22' : '1',
    'root@192.200.41.231:22' : '1'
}

def execute_ls():
    run('uname -s')
    run('ls -l')
```

一定要记得写端口等信息。



# 5、分配不同的组

​	多个项目，不同的操作，那么我们就需要使用不同的操作。引入 分组

```python
from fabric.api import *

env.passwords = {
    'root@192.200.41.233:22' : '1',
    'root@192.200.41.231:22' : '1',
    'root@192.200.41.203:22' : '2',
    'tly@192.168.11.11:22': 1,
}

env.roledefs = {
            'testserver': ['root@192.200.41.233:22',],  
            'realserver': ['tly@192.168.11.11:22', ]
            }

@roles('testserver')
def execute_ls():
    with cd('/etc'):
        run('uname -s')
        run('ls -l')
```



​	

​	