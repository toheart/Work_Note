



# flask项目

项目总体的目录结构：

/projects/模块名称/子模块名称/requirements/requirements.list	 依赖库	存放代码所依赖的代码

​						     /app   						功能代码

​						     /config 						配置文件 存放上线使用的配置文件

​						     /tasks						任务管理

​						    /data 							数据保存

​						   /log							进程日志打印输出的目录

## 1、flask的目录结构

​	1、项目目录的比较好的结构

├── app
│   ├── controller

│   │   ├── v1

│   │   │   ├── bug.py				-------------->用于bug处理的文件
│   │   │   ├── \__init__.py			-------------->这个是蓝图的创建文件
│   │   │   ├── tamper.py			-------------->用于tamper处理的文件
│   │   │   ├── usability.py			-------------->用于usability处理的文件
│   │   │   └── user.py				-------------->用于user处理的文件
│   ├── \__init__.py				-------------->这个是app的初始化文件
│   └── models.py				-------------->这个是ORM映射的文件
├── config.py					-------------->这个是相关配置文件的文件

├── log.py                                            --------------> 日志输出文件

└── cloudeye.py    				-------------->这个是主app的进入界面

功能如右边显示。

每个文件的代码如下解释。

### 为什么采用这样的目录结构？

​	对于版本的迭代来说，这样的目录结构比较适合于版本的扩展。多个办法使用蓝图的方式都在一台服务器下。



从一个应用的入口开始：

### 1.1、cloudeye.py开始的地方

```python
# coding=utf-8
#!/usr/bin/python
from app import app	#从app目录下__init__.py中导入app
	
if __name__ == "__main__":
    app.run('0.0.0.0',port=5000, debug=True)	#使用python eyecloud.py启动应用	
```

另一种比较推荐的启动应用的方式：(进入项目顶层目录)

​	export FLASK_APP=cloudeye.py

​	export FLASK_DEBUG=1  #开启DEBUG

然后直接执行

​	`flask run -h 0.0.0.0 -p 5000` 

这样flask就开始执行了。



### 1.2、app目录下的解析

​	从eyecloud.py进入app的目录下, 引用的是\__init__.py的文件中的app模块

```python
from flask import Flask 	# 导入Flask
from flask_sqlalchemy import SQLAlchemy	
from flask_migrate import Migrate

from config import Config
from app.controller.v1 import v1
from app.models import db

app = Flask(__name__)		#创建app实例对象
app.config.from_object(Config)	#导入相关扩展的配置文件
db.init_app(app)			# 初始化数据库连接
app.register_blueprint(v1, url_prefix='/api/cloudeye/v1')	#注册组件化的蓝图
migrate = Migrate(app, db)	 # 创建数据库迁移的对象

from app import models		 # 导入models模块
```

​	新知识点：

​		app.config.from_object(模块名)

config.py代码如下：

```python
# coding=utf-8
#!/usr/bin/python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #CACHE配置 暂没有使用
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = 0
    #数据库相关配置
    DB_USER = 'root'
    DB_PASSWORD = '1'
    DB_HOST = '127.0.0.1'
    DB_DB = 'dataApi'
    #SQLAlchemy的配置项
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_DB)
```

​	对于迁移数据库的使用：

​		因为之前有导入FLASK_APP作为环境变量，所以可以使用如下命令来迁移

```shell
flask db init 		#初始化migration
flask db migrate	#将models映射为sql语句保存
flask db upgrade	#向数据库中导入sql语句
```



### 1.3、蓝图的使用

​	在app中我们注册了蓝图的应用，而蓝图的模块来自于controller/v1/\__init__.py,代码如下

```python
# coding=utf-8
#!/usr/bin/python
from flask import Blueprint

v1 = Blueprint('v1', __name__) #'v1'表示endpoint。

import bug
import tamper
import usability
import user
```

### 1.4、接口使用的一个框架

#### flask_restful

​	理由？

