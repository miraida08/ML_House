from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from house_app.db.models import House
from house_app.db.database import SessionLocal
from house_app.db.schema import HouseSchema
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

house_router = APIRouter(prefix='/houses', tags=['House'])

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / 'house_price_model_job.pkl'
scaler_path = BASE_DIR / 'scaler.pkl'


model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@house_router.get('/search/', response_model=List[HouseSchema])
async def house_search(house_name: str, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.house_name.ilike(f'%{house_name}%')).all()
    if not house_db:
        raise HTTPException(status_code=404, detail='House not found')
    return house_db


# store
@house_router.post('/house/create/', response_model=HouseSchema)
async def house_create(house: HouseSchema, db: Session = Depends(get_db)):
    house_db = House(**house.dict())
    db.add(house_db)
    db.commit()
    db.refresh(house_db)
    return house_db


@house_router.get('/house/', response_model=List[HouseSchema])
async def house_list(db: Session = Depends(get_db)):
    return db.query(House).all()


@house_router.get('/house/{house_id}/', response_model=HouseSchema)
async def house_detail(house_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='house not found')
    return house


@house_router.put('/house/{house_id}/', response_model=HouseSchema)
async def house_update(house_id: int, house_data: HouseSchema, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='House not found')
    for house_key, house_value in house_data.dict().items():
        setattr(house, house_key, house_value)
    db.commit()
    db.refresh(house)
    return house


@house_router.delete('/house/{house_id}/')
async def house_delete(house_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail='house not found')
    db.delete(house)
    db.commit()
    return {'message': 'this house is deleted'}


model_columns = [
    'GrLivArea',
    'YearBuilt',
    'GarageCars',
    'TotalBsmtSF',
    'FullBath',
    'OverallQual'
]


@house_router.post('/predict/')
async def predict_price(house: HouseSchema, db: Session = Depends(get_db)):
    input_data = {
        'GrLivArea': house.GrLivArea,
        'YearBuilt': house.YearBuilt,
        'GarageCars': house.GarageCars,
        'TotalBsmtSF': house.TotalBsmtSF,
        'FullBath': house.FullBath,
        'OverallQual': house.OverallQual
    }
    input_df = pd.DataFrame([input_data])
    scaled_df = scaler.transform(input_df)
    predicted_price = model.predict(scaled_df)[0]
    return {'predicted_price': round(predicted_price)}

