# nginx学习

## 安装nginx

前期准备工作：

​	1、查看内核版本，看看是否高于2.6。#2.6版本以上内核才支持epoll

​	2、安装GCC编译器

​		`yum -y install gcc`

​	3、安装C++编译器

​		`yum -y install gcc-c++`

​	4、安装PCRE库  为了支持正则表达式

​		`yum install -y pcre pcre-devel`

​	5、安装zlib库

​		`yum install -y zlib zlib-devel`

​	6、安装OpenSSL

​		`yum install -y openssl openssl-devel`