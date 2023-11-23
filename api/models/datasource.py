from sqlalchemy import Column, Integer, DateTime, String, JSON, ForeignKey, Float, ARRAY
from api.models.utils.base import BaseModel

# Alembic -> Migraciones

class DataSourceModel(BaseModel):
    __tablename__ = 'data_sources'
    
    data_type = Column(String(5), nullable=False)
    # Ej: Tienda de lentes y subo un PDF con los lentes
    # metadata solo se guarda en ChromaDB y la referencia de la metadata sera el ID del DataSource
    #metadata = Column(JSON)  # Storing metadata as JSON
    # Los embeddings SOLO se guardan en la BD en vector
    # embeddings = Column(ARRAY(Float))  # Storing embeddings as an array of floats
    chatbot_id = Column(Integer, nullable=False)


    # Subo archivo
    # Archivo se guarda localmente
    # Generamos los embeddings
    # Agregamos los embeddings a la BD en Vector
    # Eliminamos archivo
    