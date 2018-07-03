# flask的快速入门使用

## 1、项目目录的比较好的结构

├── app
│   ├── controller
│   │   ├── bug.py				-------------->用于bug处理的文件
│   │   ├── \__init__.py				-------------->这个是蓝图的创建文件
│   │   ├── tamper.py				-------------->用于tamper处理的文件
│   │   ├── usability.py			-------------->用于usability处理的文件
│   │   └── user.py				-------------->用于user处理的文件
│   ├── \__init__.py				-------------->这个是app的初始化文件
│   └── models.py				-------------->这个是ORM映射的文件
├── config.py					-------------->这个是相关配置文件的文件
└── cloudeye.py    				-------------->这个是主app的进入界面

功能如右边显示。

每个文件的代码如下解释。

从一个应用的入口开始：

### 1.1、eyecloud.py开始的地方

```python
# coding=utf-8
#!/usr/bin/python
from app import app	#从app目录下__init__.py中导入app
	
if __name__ == "__main__":
    app.run('0.0.0.0',port=5000, debug=True)	#使用python eyecloud.py启动应用	
```

另一种比较推荐的启动应用的方式：(进入项目顶层目录)

​	export FLASK_APP=eyecloud.py

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
from app.controller import v1

app = Flask(__name__)		#创建app实例对象
app.config.from_object(Config)	#导入相关扩展的配置文件
app.register_blueprint(v1, url_prefix='/api/cloudeye/v1')	#注册组件化的蓝图

db = SQLAlchemy()			# 创建ORM的实例对象
db.init_app(app)			# 初始化数据库连接
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

​	在app中我们注册了蓝图的应用，而蓝图的模块来自于controller/\__init__.py,代码如下

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

​	