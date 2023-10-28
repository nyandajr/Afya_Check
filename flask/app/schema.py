from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # roles: user, admin
    role = db.Column(db.String(16), nullable=False, default='user')
    scores = db.relationship('UserScores', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            username=self.username, 
            age=self.age, 
            gender=self.gender, 
            date_registered=self.date_registered
        )


class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    title_sw = db.Column(db.String(), nullable=False)
    options = db.relationship('CheckInOption', backref='check_in', lazy=True)

    def __repr__(self):
        return f"<CheckIn {self.title}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            title=self.title, 
            title_sw=self.title_sw,
            options=[option.to_dict() for option in self.options]
        )
    

class CheckInOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    text_sw = db.Column(db.String(), nullable=False)
    checkin_id = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)

    def __repr__(self):
        return f"<CheckInOption {self.text}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            text=self.text, 
            text_sw=self.text_sw,
            checkin_id=self.checkin_id
        )


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    title_sw = db.Column(db.String(), nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    questions = db.relationship('AssessmentQuestion', backref='assessment', lazy=True)
    scores = db.relationship('UserScores', backref='assessment', lazy=True)

    def __repr__(self):
        return f"<Assessment {self.title}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            title=self.title,
            title_sw=self.title_sw,
            max_score=self.max_score,
            questions=[question.to_dict() for question in self.questions]
        )


class AssessmentQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    text_sw = db.Column(db.String(), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    options = db.relationship('AssessmentOption', backref='assessment_question', lazy=True)

    def __repr__(self):
        return f"<AssessmentQuestion {self.text}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            text=self.text, 
            text_sw=self.text_sw,
            assessment_id=self.assessment_id,
            options=[option.to_dict() for option in self.options]
        )
    

class AssessmentOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    text_sw = db.Column(db.String(), nullable=False)
    value = db.Column(db.Integer, nullable=False) # 0, 1, 2, 3...
    assessment_question_id = db.Column(db.Integer, db.ForeignKey('assessment_question.id'), nullable=False)

    def __repr__(self):
        return f"<AssessmentOption {self.text}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            text=self.text, 
            text_sw=self.text_sw,
            value=self.value,
            assessment_question_id=self.assessment_question_id
        )


class UserScores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    age_group = db.Column(db.String(6), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)

    def __repr__(self):
        return f"<UserScores {self.user_id} {self.assessment_id}>"
    
    def to_dict(self):
        return dict(
            id=self.id, 
            user_id=self.user_id, 
            assessment_id=self.assessment_id,
            score=self.score,
            date_taken=self.date_taken.strftime("%Y-%m-%d")
        )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
