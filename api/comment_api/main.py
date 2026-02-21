from fastapi import APIRouter
from database.commenservice import *


comment_router = APIRouter(prefix='/comment', tags=['Comment API'])


@comment_router.post('/create_comment')
async def create_comment_api(text: str, uid: int, pid: int):
    result = create_comment_db(text=text, uid=uid, pid=pid)
    return {'status': 1, 'message': result}


@comment_router.put('/update_comment')
async def update_comment_api(cid: int, new_info: str):
    result = update_comment_db(cid=cid, new_info=new_info)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}

@comment_router.delete('/delete_comment')
async def delete_comment_api(cid: int):
    result = delete_comment_db(cid=cid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}

@comment_router.get('/get_comment_by_post')
async def get_comment_by_post_api(pid: int):
    result = get_exact_post_comment_db(pid=pid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}


@comment_router.get('/get_comment_by_user')
async def get_comment_by_user_api(uid: int):
    result = get_comment_by_user_api(uid=uid)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': result}