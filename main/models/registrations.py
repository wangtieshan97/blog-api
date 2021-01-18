from main import db

registrations = db.Table(
    'registrations',
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)
