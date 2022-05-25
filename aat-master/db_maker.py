from datetime import datetime
from my_flask_app import db
from my_flask_app.models import Assessment, User, Question, Questionset, Result, Student, Question2

db.drop_all()
db.create_all()

# Jern
user1 = User(firstname="user1", username="user1@test.ac.uk",
             password="passuser1",profilePic='hud_p1.png',
             ownedBadges='',
             ownedBackgrounds='',
             user_highestMark=76.4,
             user_averageMark=0,
             total_tests_completed=4,
             summative_tests_completed=0,
             formative_tests_completed=0,
             points=3,
             #breaks the submit page WS
             score=None,
             summative_mark='',
             formative_mark='')


user2 = User(firstname="user2", username="user2@test.ac.uk",
             password="passuser2",profilePic='hud_p1.png',
             ownedBadges='',
             ownedBackgrounds='',
             user_highestMark=64.3,
             user_averageMark=0,
             total_tests_completed=10,
             summative_tests_completed=0,
             formative_tests_completed=0,
             points=15,
             #breaks the sumbit page WS
             score=0,
             summative_mark='',
             formative_mark='')


# Jern
q1 = Question(question="In what circumstances is an economy said to be in recession?", 
option1="A. If real GDP falls in one quarter compared with the quarter before.", 
option2="B. If real GDP falls for two consecutive quarters.", 
option3="C. If real GDP falls in one year compared with the year before.",
option4="D. If real GDP falls for two consecutive years.", 
answer="B. If real GDP falls for two consecutive quarters.", 
feedback="Statement B is correct: this is the definition of a recession used by economists.", 
level="Beginner", 
tag="Macroeconomics", 
point=2)

q2 = Question(question="Which of the following statements is false?",
option1="A. The GDP deflator is a price index that covers all goods and services included in GDP.", 
option2="B. The RPI is a price index that covers a wide range of goods and services bought by households.",
option3="C. The CPI is a price index that covers a wide range of goods and services bought by households.", 
option4="D. The CPI generally rises more quickly than the RPI.", 
answer="D. The CPI generally rises more quickly than the RPI.", 
feedback="Statement D is false. The CPI generally rises more slowly than the RPI.", 
level="Intermediate", 
tag="Macroeconomics", 
point=4)

q3 = Question(question="Which of the following would cause a bank to lose reserves?",
option1="A. One of the bank's depositors makes an internet payment to another of its depositors.",
option2="B. One of the bank's depositors pays out a cheque to another of its depositors.", 
option3="C. One of the bank's depositors pays out a cheque to a depositor of another bank.",
option4="D. The bank raises the interest rate it pays on deposits.", 
answer="C. One of the bank's depositors pays out a cheque to a depositor of another bank.", 
feedback="Statement C is correct. In this case, the bank must give reserves to the bank of the person who receives the cheque.", 
level="Beginner", 
tag="Banking", 
point=2)

q4 = Question(question="Which of the following would not shift the money demand curve to the right?", option1="A. A move which means that all workers who were in the past paid weekly will in future be paid monthly.", option2="B. A rise in incomes.", option3="C. A rise in wealth.",
              option4="D. A fall in the interest rate.", answer="D. A fall in the interest rate.", feedback="Statement D is correct. The effect on the quantity of money demanded of a change in the interest rate is shown by a move along the money demand curve, not by a shift of the curve.", level="Beginner", tag="Banking", point=2)

q5 = Question(question="On which of the following do Keynesians and monetarists agree?", option1="A. The most important cause of demand shocks is changes in the money stock.", option2="B. The demand for money is interest elastic.", option3="C. Output departs at times from potential output because of demand shocks.", option4="D. When there is a recessionary gap, flexible wages will return the labour market to equilibrium fairly quickly.",
              answer="C. Output departs at times from potential output because of demand shocks.", feedback="Statement C is correct. Regarding statement a, Keynesians believe other causes of shocks are more important. Regarding statement b, monetarists believe the demand for money is interest inelastic. Regarding statement d Keynesians believe wages are not very flexible.", level="Advanced", tag="Business Cycle", point=4)

q6 = Question(question="In this question, ignore new classical economists who propose real business cycle theory. Which of the following statements is false?", option1="A. On the new Keynesian view, a single unexpected demand shock could take output below the potential level.", option2="B. On the new Keynesian view, it needs repeated unexpected demand shocks to take output below the potential level for long periods.", option3="C. On the new classical view, it needs an unexpected demand shock to take output below the potential level.",
              option4="D. On the new classical view, it needs repeated unexpected demand shocks to take output below the potential level for long periods.", answer="B. On the new Keynesian view, it needs repeated unexpected demand shocks to take output below the potential level for long periods.", feedback="Statement B is false. Owing to an assumption of sticky wages, new Keynesians believe that a single shock could lead to output being below the potential level for a long period.", level="Intermediate", tag="Business Cycle", point=3)

q7 = Question(question="Suppose inflation over the next year is expected to be 5%, and assume there are no supply shocks. What rate of inflation will the short-run Phillips curve show at the natural rate of unemployment?", option1="A. 0%", option2="B. Between 0% and 5%",
              option3="C. 5%", option4="Over 5%", answer="C. 5%", feedback="Statement C is correct. In the absence of supply shocks, the short-run Phillips curve always shows the expected rate of inflation at the natural rate of unemployment.", level="Beginner", tag="Inflation", point=2)

q8 = Question(question="Which of the following explains why the long-run Phillips curve is drawn as a vertical line?", option1="A. Because in the long run, government policies will ensure that unemployment is at its natural rate.", option2="B. Because in the long run, the labour market will settle so that unemployment is at its natural rate.", option3="C. Because of the quantity theory of money.",
              option4="D. Because its true shape is unknown.", answer="B. Because in the long run, the labour market will settle so that unemployment is at its natural rate.", feedback="Statement B is correct. In the long run unemployment will be at the natural rate, while the inflation rate could be anything, depending chiefly on the rate of growth of the money stock and the rate of growth of real output.", level="Advanced", tag="Inflation", point=5)

