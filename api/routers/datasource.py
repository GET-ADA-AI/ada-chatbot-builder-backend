# /datasource
from fastapi import APIRouter, Depends
from api.schemas.datasource import DataSourceCreate, DataSourceGet
from api.services.datasource import DataSourceService
from api.services.jwt import JwtService
from api.services.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List


datasource_router = APIRouter()

# localhost:8000/datasource POST
@datasource_router.post("/", response_model=DataSourceGet)
def create_datasource(datasource: DataSourceCreate, db: Session = Depends(get_db)):
    """
    Create a new datasource
    """

    return DataSourceService.create_datasource(datasource, db)

@datasource_router.delete("/{data_id}", response_model=DataSourceGet)
def delete_datasource(data_id: int, db: Session = Depends(get_db)):
    """
    Delete a datasource by id
    """
    return DataSourceService.delete_datasource(data_id, db)
