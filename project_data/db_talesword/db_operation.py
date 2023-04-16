from project_data.db_talesword.data.users import User
from datetime import datetime


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
    from project_data.db_talesword.data import db_session
    db_session.global_init("db/data_talesworlds.db")
    user = User()
    user.userID = userid
    user.nickname = nickname
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    print('Ник утверждён')


def edit_nickname_in_table(userid, nickname):
    from project_data.db_talesword.data import db_session
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
    from project_data.db_talesword.data import db_session
    db_session.global_init("project_data/db_talesword/db/data_talesworlds.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.userID == userid)
    for _ in user:
        return False  # Если сработает - значит не регистрируем
    return True

