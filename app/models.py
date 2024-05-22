from app import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    root = db.Column(db.Integer, default=0)
   
    def __repr__(self):
        return 'User %r' % self.id 


class Articles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    image_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    color = db.Column(db.String(100))
    root = db.Column(db.Integer, default=1)

    def __repr__(self):
        return 'Articles %r' % self.id 


class Tests(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    image_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    color = db.Column(db.String(100))
    
    def __repr__(self):
        return 'Tests %r' % self.id 


class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id'))
    
    def __repr__(self):
        return 'Question %r' % self.id 


class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    weight = db.Column(db.Integer)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
    
    def __repr__(self):
        return 'Answer %r' % self.id 


class Interpretation(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id'))
    
    def __repr__(self):
        return 'Interpretation %r' % self.id 


class Rezult(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    total_score = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return 'Interpretation %r' % self.id 