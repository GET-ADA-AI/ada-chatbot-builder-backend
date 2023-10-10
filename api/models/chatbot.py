# models/chatbot.py
from sqlalchemy import Column, Integer, DateTime, String, JSON
from api.models.utils.base import BaseModel

class ChatBotModel(BaseModel):
    """
    ChatBot model that ineherits from BaseModel and maps to the ChatBot tabble in the database.
    """

    # Table name
    __tablename__ = "chatbot"

    # Model's specific attributes
    chatbot_type = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    # En vez de utilizar JSON, aplicar herencia para cada tipo de chatbot
    # En los tipos de chatbot especificos agregamos los atributos que corresponden a cada tipo
    # En esta tabla se quedan los atributos de configuracion generales
    # Nombre del chatbot, Tono de voz -> Parrafo, CONSIDERAR IDEA INICIAL: https://miro.com/app/board/uXjVM0wdZZ4=/?share_link_id=921013511119
    # configuration = Column(JSON, nullable=False)
    # data_source_ids = Column(Integer, nullable=False)

    """
    def update_configuration(self, new_config):
        
        Update the configuration of the chatbot.

        Parameters
        ----------
        new_config : dict
            New configuration to update.
        
        self.configuration = new_config

    def add_data_source(self, data_source_id):
        
        Add a new data source ID to the data_source_ids.

        Parameters
        ----------
        data_source_id : int
            ID of the new data source to add.
        
        if self.data_source_ids is None:
            self.data_source_ids = []
        self.data_source_ids.append(data_source_id)

    def remove_data_source(self, data_source_id):
        
        Remove a data source ID from the data_source_ids.

        Parameters
        ----------
        data_source_id : int
            ID of the data source to remove.
        
        if self.data_source_ids and data_source_id in self.data_source_ids:
            self.data_source_ids.remove(data_source_id)
    """