​	当我们传入json数据的使用，我们需要对传进来的参数进行校验，看参数是否满足？一般情况下，我们都会去自己手动的来判断是否传入值，或者写通用的函数。这样的重复造轮子，我觉得是多余的。那么我们就需要一个方法。

​	from flask_restful import fields, marshal_with

​	field+ marshal_with 装饰器。可以用来格式化输出。

​	reqparse 用来判断传入的json类型是否能够满足。

### 1.5、flask一些常用的函数的介绍 

#### 1.5.1、Flask、SQLAlchemy、Migrate

```python
from flask import Flask 	# 导入Flask
from flask_sqlalchemy import SQLAlchemy	 #一般对象的新建在models中进行
from flask_migrate import Migrate

app = Flask(__name__)    #初始化Flask对象
app.config.from_object(Config)	#导入相关扩展的配置文件
db.init_app(app)			# 初始化数据库连接
migrate = Migrate(app, db)
```

#### 1.5.2、request，jsonify，session

from flask import request, session, jsonify	

request:

​	request.args.get() 获取GET方式请求的数据

​	request.json.get()   获取json 数据

 	request.form.get() 获取form 表单的数据

jsonify:

​	作用：自动的将字典类型的数据转化成json格式的数据，并添加Content-Type：Application/json

session:
	使用前，在app中添加session的SECRET_KEY

​	然后像类字典的方式使用则OK。

#### 1.5.3、redirect，url_for

​	redirect:

​		from flask import redirect

​		redirect('/hello')

​	url_for:

​		使用url映射中保存的信息生成url 

​	

### 1.6、日志相关的配置

```python
"""
logger.py

Author: zeusguy
Date: 20171108
"""
import logging
import os
import re
import time

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

from app.config import CORE_CFG   


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


def get_logger(
    logger_name, fname=None,
    log_dir=CORE_CFG.LOG['log_dir'], 
    level=CORE_CFG.LOG['log_level'],
    type=CORE_CFG.LOG['log_type']):
    """获取日志logger。

    Args:
        logger_name: logger名称
        log_dir: 日志基础路径
        fname: 日志文件名称字符串
        level: 日志级别
        type: 取值'TimeRotatingFileHandler'、'RotatingFileHandler'、'StreamHandler'
    """
    log_dir = os.path.join(log_dir, logger_name)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    log_fmt = '[%(asctime)s][%(levelname)s][%(filename)s]%(message)s'
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_fmt, date_fmt)

    logger = logging.getLogger(logger_name)
    logger.setLevel(LEVELS[level])

    # add by zeusguy
    # 20171201
    # 如果logger.handlers非空，直接返回
    # 解决输出多行相同记录的BUG
    if logger.handlers:
        return logger

    if not fname:
        fname = '_'.join([logger_name, str(os.getpid())])

    if type == 'TimedRotatingFileHandler':
        date_now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        log_file = os.path.join(log_dir, ''.join([fname, '.log']))
        if not os.path.exists(log_file):
            tmp_file = open(log_file, "w")
            tmp_file.close()
        log_handler = TimedRotatingFileHandler(filename=log_file, 
                                               when='midnight',
                                               interval=1,
                                               backupCount=7)
        log_handler.suffix = "%Y-%m-%d.log"
        log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}\.log")
    elif type == 'RotatingFileHandler':
        log_file = os.path.join(log_dir, fname)
        if not os.path.exists(log_file):
            tmp_file = open(log_file, "w")
            tmp_file.close()
        log_handler = RotatingFileHandler(filename=log_file, mode='a', 
                                          maxBytes=1024*1024*2, backupCount=10)
    else:
        log_handler = StreamHandler()

    log_handler.setFormatter(formatter)
    logger.setLevel(LEVELS[level])
    logger.addHandler(log_handler)

    return logger
```

日志打印的目录：

​	/projects/模块名/log



##2、flask的部署规范

**使用**：flask+gunicorn+nginx+supervisor+docker

每部分的功能：

###gunicorn

了解wsgi协议：

web应用的本质，分为四个部分：

