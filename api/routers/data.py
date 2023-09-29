# /data
from fastapi import APIRouter, Depends
from api.schemas.data import DataCreate, DataGet, DataUpdate
from api.services.data import DataService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


data_router = APIRouter()

# localhost:8000/data POST
@data_router.post("/", response_model=DataGet)
def create_data(data: DataCreate, db: Session = Depends(get_db)):
    """
    Create a new data
    """

    return DataService.create_data(data, db)

@data_router.delete("/{data_id}", response_model=DataGet)
def delete_data(data_id: int, db: Session = Depends(get_db)):
    """
    Delete a data by id
    """
    return DataService.delete_data(data_id, db)

@data_router.patch("/{data_id}", response_model=DataGet)
def patch_data(data_id: int, data_update: DataUpdate, db: Session = Depends(get_db)):
    """
    Patch a data by id
    """
    return DataService.patch_data(data_id, data_update, db)
