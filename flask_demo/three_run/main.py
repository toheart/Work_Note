#!/usr/bin/python
# coding=utf-8
# main.py
# @author TangLyan
# @description 
# @created Fri Jun 29 2018 09:17:29 GMT+0800 (中国标准时间)
# @last-modified Fri Jun 29 2018 09:17:29 GMT+0800 (中国标准时间)
import json
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import fields 
from flask_restful import marshal_with 
from flask_restful import reqparse 
from sqlalchemy.orm import class_mapper

app = Flask(__name__)

class Config(object):
      #对外Api数据库相关配置
    DB_USER = 'root'
    DB_PASSWORD = 'sangfor'
    DB_HOST = '192.200.41.231'
    DB_DB = 'dataapi'
    #SQLAlchemy的配置项
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}?charset=utf8".format(DB_USER, DB_PASSWORD, DB_HOST, DB_DB)
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

# 资产表
class Asset(db.Model):
    __tablename__ = 'asset_table'
    auto_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String(128), nullable=False)
    monitor_url = db.Column(db.String(256), nullable=False)
    scan_policy = db.Column(db.Text())
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime())
    update_time = db.Column(db.DateTime())
    is_delete = db.Column(db.String(1), default='0')
    sub_service_id = db.Column(db.String(128))

    def as_dict(self):
        return dict((col.name, getattr(self, col.name))
            for col in class_mapper(self.__class__).mapped_table.c)

    def dict(self):
        print(self.__table__.columns)


post_fields = {
    "auto_id": fields.Integer(),
    'service_id': fields.String()
}

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

req_post_parse = reqparse.RequestParser()
req_post_parse.add_argument('token', type=str, required=True, help='no token', location=['json'])
req_post_parse.add_argument('username', type=str, location=['json'])

@app.route('/')  
def hello():
    data = db.session.query((Asset.service_id,Asset.status)).filter_by(service_id='sangfor').all()
    print(Asset.service_id.key)
    return json.dumps(data, cls=AlchemyJsonEncoder)


@app.route('/post', methods=['POST'])
def post():
    args = req_post_parse.parse_args(strict=True)
    return "helloworld"

@app.errorhandler(400)
def bad_request(error):
    return jsonify(error.data.get('message'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)   