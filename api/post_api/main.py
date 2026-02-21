from fastapi import APIRouter
from database.postservice import *


post_router = APIRouter(prefix='/post', tags=['Post API'])



@post_router.post('/create_post')
async def create_user_api(uid: int, text: str):
    result = create_post_db(uid=uid, text=text)
    return {'status': 1, 'message': result}

@post_router.get('/get_user_posts')
async def get_post_exact_user_api(uid: int):
    result = get_exact_user_post_db(uid=uid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}

@post_router.get('/get_posts')
async def get_all_or_exact_post_api(pid: int):
    result = get_all_or_exact_post(pid=pid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}


@post_router.put('/update_post')
async def update_post_api(pid: int, new_info: str):
    result = update_post_db(pid=pid, new_info=new_info)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}

@post_router.delete('/delete_post')
async def delete_post_api(pid: int):
    result = delete_post_db(pid=pid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}