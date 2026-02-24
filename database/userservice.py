from database import get_db
from database.models import User
from api.schemas import UserSchema


def create_user_db(user_data: UserSchema):
    db = next(get_db())
    user_dict = user_data.model_dump()
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    return True





def get_user_db(uid = 0):
    db = next(get_db())
    if uid:
        exact_user = db.query(User).filter_by(id=uid).first()
        if exact_user:
            return exact_user
        return False
    all_users = db.query(User).all()
    return all_users


def update_user_db(uid, change_info, new_info):
    db = next(get_db())
    exact_user = db.query(User).filter_by(id=uid).first()
    if exact_user:
        if change_info == 'name':
            exact_user.name = new_info
        elif change_info == 'email':
            exact_user.email = new_info
        elif change_info == 'password':
            exact_user.password = new_info
        elif change_info == 'user_name':
            exact_user.user_name = new_info
        elif change_info == 'lastname':
            exact_user.lastname = new_info
        elif change_info == 'birthday':
            exact_user.birthday = new_info
        elif change_info == 'city':
            exact_user.city = new_info
        db.commit()
        return True
    return False



def delete_user_db(uid):
    db = next(get_db())
    exact_user = db.query(User).filter_by(id=uid).first()
    if exact_user:
        db.delete(exact_user)
        db.commit()
        return True
    return False


def verify_password(password, password_db):
    return password == password_db

def get_user_by_username_db(username):
    db = next(get_db())
    user = db.query(User).filter_by(username = username).first()
    if user:
        return user
    return False



