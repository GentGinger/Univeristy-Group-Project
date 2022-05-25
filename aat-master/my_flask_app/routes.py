from distutils.log import info
from shutil import _ntuple_diskusage
from flask import render_template, url_for, request, redirect, flash
from wtforms.widgets.core import html_params
from wtforms import StringField, PasswordField, SubmitField, RadioField,BooleanField, DateTimeField, SelectField, TextAreaField
from my_flask_app import app,db
from my_flask_app.models import Questionset, User,Question, Assessment, Result, Student, Question2, CommentModel, changePP
from my_flask_app.forms import LoginForm,QuestionForm,FilterForm,EditForm, TestForm, AssessmentCreateForm, StatsForm, QuestionForm2, FilterForm2, AddCommentForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, null

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/login",methods=['GET','POST'])
def login():
  #Making page only accessible for guests
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()

  #Logs in registered user
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user,remember=form.remember_me.data)
      flash('You\'ve successfully logged in!')
      return redirect(url_for('home'))
    flash('Incorrect email or password supplied.')
    return redirect(url_for('login_error'))
  return render_template('login.html',title='Login', form=form)


@app.route("/login_error",methods=['GET','POST'])
def login_error():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()

   #Logs in registered users
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('You\'ve successfully logged in!')
      return redirect(url_for('home'))
    flash('Incorrect email or password supplied.') 
  return render_template('login_error.html',title='Login_error', form=form)


@app.route("/logout")
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
  return render_template('account.html',title='Account')

#Jern
@app.route("/test", methods=['POST','GET'])
def test():

  questions_list=Question.query.order_by(Question.q_id.asc()).all()
    
  return render_template("test.html",title="Test",questions_list=questions_list)

#Jern
@app.route("/submittest", methods=["POST", "GET"])
@login_required
def submittest():
    total_questions = Question.query.order_by(Question.q_id.asc()).count()
    questions_list = Question.query.order_by(Question.q_id.asc()).all()
    answered_questions_list = []
    count = 0
    for question in questions_list:
        answered_question = request.form[str(question.q_id)]
        answered_questions_list.append(
            {"answered_question": answered_question, "question": question}
        )
        if question.answer == answered_question:
            count += 1
    tests = User.query.filter_by(username=current_user.username).first()
    tests.total_tests_completed += 1
    tests.points += 3
    db.session.commit()

    return render_template(
        "submittest.html",
        title="testresults",
        questions_list=questions_list,
        count=count,
        answered_questions_list=answered_questions_list,
        total_questions=total_questions,
    )

#Jern
@app.route("/edit_question1", methods=["POST", "GET"])
@login_required
def edit_question1():
  form=FilterForm()

  level=request.args.get("level")
  tag=request.args.get("tag")
  query=Question.query

  if level=="All" and tag=="All":
    query=Question.query.order_by(Question.q_id.asc())
  elif level and tag=="All":
    query=query.filter(Question.level == level)
  elif level=="All" and tag:
    query=query.filter(Question.tag== tag)
  elif level and tag:
    query=query.filter(Question.level == level,Question.tag== tag)
  else:
    query=Question.query.order_by(Question.q_id.asc())

  questions_list=query.all()

  return render_template("edit_question1.html", title="edit_question1", questions_list=questions_list, form=form)

#Jern
@app.route("/newtest", methods=["POST", "GET"])
@login_required
def newtest():    
  form=QuestionForm()
  if form.validate_on_submit():
    question=Question(question=form.question.data,option1=form.option1.data,option2=form.option2.data,option3=form.option3.data,option4=form.option4.data,answer=form.answer.data,feedback=form.feedback.data,level=form.level.data,tag=form.tag.data,point=form.point.data)
    db.session.add(question)
    db.session.commit()
    flash("Question has been added!", "success")
    return redirect(url_for("edit_question1"))
  return render_template("newtest.html", title="NewTest", form=form)

