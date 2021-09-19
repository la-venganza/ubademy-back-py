from app.db import db, BaseModelMixin


class Course(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    length = db.Column(db.Integer)
    year = db.Column(db.Integer)
    teacher = db.Column(db.String)
    subject = db.Column(db.String)

    def __init__(self, title, length, year, teacher, subject):
        self.title = title
        self.length = length
        self.year = year
        self.teacher = teacher
        self.subject = subject

    def __repr__(self):
        return f'Course({self.title})'

    def __str__(self):
        return f'{self.title}'
