# 裸centos的一些安装部署

## 1、安装python-pip

​	首先安装epel扩展源：

​		yum -y install epel-release

​	更新完成之后，安装pip:

​		yum -y install python-pip

## 2、安装python依赖包：

​	初次直接运行：

​		pip install -r requirement.list

​	如果是裸的centos绝对会报错！

​	然后开始漫长的改错安装。

	### 错误一：EnvironmentError: mysql_config not found

​	原因：缺少mysql驱动导致，所以加上mysql就行

​	`yum -y install mysql-devel`



###错误二：error: command 'gcc' failed with exit status 1

​	原因：没有gcc命令（c语言编译器），没有 那就安就行了

​	`yum -y install gcc`

​	但是还是会再次报错：然后 我们需要安装下 

​	`yum -y install python-devel`

以上，就安装完了依赖包。



## 3、安装gunicorn

​	没有别的就一个：

​	`pip install gunicorn`



## 4、安装supervisor 

​	安装命令

​	`easy_install supervisor`

​	验证是否成功：echo_supervisord_conf

​	然后mkdir /etc/supervisor

​		echo_supervisord_conf > /etc/supervisor/supervisord.conf	

​	现在有配置文件还是不够，我们需要扩展，所以

  		mkdir   /etc/supervisor/config.d 

​	修改/etc/supervisor/supervisord.conf的最下面的一行include

​		files = /etc/supervisor/config.d/*.conf



​	最基本的配置：

```ini
[program:tomcat]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run
directory=xxxx
autostart=true
autorestart=true
startsecs=5
priority=1
stopasgroup=true
killasgroup=true
```



## 5、安装nginx

​	安装各种依赖项：

### 1、查看内核版本，看看是否高于2.6。#2.6版本以上内核才支持epoll

###2、安装GCC编译器

`yum -y install gcc`

###3、安装C++编译器

`yum -y install gcc-c++`

###4、安装PCRE库  为了支持正则表达式

`yum install -y pcre pcre-devel`

####5、安装zlib库

`yum install -y zlib zlib-devel`

###6、安装OpenSSL

`yum install -y openssl openssl-devel`

### 7、安装nginx

`yum -y install nginx `

以上依赖环境全部安装完成。



全部都安装的命令：

```shell
yum -y install gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel nginx
```



## 6、设置系统时间

下载工具：ntp

```shell 
yum -y install ntp
ntpdate -u asia.pool.ntp.org
rm -rf /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```



## 7、设置supervisor为开机自启动

1、vim /lib/systemd/system/supervisord.service 

2、

```vim
[Unit]
Description=Process Monitoring and Control Daemon
After=rc-local.service



[Service]
Type=forking
ExecStart=/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
ExecReload=supervisorctl reload



[Install]
WantedBy=multi-user.target
```



3、systemctl enable supervisord.service 



## 8、mysql远程授权访问

```shell
 GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "password";
 flush privileges;

 
[mysqld] 
skip_name_resolve 

```