#Jern
@app.route("/question/<int:q_id>", methods=["POST", "GET"])
@login_required
def question(q_id):
    question = Question.query.get_or_404(q_id)
    form = EditForm()
    if form.validate_on_submit():
        question.question = form.question.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.answer = form.answer.data
        question.feedback = form.feedback.data
        question.level=form.level.data
        question.tag=form.tag.data
        question.point=form.point.data
        db.session.commit()
        flash("Updated")
        return redirect(url_for("question", q_id=question.q_id))
    elif request.method == "GET":
        form.question.data = question.question
        form.option1.data = question.option1
        form.option2.data = question.option2
        form.option3.data = question.option3
        form.option4.data = question.option4
        form.answer.data = question.answer
        form.feedback.data = question.feedback
        form.level.data=question.level
        form.tag.data= question.tag
        form.point.data=question.point
    
    return render_template(
        "question.html", title="Question", question=question, form=form
    )

#Jern
@app.route("/delete/<int:q_id>", methods=["POST"])
@login_required
def delete(q_id):
    questions_list = Question.query.order_by(Question.q_id.asc()).all()
    question = Question.query.get_or_404(q_id)

    db.session.delete(question)
    db.session.commit()

    flash("Question has been deleted.")
    return redirect(url_for('edit_question1'))

# Gaia - Creating route to show type2 questions.
@app.route("/show_question2", methods=["POST", "GET"])
def show_question2():
  form=FilterForm2()

  level2=request.args.get("level2")
  tag2=request.args.get("tag2")
  query=Question2.query

  if level2=="All" and tag2=="All":
    query=Question2.query.order_by(Question2.id.asc())
  elif level2 and tag2=="All":
    query=query.filter(Question2.level2 == level2)
  elif level2=="All" and tag2:
    query=query.filter(Question2.tag2== tag2)
  elif level2 and tag2:
    query=query.filter(Question2.level2 == level2, Question2.tag2== tag2)
  else:
    query=Question2.query.order_by(Question2.id.asc())

  questions2_list=query.all()

  return render_template("show_question2.html", title="show_question2", questions2_list=questions2_list, form=form)

# Gaia - Creating route to create type2 questions.
@app.route("/add_question2", methods=["GET", "POST"])
def add_question2():
    form = QuestionForm2()
    questions = Question2.query.all()

    if form.validate_on_submit():
        question2 = Question2(
            text=form.text.data,
            option2a=form.option2a.data,
            option2b=form.option2b.data,
            answer2=form.answer2.data,
            feedback2=form.feedback2.data,
            level2=form.level2.data, point2=form.point2.data, tag2=form.tag2.data
        )
        form.text.data = ""
        form.option2a.data = "True"
        form.option2b.data = "False"
        form.answer2.data = ""
        form.feedback2.data = ""
        form.level2.data = ["Beginner", "Intermediate", "Advanced"]
        form.point2.data = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        form.tag2.data = ""
        # Add question data to database
        db.session.add(question2)
        db.session.commit()
        # Return a message
        flash("Question created successfully!", category="success")
        return redirect(url_for("show_question2"))
    # Redirect to the page
    return render_template("add_question2.html", form=form, questions=questions)


# Gaia - Creating route to delete type2 questions.
@app.route("/delete-question/<int:id>")
def delete_question(id):
    question2 = Question2.query.filter_by(id=id).first()

    if not question:
        flash("Question does not exist.", category="error")
    else:
        db.session.delete(question2)
        db.session.commit()
        flash("Question deleted!", category="success")

    return redirect(url_for("show_question2"))


# Gaia - Creating route to edit type2 questions.
@app.route("/edit-question/<int:id>", methods=["GET", "POST"])
def edit_question(id):
    question2 = Question2.query.get_or_404(id)
    form = QuestionForm2()

    if form.validate_on_submit():
        question2.text = form.text.data
        question2.option2a = form.option2a.data
        question2.option2b = form.option2b.data
        question2.answer2 = form.answer2.data
        question2.feedback2 = form.feedback2.data
        question2.level2 = form.level2.data
        question2.point2 = form.point2.data
        question2.tag2 = form.tag2.data
        # Update database
        db.session.add(question2)
        db.session.commit()
        flash("Question has been edited!", category="success")
        # return redirect(url_for('add_question2', id=question.id))

    form.text.data = question2.text
    form.option2a.data = question2.option2a
    form.option2b.data = question2.option2b
    form.answer2.data = question2.answer2
    form.feedback2.data = question2.feedback2
    form.level2.data = question2.level2
    form.point2.data = question2.point2
    form.tag2.data = question2.tag2
    return render_template("edit_question2.html", form=form)
  

