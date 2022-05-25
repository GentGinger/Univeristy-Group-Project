from pstats import Stats
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField,BooleanField, DateTimeField, SelectField, TextAreaField
from my_flask_app import app,db
from my_flask_app.models import Questionset, User,Question, Assessment, Result, Student, Question2
from wtforms.validators import DataRequired
from my_flask_app.models import User, Question, Assessment
from flask_login import current_user
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TestForm(FlaskForm):
    radio = RadioField('Label', choices=[
                       (Question.option1, Question.option1), ('value_two', 'v2')])

# Jern


class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    option1 = StringField('Option1', validators=[DataRequired()])
    option2 = StringField('Option2', validators=[DataRequired()])
    option3 = StringField('Option3', validators=[DataRequired()])
    option4 = StringField('Option4', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    level = SelectField('Level', choices=[(
        "Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    tag = StringField('Tag',validators=[DataRequired()])
    point = SelectField("Choose points for this question:", choices=[(
        1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])
    submit = SubmitField('Update')

# Jern


class EditForm(FlaskForm):
    question = TextAreaField('Question')
    option1 = StringField('Option1')
    option2 = StringField('Option2')
    option3 = StringField('Option3')
    option4 = StringField('Option4')
    answer = StringField('Answer')
    feedback = TextAreaField('Feedback')
    level = SelectField('Level', choices=[(
        "Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    tag = StringField('Tag')
    point = SelectField("Choose points for this question:", choices=[(
        1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])
    submit = SubmitField('Submit')

# Jern


class FilterForm(FlaskForm):
    level = SelectField('Level', choices=[("All", "All(Level)"), (
        "Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    tag = SelectField('Tag', choices=[("All", "All(Tag)"), ("Macroeconomics", "Macroeconomics"), ("Banking", "Banking"), (
        "Business Cycle", "Business Cycle"), ("Inflation", "Inflation"), ("Supply and Demand", "Supply and Demand")])
    submit = SubmitField('Filter')


# Gaia
class QuestionForm2(FlaskForm):
    text = StringField("Question Text:", validators=[DataRequired()], widget=TextArea())
    option2a = StringField("Option 1 (type True):", validators=[DataRequired()])
    option2b = StringField("Option 2 (type False):", validators=[DataRequired()])
    answer2 = StringField("Correct Answer:", validators=[DataRequired()])
    feedback2 = StringField("Feedback:", validators=[DataRequired()])
    level2 = SelectField(
        "Choose a level of difficulty:",
        choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")],
    )
    point2 = SelectField("Choose points for this question:", choices=[("1", "1"), ("2", "2"), (
        "3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")])
    tag2 = StringField("Tag:", validators=[DataRequired()])
    submit2 = SubmitField("Submit")

# Gaia 
class FilterForm2(FlaskForm):
    level2 = SelectField('Level', choices=[("All", "All(Level)"), (
        "Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    tag2 = SelectField('Tag', choices=[("All", "All(Tag)"), ("Software Engineering", "Software Engineering"), ("Agile technique", "Agile technique"), (
        "Project Management", "Project Management"), ("Reflective writing", "Reflective writing")])
    submit = SubmitField('Filter')

# Samuel. For creating assessment.


class AssessmentCreateForm(FlaskForm):
  assessment_name = StringField('Assessment Title', validators=[DataRequired()])
  module_id = StringField('Module ID', validators=[DataRequired()])
  start_date = DateTimeField('Start Date and Time (Format: day-month-year hour-minuter; eg. 3-5-2022 8:30)', format='%d-%m-%Y %H:%M')
  end_date = DateTimeField('End Date and Time (Format: day-month-year hour-minuter; eg. 3-5-2022 11:45)', format='%d-%m-%Y %H:%M')
  comment = TextAreaField('General Comment')
  assessment_type = RadioField('Assessment Type', choices=[('Summative','Summative'),('Formative','Formative')])


class StatsForm(FlaskForm):
    try:
      cohorts = SelectField(choices=None)
      students = SelectField(choices=None)
      assesements = SelectField(choices=None)
      submit = SubmitField("Submit")
    except:
      print('This is fine')
    
    def __init__(self):
      super(StatsForm, self).__init__()
      self.cohorts.choices = list(dict.fromkeys([(str(cohort[0]),str(cohort[0])) for cohort in Result.query.with_entities(Result.cohort)]))

      self.students.choices =  list(dict.fromkeys([(str(student[0]),str(student[0])) for student in Result.query.with_entities(Result.student_id)]))

      self.assesements.choices =  list(dict.fromkeys([(str(assesment[0]),str(assesment[0])) for assesment in Result.query.with_entities(Result.assesment)]))

      self.students.choices.insert(0,('AllTest', 'All Assesments'))
      self.cohorts.choices.insert(0,('AllCohort','All Cohorts'))
      self.assesements.choices.insert (0,('AllTest', 'All Assesments'))
      

# Ruiwen
class AddCommentForm(FlaskForm):
  content = TextAreaField('Comment content',validators=[DataRequired()])
  submit = SubmitField('Post a comment')
