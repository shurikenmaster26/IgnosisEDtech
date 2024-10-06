from Ignosis import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),unique=False,nullable=False, default='default.png')
    password=db.Column(db.String(60),nullable=False)
    bio=db.Column(db.Text() ,nullable=True, default="")
    skillset=db.Column(db.Text(), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_points = db.Column(db.Integer, default=0)
    current_league=db.Column(db.Text(), nullable=False, default='Mortal')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Badges(db.Model):
    BadgeID = db.Column(db.Integer, primary_key=True)
    BadgeName = db.Column(db.Text)
    Classification = db.Column(db.Text)
    Badge_image=db.Column(db.String(20),unique=False,nullable=False, default='unranked.jpeg')

class PracticeProblems(db.Model):
    ProblemID = db.Column(db.Integer, primary_key=True)
    ProblemStatement = db.Column(db.Text)
    SolvingPoints = db.Column(db.Integer)
    ProblemClass = db.Column(db.Text)

class UserBadges(db.Model):
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    BadgeID = db.Column(db.Integer, db.ForeignKey('badges.BadgeID'), primary_key=True)

    user = db.relationship('User', backref='user_badges')
    badge = db.relationship('Badges', backref='user_badges')

class UserProblems(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    ProblemID = db.Column(db.Integer, db.ForeignKey('practice_problems.ProblemID'))

    user = db.relationship('User', backref='user_problems')
    problem = db.relationship('PracticeProblems', backref='user_problems')
    
    def update_user_points(user_id, points):
        user = User.query.get(user_id)
        if user:
            user.total_points += points
            db.session.commit()

class MCQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    choices = db.Column(db.Text, nullable=False)  # Store choices as a JSON string
    correct_answer = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"MCQuestion('{self.question}', '{self.correct_answer}')"