# @app.route("/submittest", methods=['POST','GET'])
# def submittest():
#   questions_list=Question.query.order_by(Question.q_id.asc()).all()
#   count=0
#   for question in questions_list:
#     question_id=str(question.q_id)
#     selected_option= request.form[question_id]
#     if question.answer == selected_option:
#         count +=1
    
#     count=str(count)
  
#   return render_template("submittest.html",title="testresults",questions_list=questions_list,count=count)
 
# Samuel. Create assessment from questions in database.
@app.route("/createassessment", methods=['POST','GET'])
@login_required
def createassessment():
  form = AssessmentCreateForm()
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  questions_list2=Question2.query.order_by(Question2.id.asc()).all()
  questionset_leng=(Questionset.query.order_by(Questionset.id.asc()).all())[-1].set_no+1

  if form.validate_on_submit():
    q_list = request.form.getlist('include_q')
    q_list2 = request.form.getlist('include_q2')
    print("q_list",q_list)
    print("q_list2",q_list2)
    i=1
    for question in questions_list:
      j=question.q_id
      if (str(j) in q_list):
        q_set = Questionset(set_no=questionset_leng,question_id=question.q_id)
        db.session.add(q_set)
        i+=1
    k=1
    for question in questions_list2:
      l=question.id
      if (str(l) in q_list2):
        q_set2 = Questionset(set_no=questionset_leng,question_id2=question.id)
        db.session.add(q_set2)
        k+=1
    assessment = Assessment(assessment_name=form.assessment_name.data, module_id=form.module_id.data, start_date=form.start_date.data, end_date=form.end_date.data, question_set_no=questionset_leng, comment=form.comment.data, assessment_type=form.assessment_type.data)
    db.session.add(assessment)
    db.session.commit()

    flash('Assessment has been created')

    return redirect(url_for('home'))
  return render_template('create_assessment.html',title='create_assessment', form=form, questions_list=questions_list, questions_list2=questions_list2)

# Samuel. View the assessment in the database.
@app.route("/viewassessment", methods=['POST','GET'])
@login_required
def viewassessment():
  assessment_list=Assessment.query.order_by(Assessment.assessment_id.asc()).all()
  question_list=Question.query.order_by(Question.q_id.asc()).all()
  question_list2=Question2.query.order_by(Question2.id.asc()).all()
  questionset=Questionset.query.all()
  return render_template('view_assessment.html',title='view_assessment', assessment_list=assessment_list, question_list=question_list, question_list2=question_list2, questionset=questionset)

# Samuel. Delete the assessment in the database.
@app.route("/deleteassessment/<int:assessment_id>", methods=['POST','GET'])
@login_required
def deleteassessment(assessment_id):
  assessment=Assessment.query.get_or_404(assessment_id)
  questionset=Questionset.query.filter_by(set_no=assessment.question_set_no).all()
  for q in questionset:
    db.session.delete(q)
  db.session.delete(assessment)
  db.session.commit()

  flash('Assessment has been deleted')

  return redirect(url_for('viewassessment'))

# Samuel. Edit the assessment in the database
@app.route("/editassessment/<int:assessment_id>", methods=['POST','GET'])
@login_required
def editassessment(assessment_id):
  assessment=Assessment.query.get_or_404(assessment_id)
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  questions_list2=Question2.query.order_by(Question2.id.asc()).all()
  form = AssessmentCreateForm()
  included_q=Questionset.query.filter_by(set_no=assessment.question_set_no).all()
  included_q_id=[]
  included_q2_id=[]
  for i in included_q:
    if not i.question_id == None:
      included_q_id.append(i.question_id)
  for i in included_q:
    if not i.question_id2 == None:
      included_q2_id.append(i.question_id2)

  if form.validate_on_submit():
    assessment.assessment_name=form.assessment_name.data
    assessment.module_id=form.module_id.data
    assessment.start_date=form.start_date.data
    assessment.end_date=form.end_date.data
    assessment.comment=form.comment.data
    assessment.assessment_type=form.assessment_type.data

    q_list = request.form.getlist('include_q')
    for question in questions_list:
      j=question.q_id
      if str(j) in q_list:
        if j not in included_q_id:
          q_set = Questionset(set_no=assessment.question_set_no,question_id=question.q_id)
          db.session.add(q_set)
      elif j in included_q_id:
        delete_set = Questionset.query.filter_by(set_no=assessment.question_set_no,question_id=question.q_id).first()
        delete_set.set_no=0
        d=Questionset.query.filter_by(set_no=0).first()
        db.session.delete(d)
    q_list2 = request.form.getlist('include_q2')
    for question in questions_list2:
      j=question.id
      if str(j) in q_list2:
        if j not in included_q2_id:
          q_set2 = Questionset(set_no=assessment.question_set_no,question_id2=question.id)
          db.session.add(q_set2)
      elif j in included_q2_id:
        delete_set = Questionset.query.filter_by(set_no=assessment.question_set_no,question_id2=question.id).first()
        delete_set.set_no=0
        d=Questionset.query.filter_by(set_no=0).first()
        db.session.delete(d)
    db.session.commit()
    flash('Assessment has been updated')
    return redirect(url_for('viewassessment'))
  elif request.method=='GET':
    form.assessment_name.data=assessment.assessment_name
    form.module_id.data=assessment.module_id
    form.start_date.data=assessment.start_date
    form.end_date.data=assessment.end_date
    form.comment.data=assessment.comment
    form.assessment_type.data=assessment.assessment_type

  return render_template('edit_assessment.html',title='edit_assessment', form=form, questions_list=questions_list, questions_list2=questions_list2, included_q_id=included_q_id, included_q2_id=included_q2_id)

