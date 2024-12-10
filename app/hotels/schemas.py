from datetime import date
from pydantic import BaseModel, json


class SHotel(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    