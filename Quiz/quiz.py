from flask import Flask, render_template, request, url_for, redirect, send_file
from flask import session
import random, copy
import json
import os


app = Flask(__name__)
rand_int = str(random.randint(10,999999999999))
app.secret_key = '##$$%%876ty' + rand_int
IMAGE_FOLDER = os.path.join('static', 'images')
winner_file = 'winner' + rand_int + '.inf'
with open('answer.cnf', 'r') as answer_file:
    qsn_data = json.load(answer_file)
with open('users.inf','r') as user_file:
    user_data = json.load(user_file)
user_list = user_data
questions = qsn_data


@app.route('/')
def quiz():
    if 'username' in session:
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('login_page'))

@app.route('/index')
def home_page():
    if 'username' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login_page'))

@app.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']

        if username in user_list:
            session['username'] = request.form['username']
            return redirect(url_for('home_page'))
        else:
            warn = ["Invalid User"]
            return render_template('login.html', w=warn)

    else:
        image = send_file('static/images/bg.png')
        return render_template('login.html', w=[], i=image)

@app.route('/winner', methods=['GET'])
def winner():
    if os.path.exists(winner_file):
        fp = open(winner_file)
        winners = fp.readlines()
        winner = winners[0]
        runner_up1 = "Nobody is runner Up yet"
        runner_up2 = "Nobody is 2nd runner Up yet"
        if len(winners) > 1:
            runner_up1 = winners[1] + "is 1st runner up."
        if len(winners) > 2:
            runner_up2 = winners[2] + "is 2nd runner up"

        fp.close()
        return render_template('winner.html', w=winner, w1=runner_up1, w2=runner_up2)
    else:
        winner_name = 'Till now, Nobody'
    return render_template('winner.html', w=winner_name, w1="", w2="")


@app.route('/quiz', methods=['POST'])
def quiz_answers():
    max_num = len(questions)
    form_res = request.form
    qnum = int(form_res['qnum'])
    print(form_res)
    if qnum == 0:
        # qsn = questions[qnum]['qsn']
        qsn = os.path.join(IMAGE_FOLDER, questions[qnum]['qsn'])
        #choices = questions[qnum]['choices']
        return render_template('quiz.html', num=qnum + 1, q=qsn, m=max_num)

    elif qnum <= max_num:
        qsn = questions[qnum - 1]['qsn']
        ans = str(form_res['ans']).upper()
        correct_ans = questions[qnum - 1]['answer'].upper()
        print(ans)
        print(correct_ans)
        if ans == correct_ans:

            if qnum == max_num:
                if os.path.exists(winner_file):
                    fp = open(winner_file,'r')
                    winner_name = fp.read()
                    fp.close()
                    fp = open(winner_file,'a+')
                    fp.write(session['username'])
                    fp.write('\n')
                    fp.close()
                    return redirect(url_for('winner'))

                with open(winner_file, 'w') as fp:
                    fp.write(session['username'])
                    fp.write('\n')
                msz = 'Congratulations, {} Won!'.format(session['username'])
                return render_template('finish.html', msz=msz)
            # return next Page
            qsn = os.path.join(IMAGE_FOLDER, questions[qnum]['qsn'])
            #choices = questions[qnum]['choices']
            return render_template('quiz.html', num=qnum + 1, q=qsn,m=max_num)

        else:
            # stay on the same page
            # qsn = questions[qnum - 1]['qsn']
            qsn = os.path.join(IMAGE_FOLDER, questions[qnum-1]['qsn'])
            warn = ['Try Again']
            return render_template('quiz.html', num=qnum, q=qsn, w=warn,m=max_num)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
