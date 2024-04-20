from flask_login import UserMixin
from quizPack import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(10), nullable = False, unique = True)
    email = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20), nullable = False)
    points = db.Column(db.Integer, default = 0)
    profile = db.Column(db.String(20), default = 'user.jpg')
    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.points}', '{self.profile}')"
    

class SavedQuestions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    question = db.Column(db.String(1000), nullable = False)
    option1 = db.Column(db.String(1000), nullable = False)
    option2 = db.Column(db.String(1000), nullable = False)
    option3 = db.Column(db.String(1000), nullable = False)
    option4 = db.Column(db.String(1000), nullable = False)
    answer = db.Column(db.String(1000), nullable = False)
    explanation = db.Column(db.String(1000), nullable = False)
    def __repr__(self):
        return f"SavedQuestions('{self.id}','{self.user_id}', '{self.question}','{self.option1}', '{self.option2}', '{self.option3}', '{self.option4}', '{self.answer}', '{self.explanation}')"
