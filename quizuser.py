import logging
import datetime
import uuid
import requests
import random
log = logging.getLogger(__name__)


class QuizUser:
    def __init__(self, username='default', question_amount=3):
        self.id = ''
        self.date = None
        self.name = ''
        self.create_user(username=username)

        self.session_token = ''
        self.connect_open_trivia()

        self.question_list = []
        self.correct_counter = 0
        self.question_counter = -1
        self.score = 0.0
        self.call_for_questions(amount=question_amount)

    def create_user(self, username='default'):
        log.info('create_user')

        self.id = str(uuid.uuid1())[:8]
        self.date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.name = username
        log.debug('name: ' + str(self.name) + ' date: ' + self.date + ' id: ' + self.id)

        self.connect_open_trivia()

    def connect_open_trivia(self):
        log.debug('connect_open_trivia')
        response = requests.get('https://opentdb.com/api_token.php?command=request')
        if response.status_code == 200:
            log.debug('Resppnse code: ' + str(response.status_code))
            self.session_token = response.json()['token']
            log.debug('Successfully stored sessions token.')
        else:
            log.warning('No sessions token recifed! Response code: ' + str(response.status_code))

    def call_for_questions(self, amount=3):
        log.info('call_for_question')
        # https://opentdb.com/api.php?amount=10&token=YOURTOKENHERE
        request_url = 'https://opentdb.com/api.php?&type=multiple&amount=' + str(amount) + '&token=' + self.session_token
        log.debug('request_url:\n' + request_url)
        response = requests.get(request_url)
        log.debug('response.encoding: ' + response.encoding)
        #response.encoding = 'utf-8'
        if response.status_code == 200:
            log.debug('Response code: ' + str(response.status_code))
            response_json = response.json()
            self.question_list = response_json['results']
            log.debug('question_list:\n' + str(self.question_list))
        else:
            log.warning('No questions recifed! Response code: ' + str(response.status_code))

    def get_next_question(self):
        log.info('get_next_question')

        self.question_counter = self.question_counter + 1
        log.debug('question_counter: ' + str(self.question_counter))

        if self.question_counter >= len(self.question_list):
            log.debug('No more questions available!')
            return False, False

        question = self.question_list[self.question_counter].get('question')
        log.debug('question: ' + question)

        answers = []
        answers.append(self.question_list[self.question_counter].get('correct_answer'))
        for item in self.question_list[self.question_counter].get('incorrect_answers'):
            answers.append(str(item))

        random.shuffle(answers)
        log.debug('answers: ' + str(answers))
        self.question_list[self.question_counter]['shuffled_answers'] = answers

        return question, answers

    def save_user_answer(self, question_num=None, answer_num=None):
        log.info('save_user_answer')
        log.debug('question_num: ' + str(question_num))
        log.debug('answer_num: ' + str(answer_num))

        log.debug('shuffled_answers: ' + str(self.question_list[question_num]['shuffled_answers']))

        answer_text = self.question_list[question_num]['shuffled_answers'][int(answer_num)]
        log.debug('answer_text: ' + answer_text)

        self.question_list[question_num]['user_answer'] = answer_text

        status_value = self.is_correct(question_num=question_num)
        self.update_score(status_value=status_value)

    def is_correct(self, question_num=None):
        log.info('is_correct')
        log.debug('question_num: ' + str(question_num))
        log.debug('correct_answer: ' + str(self.question_list[question_num]['correct_answer']))
        if self.question_list[question_num]['correct_answer'] == self.question_list[question_num]['user_answer']:
            log.debug('user answer ist correct!')
            return True
        return False

    def update_score(self, status_value=False):
        log.debug('update_score')
        if status_value:
            self.correct_counter = self.correct_counter + 1
        log.debug('correct_counter: ' + str(self.correct_counter))
        log.debug('question_counter: ' + str(self.question_counter))
        self.score = int(self.correct_counter / float(self.question_counter+1) * 100)
        log.debug('score: ' + str(self.score))

    def print_stats(self):
        log.info('print_stats')
        log.debug('name: ' + str(self.name))
        log.debug('id: ' + str(self.id))
        log.debug('date: ' + str(self.date))
        log.debug('session_token: ' + str(self.session_token))
        log.debug('correct_counter: ' + str(self.correct_counter))
        log.debug('question_counter: ' + str(self.question_counter))
        log.debug('score: ' + str(self.score))
