import os

from flask import request, current_app
from werkzeug.utils import secure_filename

from main.api import api
from main.utils.auth import auth
from main.utils.response import Response

@api.route('/upload', methods = ['POST'])
@auth.login_required
def upload():
    # 参数错误
    if 'files' not in request.files:
        return Response.error('请求参数错误')
    files = request.files.getlist('files')

    # 未选择文件
    if files[0].filename == '':
        return Response.error('附件不存在')
    
    # 文件类型检查
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    for file in files:
        if '.' not in file.filename or file.filename.split('.')[-1].lower() not in allowed_extensions:
            return Response.error('存在非法文件类型')
    
    # 路径检查
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    
    # 开始上传
    for file in files:
        file.save(os.path.join(upload_folder, secure_filename(file.filename)))
    return Response.success('附件上传成功')
