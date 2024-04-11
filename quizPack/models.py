from quizPack import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(10), nullable = False, unique = True)
    # name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20), nullable = False)
    points = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.points}')"
