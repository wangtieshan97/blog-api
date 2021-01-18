import json

from flask import request, current_app

from main.api import api
from main.utils.auth import auth, generate_auth_token
from main.utils.response import Response

# 用户登录
@api.route('/login', methods = ['POST'])
def login():
    # 获取请求参数
    try:
        data = json.loads(request.data)
    except:
        return Response.error('请求参数错误')
    
    # 数据格式校验
    username = data.get('username')
    if not username or len(username) < 2:
        return Response.error('用户名格式错误')
    password = data.get('password')
    if not password or len(password) < 6:
        return Response.error('密码格式错误')
    
    # 验证用户信息
    if username != current_app.config['USERNAME']:
        return Response.error('用户信息不存在')
    if password != current_app.config['PASSWORD']:
        return Response.error('密码错误')
    
    # 获取令牌
    token = generate_auth_token(3600)
    return Response.success(token)
