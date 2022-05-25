from datetime import datetime
from email.policy import default
from my_flask_app import db, login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    profilePic= db.Column(db.String(120), nullable=False) 
    user_highestMark = db.Column(db.Float, nullable = True)
    user_averageMark = db.Column(db.Float, nullable = True)
    total_tests_completed = db.Column(db.Integer, nullable = True)
    summative_tests_completed = db.Column(db.Integer, nullable = True)
    formative_tests_completed = db.Column(db.Integer, nullable = True)
    points = db.Column(db.Integer, nullable = True)
    ownedBadges = db.Column(db.String(120), nullable=True)
    ownedBackgrounds = db.Column(db.String(120), nullable=True)
    hashed_password = db.Column(db.String(128))
    #breaks the submit page WS
    summative_mark = db.Column(db.Integer, nullable = True)
    formative_mark = db.Column(db.Integer, nullable = True)
    score = db.Column(db.Integer, nullable = True)
    

    def __repr__(self):
        return f"User('{self.firstname}','{self.username}','{self.score}')"

    # adated from Grinberg(2014, 2018)

    @property
    def password(self):
         raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
         self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# Jern


class Question(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), unique=False, nullable=False)
    option1 = db.Column(db.String(128), unique=False, nullable=False)
    option2 = db.Column(db.String(128), unique=False, nullable=False)
    option3 = db.Column(db.String(128), unique=False, nullable=False)
    option4 = db.Column(db.String(128), unique=False, nullable=False)
    answer = db.Column(db.String(128), unique=False, nullable=False)
    feedback = db.Column(db.String(300), unique=False, nullable=False)
    level = db.Column(db.String(20), unique=False, nullable=False)
    tag = db.Column(db.String(20), unique=False, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    questionset = db.relationship("Questionset", back_populates="questions")

# Gaia
class Question2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    option2a = db.Column(db.Text, nullable=False)
    option2b = db.Column(db.Text, nullable=False)
    answer2 = db.Column(db.Text, nullable=False)
    feedback2 = db.Column(db.Text, nullable=False)
    level2 = db.Column(db.String(50), nullable=False)
    point2 = db.Column(db.Integer, nullable=False)
    tag2 = db.Column(db.Text, nullable=False)
    questionset = db.relationship("Questionset", back_populates="questions2")

# Samuel. Table that linkup multiple questions with multiple assessments.
class Questionset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_no = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey("question.q_id"))
    question_id2 = db.Column(db.Integer, db.ForeignKey("question2.id"))
    questions = db.relationship("Question", back_populates="questionset")
    questions2 = db.relationship("Question2", back_populates="questionset")

    assessments = db.relationship("Assessment", back_populates="questionsets")

# Samuel. Table for storing data of assessment.
class Assessment(db.Model):
    assessment_id = db.Column(db.Integer, primary_key=True)
    assessment_name = db.Column(db.String(50), nullable=False)
    module_id = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    comment = db.Column(db.String(300))
    assessment_type = db.Column(db.String)
    question_set_no = db.Column(db.Integer, db.ForeignKey("questionset.set_no"))
    questionsets = db.relationship("Questionset", back_populates="assessments")

class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cohort = db.Column(db.Integer, primary_key=True)
  result = db.Column(db.Integer, db.ForeignKey('result.score'), nullable=True)

  
class Result(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cohort = db.Column(db.Integer, db.ForeignKey('student.cohort'))
  assesment = db.Column(db.Integer)
  student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
  score = db.Column(db.Integer)
  # timetaken = db.Column(db.Integer, primary_key=True)

#Ruiwen
class CommentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='comments')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def changePP(badge):
  tests = User.query.filter_by(username=current_user.username).first()
  str(badge)
  badge = badge.strip('<>')
  tests.profilePic = badge + ".png"
  db.session.commit()
