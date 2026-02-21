from fastapi import APIRouter
from database.userservice import *
from api.schemas import UserSchema

user_router = APIRouter(prefix="/user", tags=["User API"])


@user_router.post('/create_user')
async def create_user_api(user_data: UserSchema):
    result = create_user_db(user_data)
    return {'status': 1, 'message': result}


@user_router.get('/get_user')
async def get_user_api(uid: int):
    result = get_user_db(uid=uid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}


@user_router.put('/update_user')
async def update_user_api(uid: int, change_info: str, new_info: str):
    result = update_user_db(uid=uid, change_info=change_info, new_info=new_info)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}


@user_router.delete('/delete_user')
async def delete_user_api(uid: int):
    result = delete_user_db(uid=uid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}