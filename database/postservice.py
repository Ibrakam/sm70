"""
1. Создание поста
2. Изменение поста
3. Удаление поста
4. Получить пост определенного пользователя
5. Получение всех или определенного поста

"""


from database.models import UserPost
from database import get_db



"""
db = next(get_db())
ДОбавление
new_post = UserPost(text=text, uid=uid)
db.add(new_post)
db.commit()

Получение данных
db.query(UserPost).all()
db.query(UserPost).filter_by(id=1).first()

Изменение
udpate_post = db.query(UserPost).filter_by(id=1).first()
update_post.text = "sdkmsdf"
db.commit()

УДаление
delete_post = db.query(UserPost).filter_by(id=1).first()
db.delete()
db.commit()


"""


def create_post_db(uid, text):
    db = next(get_db())
    new_post = UserPost(text=text, uid=uid)
    db.add(new_post)
    db.commit()
    return True


def update_post_db(pid, new_text):
    db = next(get_db())
    udpate_post = db.query(UserPost).filter_by(id=pid).first()
    if udpate_post:
        udpate_post.text = new_text
        db.commit()
        return True
    return False

def delete_post_db(pid):
    db = next(get_db())
    exact_post = db.query(UserPost).filter_by(id=pid).first()
    if exact_post:
        db.delete(exact_post)
        db.commit()
        return True
    return False


def get_exact_user_post_db(uid):
    db = next(get_db())
    all_post = db.query(UserPost).filter_by(uid=uid).all()
    return all_post

def get_all_or_exact_post(pid=0):
    db = next(get_db())
    if pid:
        exact_post = db.query(UserPost).filter_by(id=pid).first()
        if exact_post:
            return exact_post
        return False
    all_post = db.query(UserPost).all()
    return all_post
        

