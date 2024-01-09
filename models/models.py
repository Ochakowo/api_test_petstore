from typing import Optional, Union
from pydantic import BaseModel, Field
from utils.enums import Status


class Category(BaseModel):
    id: int = Field
    name: str


class Tag(BaseModel):
    id: int = Field(ge=0)
    name: str


class Pet(BaseModel):
    """Options - любой из типов
    Union - один из типов"""

    id: int = Field(gt=0)
    category: Optional[Category] = None
    name: str = None
    photo_urls: Optional[list[str]] = Field(alias='photoUrls')
    tags: list[Tag]
    status: Union[Status] = None