q9 = Question(question="Suppose the labour market is away from equilibrium, with unemployment above the natural rate. The new Keynesian view of inflation and unemployment offers several reasons why the labour market can stay away from equilibrium for long periods. Which of the following is not one of these reasons?", option1="A. Efficiency wages may hold wages below the equilibrium level.", option2="B. Workers may resist wage cuts which reduce their wages below those paid to other workers in the same occupation.",
              option3="C. Prices may be sticky downwards in some markets because consumers prefer stable prices.", option4="D. Prices may be sticky downwards in some markets because consumers may judge quality by price.", answer="A. Efficiency wages may hold wages below the equilibrium level.", feedback="Statement A is not one of the reasons for believing the labour market may take a long time to reach equilibrium; instead, efficiency wages cause a problem because it is believed that they may hold the wage rate above the equilibrium level, not below it.", level="Advanced", tag="Inflation", point=5)

q10 = Question(question="Suppose a market is in equilibrium, and then the demand increases. Which of the following would be shown on a graph that illustrated the effects?", option1="A. An excess demand at the initial equilibrium price.", option2="B. An excess demand at the new equilibrium price.", option3="C. An excess supply at the initial equilibrium price.", option4="D. An excess supply at the new equilibrium price.   ",
               answer="A. An excess demand at the initial equilibrium price.", feedback="Statement A shows what would be shown on a graph. Statement b is incorrect because there will be no excess demand, or indeed an excess supply, at the new equilibrium price. Statements c and d are incorrect because there will be no excess supply.", level="Intermediate", tag="Supply and Demand", point=3)


# Gaia
q1a = Question2(
    text="A Business Model is a method of doing business by which a company generates revenue to sustain itself.", option2a="True", option2b="False",
    answer2="True",
    feedback2="The correct answer is True. For further information about the topic refer to week 4 content. Additional information can be found on http://digitalenterprise.org/models/models.html?msclkid=a3d6681aaa9b11eca8d2262cd5bd96d0",
    level2="Intermediate", point2=7, tag2="Software Engineering")

# Gaia
q1b = Question2(
    text="According to Gartner, Plateau of Expectation is one of the five phases of a technology.", option2a="True", option2b="False",
    answer2="False",
    feedback2="The correct answer is False. According to Gartner, Plateau of Productivity is one of the five phases of a technology. For further information about the topic refer to week 4 content. Additional information can be found on https://www.gartner.com/en/research/methodologies/gartner-hype-cycle?msclkid=f031f98faa9c11ec946ff60371c5693a",
    level2="Beginner", point2=3, tag2="Software Engineering"
)

# Gaia
q1c = Question2(
    text="PRINCE2 is a methodology that describes methods, processes, techniques and tools that can be applied to achieve objectives.", option2a="True", option2b="False", answer2="True", feedback2="The correct answer is True. For further information about the topic refer to week 5 content.", level2="Intermediate", point2=7, tag2="Project Management"
)

# Gaia
q1d = Question2(
    text="Swarm programming involves two programmers working together.", option2a="True", option2b="False",
    answer2="False",
    feedback2="The correct answer is False. Swarm programming is pair programming with more than two programmers. For further information about the topic refer to content delivered in week 4 of spring semester.",
    level2="Beginner", point2=3, tag2="Agile technique"
)

# Gaia
q1e = Question2(
    text="Conclusion is one of the 5 steps identified by Gibb.", option2a="True", option2b="False",
    answer2="False",
    feedback2="The correct answer is False. Conclusion is one of the steps in the Gibb's 6-step model. For further information about the topic refer to content delivered in week 9 of spring semester. The topic can be deepen by reading Gibbs, G. (1988). Learning by Doing: A Guide to Teaching and Learning Methods. Oxford: Oxford Further Education Unit.",
    level2="Advanced", point2=10, tag2="Reflective writing"
)

# Samuel
qs1 = Questionset(set_no=1, question_id=1)
qs2 = Questionset(set_no=1, question_id=2)
qs3 = Questionset(set_no=1, question_id2=1)
a1 = Assessment(assessment_name="CW1", module_id="CMT001", start_date=datetime(2022,4,1,9), end_date=datetime(2022,5,1,9,30), question_set_no=1, comment="Testing Comment", assessment_type="Formative")


# TestStudent = Student()
Result1 = Result(cohort="Cohort1", assesment="Assesment1",
                 student_id="Johnny", score=32)
Result2 = Result(cohort="Cohort2", assesment="Assesment2",
                 student_id="Sarah", score=16)
Result3 = Result(cohort="Cohort3", assesment="Assesment3",
                 student_id="Mike", score=2)
Result4 = Result(cohort="Cohort4", assesment="Assesment4",
                 student_id="Jack", score=72)


db.session.add(Result1)
db.session.add(Result2)
db.session.add(Result3)
db.session.add(Result4)
# Jern
db.session.add(user1)
db.session.add(user2)
db.session.add(q1)
db.session.add(q2)
db.session.add(q3)
db.session.add(q4)
db.session.add(q5)
db.session.add(q6)
db.session.add(q7)
db.session.add(q8)
db.session.add(q9)
db.session.add(q10)


# Gaia
db.session.add(q1a)
db.session.add(q1b)
db.session.add(q1c)
db.session.add(q1d)
db.session.add(q1e)
# Samuel
db.session.add(qs1)
db.session.add(qs2)
db.session.add(qs3)
db.session.add(a1)


db.session.commit()
