from sqlalchemy import Column, Integer, DateTime, SmallInteger, String, JSON, ForeignKey, Float, ARRAY
from api.models.utils.base import BaseModel
import bcrypt


class DataSource(BaseModel):
    __tablename__ = 'data_sources'
    
    type = Column(String, index=True)
    metadata = Column(JSON)  # Storing metadata as JSON
    embeddings = Column(ARRAY(Float))  # Storing embeddings as an array of floats
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to the user who owns the data source
    


    def update_datasource(self, new_metadata):
        """
        Update the metadata of the data source.

        Parameters
        ----------
        new_metadata : dict
            New metadata to update.
        """
        self.metadata = new_metadata
    