import json, time, os

from flask import request, current_app

from main import db
from main.api import api
from main.models.note import Note
from main.models.tag import Tag
from main.models.image import Image
from main.utils.auth import auth
from main.utils.response import Response

# 新建笔记
@api.route('/create_note', methods = ['POST'])
@auth.login_required
def create_note():
    # 获取请求参数
    try:
        data = json.loads(request.data)
    except:
        return Response.error('请求参数错误')
    
    # 数据格式校验
    title = data.get('title')
    if not title or len(title) == 0:
        return Response.error('标题格式错误')
    tags_name = data.get('tags_name')
    if not tags_name or len(tags_name) == 0:
        return Response.error('标签不能为空')
    
    # 保存数据
    content = data.get('content')
    tags = Tag.query.filter(Tag.name.in_(tags_name))
    images = []
    images_name = data.get('images_name')
    if images_name and len(images_name) > 0:
        for image_name in images_name:
            images.append(Image(name = image_name))
    create_time = update_time = int(time.time()) * 1000
    note = Note(title = title, content = content, tags = tags, images = images, create_time = create_time, update_time = update_time)
    try:
        db.session.add(note)
        db.session.commit()
    except:
        return Response.error('保存笔记失败')
    return Response.success('保存笔记成功')

# 查询笔记列表
@api.route('/note_list/<int:page_num>/<int:page_size>')
def note_list(page_num, page_size):
    if page_num <= 0 or page_size <= 0:
        return Response.error('分页信息错误')
    notes = Note.query.order_by(Note.create_time.desc()).offset((page_num - 1) * page_size).limit(page_size)

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
    total = Note.query.count()
    return Response.success({
        'list': data,
        'total': total
    })

# 查询笔记详情
@api.route('/note_info/<int:id>')
def note_info(id):
    note = Note.query.get(id)
    if not note:
        return Response.error('笔记信息不存在')
    
    # 笔记阅读数+1
    note.click += 1
    try:
        db.session.add(note)
        db.session.commit()
    except:
        return Response.error('笔记信息错误')
    
    # 组装数据
    tags = []
    for tag in note.tags.order_by(Tag.name).all():
        tags.append({
            'id': tag.id,
            'name': tag.name
        })
    return Response.success({
        'title': note.title,
        'content': note.content,
        'click': note.click,
        'support': note.support,
        'update_time': note.update_time,
        'tags': tags
    })

# 修改笔记
@api.route('/change_note', methods = ['POST'])
@auth.login_required
def change_note():
    # 获取请求参数
    try:
        data = json.loads(request.data)
    except:
        return Response.error('请求参数错误')
    
    # 数据格式校验
    id = data.get('id')
    if not id:
        return Response.error("笔记id不能为空")
    note = Note.query.get(id)
    if not note:
        return Response.error('笔记信息不存在')
    title = data.get('title')
    if not title or len(title) == 0:
        return Response.error('标题格式错误')
    tags_name = data.get('tags_name')
    if not tags_name or len(tags_name) == 0:
        return Response.error('标签不能为空')
    
    # 保存数据
    note.title = title
    note.content = data.get('content') or ''
    note.update_time = int(time.time()) * 1000
    note.tags = Tag.query.filter(Tag.name.in_(tags_name))
    images_name = data.get('images_name')
    if images_name and len(images_name) > 0:
        # 追加图片
        for image_name in images_name:
            note.images.append(Image(name = image_name))
    try:
        db.session.add(note)
        db.session.commit()
    except:
        return Response.error('保存笔记失败')
    return Response.success('保存笔记成功')

# 删除笔记
@api.route('/delete_note/<int:id>')
@auth.login_required
def delete_note(id):
    note = Note.query.get(id)
    if not note:
        return Response.error('笔记信息不存在')
    
    try:
        # 删除笔记相关附件
        images = Image.query.filter_by(note_id = id)
        for image in images.all():
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.name)
            if os.path.exists(path):
                os.remove(path)
        images.delete()
        db.session.delete(note)
        db.session.commit()
    except:
        return Response.error('删除笔记失败')
    return Response.success('删除笔记成功')

# 笔记点赞
@api.route('/note_support/<int:id>')
def note_support(id):
    note = Note.query.get(id)
    if not note:
        return Response.error('笔记信息不存在')
    
    # 笔记点赞数+1
    note.support += 1
    try:
        db.session.add(note)
        db.session.commit()
    except:
        return Response.error('笔记信息错误')
    return Response.success('点赞成功')