@app.route('/stats', methods=['GET','POST'])
def stats():
  form = StatsForm()
  sum = 0
  n = 0
  stat = ""
  for i in Result.query.with_entities(Result):
    print(i)
  
  if form.is_submitted():
 
    value = request.form.get("cohorts")
    value1 = request.form.get("students")
    value2 = request.form.get("assesements")
    if value == 'AllCohort':
      if value2 == 'AllTest':
        print(1)
        cumulativeScore = Result.query.with_entities(Result.score)
      else:
        print(2)
        cumulativeScore = Result.query.with_entities(Result.score).filter_by(assesment = value2)
    # if value == 'AllStu':
    #   if value2 == 'AllTest':
    #     cumulativeScore = Result.query.with_entities(Result.score)
    #   else:
    #     cumulativeScore = Result.query.with_entities(Result.score).filter_by(student = value2)
    else: 
      cumulativeScore = Result.query.with_entities(Result.score).filter_by(assesment = value2).filter_by(cohort = value)

    print(value,value2)
    for i in cumulativeScore:
      print(i)
      sum = sum + i[0]
      n = n + 1
      stat = sum/n
    if stat == "":
      stat = 'No Results in Selected Parameters'


  return render_template('stats.html', title="stats", form = form, stat = stat)

#Williams

@app.route("/assessments", methods=['POST','GET'])
@login_required
def assessments():


    
    return render_template("assessments.html",title="Assessments")
    
@app.route("/summative", methods=['POST','GET'])
@login_required
def summative():
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  if current_user.is_authenticated:
    
    return render_template("summative.html",title="Summative", questions_list=questions_list)

@app.route("/submitsummative", methods=["POST", "GET"])
@login_required
def submitsummative():
  
    # current_user = User(request.form['score'])
    total_questions = Question.query.order_by(Question.q_id.asc()).count()
    questions_list = Question.query.order_by(Question.q_id.asc()).all()
    question_point=Question2.query.order_by(Question2.id.asc()).count()
    answered_questions_list = []
    score = 0
    count = 0
    correct = 0
    incorrect =0


    for question in questions_list:
        answered_question = request.form[str(question.q_id)]
        # question_point = request.form[int(question.point)]
        answered_questions_list.append(
            {"answered_question": answered_question, "question": question}
        )
        
        if question.answer == answered_question:
            count += 1
        if question.answer == answered_question:
            score+=question.point
            print('Score')
        if question.answer != answered_question:
          incorrect == True
        else:
          correct == False

            
       
    # tests = User.query.filter_by(username=current_user.username).first()
    # tests.total_tests_completed += 1
    # tests.summative_tests_completed += 1
    # tests.points += 3

    new_result = Result(cohort='Summative_Test_Cohort', student_id ='Summative_Test_Student', score=score, assesment = 'Summative_Test_Assesment_1' )
    db.session.add(new_result)
    db.session.commit()
        
    flash("Answers submitted!", "info")
    return render_template("submitsummative.html", title="testresults", questions_list=questions_list, count=count, answered_questions_list=answered_questions_list,total_questions=total_questions,answered_question=answered_question, score=score, question_point=question_point,incorrect=incorrect, correct=correct)
    

