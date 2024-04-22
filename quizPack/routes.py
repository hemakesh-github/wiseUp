from flask import jsonify, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from quizPack import app, login_manager, bcrypt, db
from quizPack import utils
from quizPack.forms import LoginForm, RegisterForm
from quizPack.models import User, SavedQuestions

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods = ['POST', 'GET'])
@app.route("/home", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        return render_template("quiz.html")
    return render_template("home.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return render_template('home.html')
    return render_template("login.html", form = form)

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        db.session.add(User(username = username, email = email, password = password))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/topicChoose', methods=['POST', 'GET'])
@login_required
def ChoseTopic():
    if request.method == 'POST':
        topic = request.form['topic']
        diffLevel = request.form['diffLevel']
        q = utils.Question()
        questions = q.getQuestion(topic, diffLevel)
        answers = {}
        q_no_ans = questions
        for i in questions.keys():
            x = questions[i]['answer']
            exp = questions[i]['explanation']
            answers[i] = {'answer': x, 'explanation': exp}
            del q_no_ans[i]['answer']
            del q_no_ans[i]['explanation']
        session['answers'] = answers
        return jsonify(q_no_ans)
    return render_template('topicChoosing.html')

@app.route('/account')
@login_required
def account():
    savedQs = SavedQuestions.query.filter_by(user_id = current_user.id).all()
    filename = current_user.profile
    return render_template('account.html', savedQs = savedQs, filename = filename)

@app.route('/q')
@login_required
def q():
    return render_template('quizQuestion.html', nav = False)

@app.route('/result', methods = ['POST', 'GET'])
@login_required
def result():
    if request.method == 'POST':
        points = 0
        user_answers = dict(request.get_json())
        answers = session['answers']
        for i in user_answers.keys():
            if 'chosenAnswer' in user_answers[i].keys() and user_answers[i]['chosenAnswer'] == answers[i]['answer']:
                answers[i]['correct'] = True
                points += 1
            else:
                answers[i]['correct'] = False
        answers['points'] = points
        user = current_user
        user.points += points
        db.session.commit()
        return jsonify(answers)
    return render_template('quizResult.html', nav=False)


@app.route('/savedQ', methods = ['POST', 'GET'])
def savedQuestions():
    if request.method == 'POST':
        id = request.form['q-id']
        q = SavedQuestions.query.filter_by(id = id).first()
        return jsonify({'question': q.question, 'opt1': q.option1, 'opt2': q.option2, 'opt3': q.option3, 'opt4': q.option4, 'answer': q.answer, 'explanation': q.explanation})
    return render_template('savedQ.html')

@login_required
@app.route('/changeDP', methods = ['POST', 'GET'])
def changeDP():
    if request.method == 'POST':
        file = request.files['file']
        ext = file.filename.split('.')[-1]
        filename = 'user'+str(current_user.id)+'.'+ext
        file.save('quizPack/static/images/' + filename)
        user = current_user
        user.profile = filename
        db.session.commit()
        return jsonify({'flag': True, 'filename': filename})
    return render_template('account.html')


@login_required
@app.route('/saveQuestion', methods = ['POST', 'GET'])
def saveQuestion():
    if request.method == 'POST':
        questions = request.get_json()
        user_id = current_user.id
        answers = session['answers']
        for i in questions.keys():
            db.session.add(SavedQuestions(user_id = user_id, question = questions[i]['question'], option1 = questions[i]['opt1'], option2 = questions[i]['opt2'], option3 = questions[i]['opt3'], option4 = questions[i]['opt4'], answer = answers[i]['answer'], explanation = answers[i]['explanation']))
        db.session.commit()
        return jsonify({'flag': True})
    return render_template('saveQuestion.html')