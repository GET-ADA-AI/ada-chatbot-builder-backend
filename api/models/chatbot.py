# models/user.py
from sqlalchemy import Column, Integer, DateTime, SmallInteger, String, JSON
from api.models.utils.base import BaseModel
import bcrypt

class ChatBotModel(BaseModel):
    """
    ChatBot model that ineherits from BaseModel and maps to the ChatBot tabble in the database.
    """

    # Table name
    __tablename__ = "chatbot"

    # Model's specific attributes
    chatbot_type = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    configuration = Column(JSON, nullable=False)
    data_source_ids = Column(JSON, nullable=True)
    
    def update_configuration(self, new_config):
        """
        Update the configuration of the chatbot.

        Parameters
        ----------
        new_config : dict
            New configuration to update.
        """
        self.configuration = new_config

    def add_data_source(self, data_source_id):
        """
        Add a new data source ID to the data_source_ids.

        Parameters
        ----------
        data_source_id : int
            ID of the new data source to add.
        """
        if self.data_source_ids is None:
            self.data_source_ids = []
        self.data_source_ids.append(data_source_id)

    def remove_data_source(self, data_source_id):
        """
        Remove a data source ID from the data_source_ids.

        Parameters
        ----------
        data_source_id : int
            ID of the data source to remove.
        """
        if self.data_source_ids and data_source_id in self.data_source_ids:
            self.data_source_ids.remove(data_source_id)
