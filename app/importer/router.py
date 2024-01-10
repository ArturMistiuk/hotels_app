from fastapi import APIRouter, UploadFile

from app.exceptions import IncorrectFile
from app.dao.base import BaseDAO
from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(
    prefix='/importer',
    tags=['importer']
)


@router.post('/{table_name}')
async def import_data_to_db(table_name: str, data_file: UploadFile):
    filename, ext = data_file.filename.split('.')
    if not ext == 'csv':
        raise IncorrectFile
    content = await data_file.read(-1)
    content = content.decode()

    csv_lines = content.strip().split('\n')

    header = csv_lines[0]

    data_list = []
    for line in csv_lines[1:]:
        data_list.append(dict(zip(header.split(';'), line.split(';'))))

    for record in data_list:
        if table_name == 'Booking':
            response = await BookingDAO.add(*record)
            print(response)
