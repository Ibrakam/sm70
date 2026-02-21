from fastapi import FastAPI, Request
from api.photo_api.main import photo_router
from api.user_api.main import user_router, get_user_db
from api.post_api.main import post_router, get_all_or_exact_post, get_exact_user_post_db
from api.comment_api.main import comment_router
from database import Base, engine
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(docs_url="/docs")
templates = Jinja2Templates(directory="templates")

app.include_router(photo_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
Base.metadata.create_all(engine)



@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    posts = get_all_or_exact_post()
    return templates.TemplateResponse(request, name="index.html", 
    context={"all_posts": posts})

@app.get("/user/{uid}", response_class=HTMLResponse)
async def user_post_page(request: Request, uid: int):
    user_posts = get_exact_user_post_db(uid)
    user = get_user_db(uid)
    return templates.TemplateResponse(request, name="user.html", 
    context={"user_posts": user_posts, "user": user})
