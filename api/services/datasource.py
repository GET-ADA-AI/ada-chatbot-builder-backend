from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from api.models.datasource import DataSourceModel
from api.schemas.datasource import DataSourceCreate, DataSourceGet
from typing import List
from PyPDF2 import PdfWriter
from fpdf import FPDF
from os import path

class DataSourceService:
    """
    Service class for datasource related operations
    """

    @staticmethod
    def create_datasource(dataContent: str, db: Session):
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
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('helvetica', '', 12)
            #pdf.cell(text=dataContent)
            pdf.multi_cell(0, 10, dataContent)
            pdf.output('ParcialData.pdf')

            pdf_merger = PdfWriter()
            pdf_merger.append("TrainingData.pdf")
            pdf_merger.append("ParcialData.pdf")
            pdf_merger.write("TrainingData.pdf")
            pdf_merger.close()

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
