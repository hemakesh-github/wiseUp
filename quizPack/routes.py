from copy import copy
from flask import jsonify, render_template, request, url_for, session
from flask_login import logout_user
from quizPack import app, login_manager, bcrypt, db
from quizPack import utils
from quizPack.forms import LoginForm, RegisterForm
from quizPack.models import User



@app.route("/", methods = ['POST', 'GET'])
@app.route("/home", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        q = utils.Question()
        question = q.getQuestion()
        return render_template("quiz.html", question = question)
    return render_template("home.html")

@login_manager.user_loader
@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return render_template('index.html')
    return render_template("login.html", form = form)

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("hello")
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        db.session.add(User(username = username, email = email, password = password))
        db.session.commit()
        return render_template(url_for('login'))
    print("h")
    return render_template("register.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/topicChoose', methods = ['POST', 'GET'])
def ChoseTopic():
    if request.method == 'POST':
        topic = request.form['topic']
        diffLevel = request.form['diffLevel']
        print(topic)
        q = utils.Question()
        questions = q.getQuestion(topic)
        print(questions['question1'].keys())
        answers = {}
        q_no_ans = questions
        for i in questions.keys():
            x = questions[i]['answer']
            exp = questions[i]['explanation']
            answers[i] = {'answer': x, 'explanation': exp}
            del q_no_ans[i]['answer']
            del q_no_ans[i]['explanation']
        session['answers'] = answers

        print(q_no_ans['question1'].keys())
        return jsonify(q_no_ans)
        # return render_template('quizQuestion.html', nav = False, questions = jsonify(questions))
    return render_template('topicChoosing.html')

@app.route('/account')
def account():

    return render_template('account.html')

@app.route('/q')
def q():
    return render_template('quizQuestion.html', nav = False)

@app.route('/r', methods = ['POST', 'GET'])
def r():
    if request.method == 'POST':
        points = 0
        user_answers = dict(request.get_json())
        answers = session['answers']
        for i in user_answers.keys():
            print('r')
            print(answers.keys())
            print(answers[i])
            if 'chosenAnswer' in user_answers[i].keys() and user_answers[i]['chosenAnswer'] == answers[i]['answer']:
                answers[i]['correct'] = True
                points += 1
            else:
                answers[i]['correct'] = False
        answers['points'] = points
        return jsonify(answers)
    return render_template('quizResult.html', nav = False)