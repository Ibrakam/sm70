from  fastapi import APIRouter, UploadFile, File
import random


photo_router = APIRouter(prefix="/photo", tags=["Photo API"])



@photo_router.post("/add_photo")
async def add_photo_api(pid: int, photo_file: UploadFile = File(...)):
    file_id = random.randint(1, 1_000_000)
    if photo_file:
        try:
            with open(f"database/images/photo_{file_id}_{pid}.jpg", "wb") as photo:
                photo_to_save = await photo_file.read()
                print(photo.name)
                photo.write(photo_to_save)
                return "Photo saved"
        except Exception as e:
            return str(e)