1. 浏览器发送一个HTTP请求；
2. 服务器收到请求，生成一个HTML文档；
3. 服务器把HTML文档作为HTTP响应的Body发送给浏览器；
4. 浏览器收到HTTP响应，从HTTP Body取出HTML文档并显示

以上是一个请求所做的所有的工作。对于请求静态HTML而言是很简单的，但是对于动态生成HTML，这样的繁琐的生成，我们就需要了解HTTP规范的很多东西，例如：请求头，请求行，请求体的等等处理。对于业务来说，是不友好的。正确的做法是底层代码由专门的服务器软件实现，我们用Python专注于生成HTML文档。既然是底层代码管理，那么就要定义一个统一的接口。这个接口就是wsgi。  

​														------摘自《廖雪峰的官方网站WSGI接口》

而gunicorn是一种wsgi的容器，使用prefork master-worker模型，也就是有两个进程协作工作：Master进程，负责接收和分配任务；Worker进程，负责处理子任务。当Worker进程将子任务处理完成后，结果返回给Master进程，由Master进程做归纳汇总，最后得到最终的结果 。

作用：web服务器的作用。

配置文件的相关配置：

```shell
# coding=utf-8

# 并行工作进程数
workers = 4
# 每个工作进程下的线程数
threads = 2
# 监听内网端口
bind = '127.0.0.1:8000'
# 设置守护进程，让supervisor来进行管理
daemon = 'false'
# 工作模式为协程， 默认的是sync
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '/projects/dataapi/gunicorn/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '/projects/dataapi/gunicorn/access.log'
errorlog = '/projects/dataapi/gunicorn/error.log'

loglevel = 'warning'
```



###nginx

有了web服务器，为什么还要nginx?

​	首先作为前端服务器它可以处理一切静态文件请求，此时 gunicorn 作为后端服务器，nginx 将会把动态请求转发给后端服务器，因此我们可以起多个 gunicorn 进程，然后让 nginx 作均衡负载转发请求给多个 gunicorn 进程从而提升服务器处理效率与处理能力 

​	nginx的主要作用是：

​	1、更好的处理静态资源文件

​	2、负责转发的功能

​	3、安全方面的问题，在公网下nginx毕竟是专业服务器，比较安全

​	4、支持的协议。

​	5、Nginx可以使用配置文件来添加黑名单。

总之，加nginx主要是让项目更好稳定，安全。



### supervisor

​	supervisor的作用主要是对进程进行管理。具体的使用方法可以查看另一个文档。

​	supervisord

​	supervisorctl

配置文件相关配置：

```shell
[program:dataapi]
command=/usr/bin/gunicorn -c /virus/api/api/gunicorn.conf cloudeye:app
directory=/virus/api/api
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

[program:apisync]
command=python sync_main.py
directory=/virus/api/api
autostart=true
autorestart=true
startsecs=5
stopasgroup=true
killasgroup=true
```



### docker

​	用来安装flask项目运行的最初的环境配置。

​	裸centos的安装环境请查看另一份文档。





# flask一些骚操作

## 查询数据库返回dict类型

1、在Model中实现一个方法，然后调用即可：

​	只查询一个表，返回全部字段，使用：

```python
def dict():
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
```

​	

```python
class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 判断是否是Query
        if isinstance(obj, Query):
            # 定义一个字典数组
            fields = []
            # 定义一个字典对象
            record = {}
            # 检索结果集的行记录
            for rec in obj.all():
                # 检索记录中的成员
                for field in [x for x in dir(rec) if
                              # 过滤属性
                              not x.startswith('_')
                              # 过滤掉方法属性
                              and hasattr(rec.__getattribute__(x), '__call__') == False
                              # 过滤掉不需要的属性
                              and x != 'metadata']:
                    data = rec.__getattribute__(field)
                    try:
                        record[field] = data
                    except TypeError:
                        record[field] = None
                fields.append(record)
            # 返回字典数组
            return fields
        # 其他类型的数据按照默认的方式序列化成JSON
        return json.JSONEncoder.default(self, obj)
   
json.dumps(result1, cls=AlchemyJsonEncoder)
```

















































