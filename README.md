# 我的博客

## 一、配置运行环境(Linux)

```bash
#!/bin/bash

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip3 install -r requirements.txt
pip3 install gunicorn

# 初始化数据库
flask db init
flask db migrate
flask db upgrade

# 设置账户信息(非必须)
export USERNAME='用户名'
export PASSWORD='密码'

# 启动
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

## 二、接口文档

### 1. 用户登录

```bash
POST /api/login
```

参数

```json
{
    "username": "用户名",
    "password": "密码"
}
```

响应

```json
{
    "code": 0,
    "data": "令牌",
    "msg": "ok"
}
```

### 2. 附件上传

```bash
POST /api/upload
```

参数

```bash
form-data files
```

响应

```json
{
    "code": 0,
    "data": "附件上传成功",
    "msg": "ok"
}
```

### 3. 新建笔记

```bash
POST /api/create_tag
```

参数

```json
{
    "title": "标题",
    "content": "内容",
    "tags_name": [
        "标签名1",
        "标签名2"
    ],
    "images_name": [
        "附件名1",
        "附件名2"
    ]
}
```

响应

```json
{
    "code": 0,
    "data": "保存笔记成功",
    "msg": "ok"
}
```

### 4. 查询笔记列表

```bash
GET /api/note_list/{page_num}/{page_size}
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": [],
    "msg": "ok"
}
```

### 5. 查询笔记详情

```bash
GET /api/note_info/{id}
```

参数

```bash
无
```

响应

```json
{
    "title": "标题",
    "content": "内容",
    "click": "阅读数",
    "support": "点赞数",
    "update_time": "修改时间",
    "tags_name": [
        "标签名1",
        "标签名2"
    ]
}
```

### 6. 修改笔记

```bash
POST /api/change_note
```

参数

```json
{
    "id": "序号",
    "title": "标题",
    "content": "内容",
    "tags_name": [
        "标签名1",
        "标签名2"
    ],
    "images_name": [
        "新增附件名1",
        "新增附件名2"
    ]
}
```

响应

```json
{
    "code": 0,
    "data": "保存笔记成功",
    "msg": "ok"
}
```

### 7. 删除笔记

```bash
GET /api/delete_note/{id}
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": "删除笔记成功",
    "msg": "ok"
}
```

### 8. 笔记点赞

```bash
GET /api/note_support/{id}
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": "点赞成功",
    "msg": "ok"
}
```

### 9. 新建标签

```bash
POST /api/create_tag
```

参数

```json
{
    "name": "标签名"
}
```

响应

```json
{
    "code": 0,
    "data": "新建标签成功",
    "msg": "ok"
}
```

### 10. 查询标签列表

```bash
GET /api/tag_list
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": [
        {
            "id": "序号1",
            "name": "标签名1",
            "note_num": "笔记数1"
        },
        {
            "id": "序号2",
            "name": "标签名2",
            "note_num": "笔记数2"
        }
    ],
    "msg": "ok"
}
```

### 11. 按标签查询笔记

```bash
GET /api/find_note_by_tag/{id}/{page_num}/{page_size}
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": [],
    "msg": "ok"
}
```

### 12. 删除标签

```bash
GET /api/delete_tag/{id}
```

参数

```bash
无
```

响应

```json
{
    "code": 0,
    "data": "删除标签成功",
    "msg": "ok"
}
```

