from flask import Flask, render_template, request
from project_data.webapp.data.users import User
from datetime import datetime
from sqlalchemy import select
from project_data.webapp.data import db_session

app = Flask(__name__)


def insert_feedback_in_table(userid, feedback):
    global db_session
    db_session.global_init("db/data_talesworlds.db")
    user = User()
    user.userID = 789456
    user.user_feedback = 'feedback'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def insert_nickname_in_table(userid, nickname):
    from project_data.webapp.data import db_session
    db_session.global_init("db/data_talesworlds.db")
    user = User()
    user.userID = userid
    user.nickname = nickname
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    print('Ник утверждён')


def edit_nickname_in_table(userid, nickname):
    from project_data.webapp.data import db_session
    db_session.global_init("db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.userID == userid).first()
    user.nickname = nickname
    user.created_date = datetime.now()
    db_sess.commit()
    print('Ник изменён')


def db_viewer_nickname(userid):
    """
    Для register_nickname
    """
    from project_data.webapp.data import db_session
    db_session.global_init("project_data/webapp/db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.userID == userid)
    for _ in user:
        return False  # Если сработает - значит не регистрируем
    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feedbacks')
def feedbacks():
    return render_template('feedback.html')


@app.route('/feedbacks/write', methods=['POST', 'GET'])
def write_feedback():
    if request.method == 'POST':
        insert_feedback_in_table(1, 1)
        feedback_text = request.form['feedback']


    else:
        return render_template('feedback_form.html')


@app.route('/feedbacks/edit', methods=['POST', 'GET'])
def edit_feedback():
    if request.method == 'POST':
        pass
    else:
        return render_template('feedback_edit.html')


if __name__ == "__main__":
    db_viewer_nickname(1)
    app.run(debug=True)
