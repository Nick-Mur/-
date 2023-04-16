from flask import Flask, render_template, request
from project_data.webapp.data.users import User
from datetime import datetime
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tales_secret_world_key'


def insert_feedback_in_table(userid, feedback):
    from data import db_session
    db_session.global_init("db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.userID == userid).first()
    user.user_feedback = feedback
    user.created_date = datetime.now()
    db_sess.commit()
    print('Ник изменён')


def insert_nickname_in_table(userid, nickname):
    from data import db_session
    db_session.global_init("db/data_talesworlds.db")
    user = User()
    user.userID = userid
    user.nickname = nickname
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    print('Ник утверждён')


def edit_nickname_in_table(userid, nickname):
    from data import db_session
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
    from data import db_session
    db_session.global_init("project_data/webapp/db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.userID == userid)
    for _ in user:
        return False  # Если сработает - значит не регистрируем
    return True


@app.route('/')
def index():
    with open('static/text/updates.txt', 'r', encoding="utf-8") as f:
        updates_data = f.readlines()[0]
    return render_template('index.html',
                           updates=updates_data
                           )


@app.route('/feedbacks')
def feedbacks():
    from data import db_session
    db_session.global_init("db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_feedback != None)
    feedback_list = []
    for i in user:
        print(i.userID)
        feedback_list.append({'user_id': i.userID, 'feedback': i.user_feedback})
    return render_template('feedback.html',
                           feedback_created=True,
                           feedback=feedback_list)


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
    app.run(debug=True)
