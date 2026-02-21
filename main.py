from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.comment_api.main import comment_router
from api.photo_api.main import photo_router
from api.post_api.main import get_all_or_exact_post, get_exact_user_post_db, post_router
from api.user_api.main import get_user_db, user_router
from database import Base, SessionLocal, engine
from database.models import Comment, PostPhoto, User

app = FastAPI(docs_url="/docs")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="database/images"), name="images")
templates = Jinja2Templates(directory="templates")
IMAGE_STORAGE = Path("database/images")

app.include_router(photo_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
Base.metadata.create_all(engine)

FEED_MEME_CHIPS = [
    "Когда деплой в пятницу, а ты уже в такси",
    "Это не баг, это фича с характером",
    "Рефакторинг завтра, сегодня только hotfix",
    "Вижу TODO и делаю вид, что это roadmap",
]

MEME_OF_THE_DAY = [
    "Мем дня: \"Сделал одну правку\" -> 42 файла в git status.",
    "Мем дня: \"Быстрый созвон\" длиннее, чем sprint planning.",
    "Мем дня: \"Ща только кнопку подвину\" и уже новый дизайн-систем.",
    "Мем дня: \"Не трогай прод\" звучит как личная просьба.",
]

PROFILE_MEME_STATUSES = [
    "Режим: пишу, пока тесты не моргают.",
    "Онлайн: чиню edge-case, о котором никто не просил.",
    "Статус: 80% кофе, 20% pixel-perfect.",
    "Настроение: ship it, но с ревью.",
]


def _format_reg_date(value):
    if not value:
        return "не указана"
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    return str(value)


def _normalize_photo_url(photo_path):
    if not photo_path:
        return None
    filename = Path(photo_path).name
    return f"/images/{filename}"


def _fallback_photo_url_for_post(post_id):
    try:
        files = sorted(
            IMAGE_STORAGE.glob(f"photo_*_{post_id}.jpg"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return None
    if not files:
        return None
    return _normalize_photo_url(str(files[0]))


def _build_post_cards(posts):
    db = SessionLocal()
    cards = []
    try:
        post_uids = {post.uid for post in posts}
        author_map = {}
        if post_uids:
            users = db.query(User).filter(User.id.in_(post_uids)).all()
            author_map = {user.id: user.username for user in users}

        for index, post in enumerate(posts):
            photo = (
                db.query(PostPhoto)
                .filter_by(pid=post.id)
                .order_by(PostPhoto.id.desc())
                .first()
            )
            comments = (
                db.query(Comment)
                .filter_by(pid=post.id)
                .order_by(Comment.id.asc())
                .all()
            )
            comment_items = [
                {
                    "author_name": comment.user_fk.username if comment.user_fk else "Аноним",
                    "text": comment.text,
                }
                for comment in comments
            ]
            cards.append(
                {
                    "id": post.id,
                    "text": post.text,
                    "author_id": post.uid,
                    "author_username": author_map.get(post.uid, "Неизвестный автор"),
                    "photo_url": (
                        _normalize_photo_url(photo.photo_path)
                        if photo
                        else _fallback_photo_url_for_post(post.id)
                    ),
                    "comments": comment_items,
                    "comments_count": len(comment_items),
                    "meme_chip": FEED_MEME_CHIPS[(post.id + index) % len(FEED_MEME_CHIPS)],
                    "created_at": _format_reg_date(post.reg_date),
                }
            )
    finally:
        db.close()
    return cards


def _meme_of_the_day():
    day_index = datetime.now().toordinal() % len(MEME_OF_THE_DAY)
    return MEME_OF_THE_DAY[day_index]


def _profile_meme_status(uid):
    return PROFILE_MEME_STATUSES[uid % len(PROFILE_MEME_STATUSES)]


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    posts = get_all_or_exact_post()
    post_cards = _build_post_cards(posts if isinstance(posts, list) else [])
    return templates.TemplateResponse(
        request,
        name="index.html",
        context={
            "feed_posts": post_cards,
            "meme_of_the_day": _meme_of_the_day(),
        },
    )


@app.get("/user/{uid}", response_class=HTMLResponse)
async def user_post_page(request: Request, uid: int):
    user_posts = get_exact_user_post_db(uid)
    user = get_user_db(uid)
    post_cards = _build_post_cards(user_posts if isinstance(user_posts, list) else [])
    metrics = {
        "post_count": len(post_cards),
        "city": user.city if user and user.city else "не указан",
        "reg_date": _format_reg_date(user.reg_date if user else None),
    }
    return templates.TemplateResponse(
        request,
        name="user.html",
        context={
            "user_posts": post_cards,
            "user": user,
            "metrics": metrics,
            "profile_meme_status": _profile_meme_status(uid),
        },
    )
