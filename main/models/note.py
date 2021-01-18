import time

from main import db
from main.models.registrations import registrations

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32), nullable = False)
    content = db.Column(db.Text, default = '')
    click = db.Column(db.Integer, default = 0)
    support = db.Column(db.Integer, default = 0)
    create_time = db.Column(db.Integer, default = 0)
    update_time = db.Column(db.Integer, default = 0)
    tags = db.relationship(
        'Tag',
        secondary = registrations,
        backref = db.backref('notes', lazy = 'dynamic'),
        lazy = 'dynamic'
    )
    images = db.relationship('Image', backref = 'note')
