from flask import current_app
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 鉴权实例
auth = HTTPTokenAuth(scheme = 'JWT')

# 生成令牌
def generate_auth_token(expiration = 600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'id': current_app.config['USERNAME'] }).decode('utf-8')

# 校验令牌
@auth.verify_token
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data['id'] == current_app.config['USERNAME']
    except:
        return None
