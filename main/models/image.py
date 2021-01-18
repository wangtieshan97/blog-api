from main import db

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable = False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
