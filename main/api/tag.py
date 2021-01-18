import json

from flask import request

from main import db
from main.api import api
from main.models.tag import Tag
from main.models.note import Note
from main.utils.auth import auth
from main.utils.response import Response

# 新建标签
@api.route('/create_tag', methods = ['POST'])
@auth.login_required
def create_tag():
    # 获取请求参数
    try:
        data = json.loads(request.data)
    except:
        return Response.error('请求参数错误')
    
    # 数据格式校验
    name = data.get('name')
    if not name or len(name) == 0:
        return Response.error('标签格式错误')
    
    # 保存数据
    t = Tag(name = name)
    try:
        db.session.add(t)
        db.session.commit()
    except:
        # 标签不能重名
        return Response.error('新建标签失败')
    return Response.success('新建标签成功')

# 查询标签列表
@api.route('/tag_list')
def tag_list():
    tags = Tag.query.order_by(Tag.name).all()

    # 组装数据
    data = []
    for tag in tags:
        data.append({
            'id': tag.id,
            'name': tag.name,
            'note_num': tag.notes.count()
        })
    return Response.success(data)

# 按标签查询笔记
@api.route('/find_note_by_tag/<int:id>/<int:page_num>/<int:page_size>')
def find_note_by_tag(id, page_num, page_size):
    if page_num <= 0 or page_size <= 0:
        return Response.error('分页信息错误')
    tag = Tag.query.get(id)

    if not tag:
        return Response.error('标签信息不存在')
    notes = tag.notes.order_by(Note.create_time.desc()).offset((page_num - 1) * page_size).limit(page_size).all()

    # 组装数据
    data = []
    for note in notes:
        data.append({
            'id': note.id,
            'title': note.title,
            'click': note.click,
            'support': note.support,
            'update_time': note.update_time
        })
    total = tag.notes.count()
    return Response.success({
        'list': data,
        'total': total
    })

# 删除标签
@api.route('/delete_tag/<int:id>')
@auth.login_required
def delete_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return Response.error('标签信息不存在')
    
    # 执行删除
    try:
        db.session.delete(tag)
        db.session.commit()
    except:
        return Response.error('删除标签失败')
    return Response.success('删除标签成功')
