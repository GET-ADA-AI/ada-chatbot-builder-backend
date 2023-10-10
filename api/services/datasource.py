from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.datasource import DataSourceModel
from api.schemas.datasource import DataSourceCreate, DataSourceGet
from typing import List

class DataSourceService:
    """
    Service class for datasource related operations
    """

    @staticmethod
    def create_datasource(datasource: DataSourceCreate, db: Session) -> DataSourceGet:
        """
        Create a new datasource in the PostgreSQL database

        Parameters
        ----------
        datasource : DataSourceCreate
            Pydantic model for creating a datasource
        db : Session
            Database Session

        Returns
        -------
        DataSourceGet
            Pydantic model for retrieving a datasource
        """

        try:
            #Create a new datasource
            new_datasource = DataSourceModel(data_type=datasource.data_type, chatbot_id=datasource.chatbot_id)
            # Add the datasource to the database session
            db.add(new_datasource)
            # Commit the changes to the database
            db.commit()
            # Refresh the datasource to get the datasource id
            db.refresh(new_datasource)
            # Return the new datasource
            return new_datasource

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)
        
    @staticmethod
    def delete_datasource(id: int, db: Session):
        """
        Delete a datasource from the PostgreSQL database

        Parameters
        ----------
        datasource_id : int
            ID of the datasource to delete
        db : Session
            Database Session

        Returns
        -------
        datasourceGet
            Pydantic model for retrieving a datasource
        """

        try:
            # Get datasource with datasource_id
            datasource = db.query(DataSourceModel).filter(DataSourceModel.id == id).first()
            # Check if datasource exists
            if datasource is None:
                # Raise an HTTPException with the not found error message
                raise HTTPException(status_code=404, detail="datasource not found")
            
            # Change the status of the datasource to 0
            datasource.status = 0
            # Commit the changes to the database
            db.commit()

            # Refresh the datasource
            db.refresh(datasource)

            # Return an appropriate message
            return datasource

        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Format the error message
            error_message = f"Database error: {e.orig}"
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=error_message)
