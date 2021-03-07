import uuid
from quizuser import QuizUser
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    level=logging.DEBUG
)
log = logging.getLogger(__name__)

user_list = []

from flask import Flask, request, url_for, redirect, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid1())

@app.route('/')
def index():
    log.info('call /index')
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    log.info('call /index post')

    username = request.form['username']
    question_amount = request.form['questionamount']

    log.debug('username: ' + username)
    log.debug('question_amount: ' + question_amount)

    if username == '':
        username = 'stranger'

    user = QuizUser(username=username, question_amount=question_amount)
    user_list.append(user)
    return redirect(url_for('game', id=user.id))

@app.route('/game', methods=['GET'])
def game():
    log.info('call /game get')
    userid = request.args['id']
    log.debug('userid: ' + str(userid))

    user_number = 0
    for item in user_list:
        if item.id == userid:
            break
        user_number = user_number + 1
    log.debug('user id: ' + str(user_list[user_number].id))
    log.debug('user name: ' + str(user_list[user_number].name))

    if 'answer' in request.args:
        user_answer = request.args['answer']
        log.debug('user_answer: ' + str(user_answer))
        user_list[user_number].save_user_answer(
            question_num=user_list[user_number].question_counter,
            answer_num=int(user_answer))

    question, answers = user_list[user_number].get_next_question()

    if not question:
        return redirect(url_for('results',
                                id=str(user_list[user_number].id)))

    return render_template(
        'game.html',
        userid=str(user_list[user_number].id),
        username=str(user_list[user_number].name),
        question=question,
        answer0=answers[0],
        answer1=answers[1],
        answer2=answers[2],
        answer3=answers[3])

@app.route('/results', methods=['GET'])
def results():
    log.info('call /results get')
    userid = request.args['id']
    log.debug('userid: ' + str(userid))

    user_number = 0
    for item in user_list:
        if item.id == userid:
            break
        user_number = user_number + 1
    log.debug('user id: ' + str(user_list[user_number].id))
    log.debug('user name: ' + str(user_list[user_number].name))

    correctquestions = user_list[user_number].correct_counter
    userscore = user_list[user_number].score

    return render_template(
        'results.html',
        userid=str(user_list[user_number].id),
        username=str(user_list[user_number].name),
        correctquestions=correctquestions,
        question_counter=user_list[user_number].question_counter,
        userscore=userscore)

if __name__ == '__main__':
    log.info('Startup main!')
    app.run(debug=True, host='0.0.0.0', port=80)