@app.route("/formative", methods=['POST','GET'])
@login_required
def formative():
  questions_list=Question2.query.order_by(Question2.id.asc()).all()
  if current_user.is_authenticated:


    return render_template("formative.html",title="Formative",questions_list=questions_list)

@app.route("/submitformative", methods=["POST", "GET"])
@login_required
def submitformative():
    total_questions = Question2.query.order_by(Question2.id.asc()).count()
    questions_list = Question2.query.order_by(Question2.id.asc()).all()
    question_point2=Question2.query.order_by(Question2.id.asc()).count()
    answered_questions_list = []
    count = 0
    score = 0
    correct = 0

    for text in questions_list:
        answered_question = request.form[str(text.id)]
        #question_point2 = request.form[int(text.point2)]
        answered_questions_list.append(
            {"answered_question": answered_question, "question": text}
        )
        if text.answer2 == answered_question:
            count += 1
        if text.answer2 == answered_question:
          score+=text.point2


    #So Ive hard coded the cohort and student id as they said login functionality dosnt matter? but the score is dynamic based on the test
    new_result = Result(cohort='Formative_Test_Cohort', student_id ='Formative_Test_Student', score=score, assesment = 'Formative_Test_Assesment1' )
    db.session.add(new_result)
    db.session.commit()
 
          
  
    tests = User.query.filter_by(username=current_user.username).first()
    tests.total_tests_completed += 1
    tests.formative_tests_completed += 1
    tests.points += 3
    db.session.commit()
    flash("Answers submitted!", "info")
    return render_template( "submitformative.html", title="testresults", questions_list=questions_list, count=count, answered_questions_list=answered_questions_list,total_questions=total_questions, answered_question=answered_question, score=score, question_point2=question_point2, correct=correct)

#Ruiwen
@app.route("/comment", methods=['POST','GET'])
@login_required
def comment():  
  comment_list=CommentModel.query.all()  
  form=AddCommentForm()
  if form.validate_on_submit():
    comment_list=CommentModel.query.all()  
    content = form.content.data
    comment_model = CommentModel(content=content)    
    comment_model.author = current_user
    db.session.add(comment_model)
    db.session.commit()
    flash('Comment success!','success')
    return redirect(url_for('comment'))
  return render_template("comment.html",title="Comment",form=form,comment_list=comment_list)

@app.route("/tables")
@login_required
def tables():
  users = User.query.order_by(User.firstname).all()
  return render_template('tables.html', users=users)

@app.route("/account/<coin>")
@login_required
def profilePic(coin):
  changePP(coin)
  return render_template('account.html')

@app.route("/store")
@login_required
def store():
  return render_template('store.html', title = 'store')

@app.route("/store/<badge>")
@login_required
def storechange(badge):
  changePP(badge)
  return render_template('store.html')

@app.route("/store/buyG")
@login_required
def storebuy():
  tests = User.query.filter_by(username=current_user.username).first()
  tests.points -= 3
  tests.ownedBadges += 'G'
  db.session.commit()
  return render_template('store.html', tests=tests)

@app.route("/store/buyB")
@login_required
def storebuyb():
  tests = User.query.filter_by(username=current_user.username).first()
  tests.points -= 3
  tests.ownedBadges += 'B'
  db.session.commit()
  return render_template('store.html', tests=tests)

@app.route("/store/buyP")
@login_required
def storebuyp():
  tests = User.query.filter_by(username=current_user.username).first()
  tests.points -= 3
  tests.ownedBadges += 'P'
  db.session.commit()
  return render_template('store.html', tests=tests)

@app.route("/store/buyBB")
@login_required
def storebuybb():
  tests = User.query.filter_by(username=current_user.username).first()
  tests.points -= 3
  tests.ownedBackgrounds += 'B'
  db.session.commit()
  return render_template('store.html', tests=tests)

@app.route("/store/buyBG")
@login_required
def storebuybg():
  tests = User.query.filter_by(username=current_user.username).first()
  tests.points -= 3
  tests.ownedBackgrounds += 'G'
  db.session.commit()
  return render_template('store.html', tests=tests)
