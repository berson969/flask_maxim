from pydantic import BaseModel, validator
from typing import Optional


class CreateAds(BaseModel):
    header: str
    description: str
    owner: str

    @validator('header')
    def secure_header(cls, value):
        if len(value) <= 6:
            raise ValueError('Header is short')
        return value


class UpdateAds(BaseModel):
    header: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @validator('header')
    def secure_header(cls, value):
        if len(value) <= 6:
            raise ValueError('Header is short')
        return value
