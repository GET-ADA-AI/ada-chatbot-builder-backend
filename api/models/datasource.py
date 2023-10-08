from sqlalchemy import Column, Integer, DateTime, SmallInteger, String, JSON, ForeignKey, Float, ARRAY
from api.models.utils.base import BaseModel
# Eliminar todos los unnecessary imports
import bcrypt

# Alembic -> Migraciones

class DataSource(BaseModel):
    __tablename__ = 'data_sources'
    
    # type -> palabra reservada
    # Cambiarlo por una palabra que no sea reservada
    # Utilizar un Enum o un Integer

    # class TypeEnum(Enum):
    #     # Define your enum values here
    #     PDF = 'PDF'
    #     VALUE2 = 'Value 2'
    #     VALUE3 = 'Value 3'
    
    # type = Column(Enum(TypeEnum), index=True)
    type = Column(String, index=True)

    # Ej: Tienda de lentes y subo un PDF con los lentes
    # metadata solo se guarda en ChromaDB y la referencia de la metadata sera el ID del DataSource
    metadata = Column(JSON)  # Storing metadata as JSON
    # Los embeddings SOLO se guardan en la BD en vector
    embeddings = Column(ARRAY(Float))  # Storing embeddings as an array of floats
    # cambiaria a chatbot_id
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to the user who owns the data source


    # Subo archivo
    # Archivo se guarda localmente
    # Generamos los embeddings
    # Agregamos los embeddings a la BD en Vector
    # Eliminamos archivo

    # No lo vamos a utilizar
    def update_datasource(self, new_metadata):
        """
        Update the metadata of the data source.

        Parameters
        ----------
        new_metadata : dict
            New metadata to update.
        """
        self.metadata = new_metadata
    