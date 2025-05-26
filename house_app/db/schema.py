from pydantic import BaseModel
from house_app.db.models import *


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    phone_number: Optional[str] = None


class HouseSchema(BaseModel):
    id: int
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: int

    class Config:
        from_attributes = True


