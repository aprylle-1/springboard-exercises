from crypt import methods
from urllib import response
from flask import Flask, request, render_template, redirect, flash
from flask import session
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool12345"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def root():
    """Goes to Home Page - Shows List of Surveys"""
    return render_template('home.html', surveys = surveys)

@app.route("/set-session", methods = ["POST"])
def set_session():
    session['responses'] = []
    return redirect ("/questions/0")

@app.route("/questions/<question_number>")
def generate_question(question_number):
    """Generates Question for User"""
    question_number = int(question_number)
    questions_length = len(surveys['satisfaction'].questions)
    responses = session['responses']
    curr_responses = len(responses)
    print(curr_responses)
    if curr_responses == questions_length:
        return redirect('/end')
    if question_number > curr_responses:
        flash ("You went out of order! This is your next question!", 'error')
        return redirect(f'/questions/{curr_responses}')
    if question_number < curr_responses:
        flash ("You already answered that question.", "error")
        return redirect(f'/questions/{curr_responses}') 
    if question_number < len(surveys['satisfaction'].questions):
        title = surveys['satisfaction'].title
        question = surveys['satisfaction'].questions[question_number].question
        choices = surveys['satisfaction'].questions[question_number].choices
        return render_template('question.html', title = title, question = question, choices = choices, question_number = question_number)
    return redirect('/end')

@app.route("/answer", methods=["POST"])
def save_answer():
    """Appends answer to fake DB responses"""
    answer = request.form.get('answer', 'none')
    question_number = int(request.form['question_number'])
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    return redirect(f'/questions/{question_number + 1}')

@app.route("/end")
def end_survey():
    """End of Survey - Shows user their responses"""
    questions_length = len(surveys['satisfaction'].questions)
    questions = surveys['satisfaction'].questions
    responses = session['responses']
    return render_template('end.html', responses = responses, questions=questions, questions_length = questions_length)