"""
1. СОздание коммента
2. Изменение коммента
3. Удаление коммента
4. Получение всех комментов поста(pid)
5. Получение всех комментов пользователя 


"""
from database import get_db
from database.models import Comment

def create_comment_db(uid, text, pid):
    db = next(get_db())
    new_comment = Comment(text=text, uid=uid, pid=pid)
    db.add(new_comment)
    db.commit()
    return True


def update_comment_db(cid, new_text):
    db = next(get_db())
    udpate_comment = db.query(Comment).filter_by(id=cid).first()
    if udpate_comment:
        udpate_comment.text = new_text
        db.commit()
        return True
    return False

def delete_comment_db(cid):
    db = next(get_db())
    exact_comment = db.query(Comment).filter_by(id=cid).first()
    if exact_comment:
        db.delete(exact_comment)
        db.commit()
        return True
    return False

def get_exact_post_comment_db(pid):
    db = next(get_db())
    all_comment = db.query(Comment).filter_by(pid=pid).all()
    return all_comment

def get_exact_user_comment(uid):
    db = next(get_db())
    all_comment = db.query(Comment).filter_by(uid=uid).all()
    return all_comment
        