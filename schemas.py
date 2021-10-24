from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    job_id: str = "1"

class ItemReg(Item):
    message: str = "message"
    color: Optional[str] = "primary"  # white, red, green, ..., colorful
    fontsize: Optional[int] = 16  # 8 - 32

class ItemShow(Item):
    bright: Optional[float] = 0.5   # 0.0 - 1.0
    interval: Optional[float] = 0.0

class ItemDo(ItemShow, ItemReg):
    reserved: Optional[int] = 0

