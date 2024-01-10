import shutil

from fastapi import APIRouter, Response, UploadFile, status

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Uploading images']
)


@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile) -> Response:
    im_path = f'app/static/images/{name}.webp'
    with open(im_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)

    return Response(status_code=status.HTTP_201_CREATED)
