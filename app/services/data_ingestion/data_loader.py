import os
import requests
from app.utils.loggers import get_logger
from langchain_core.documents import Document
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from app.utils.exceptions import NetworkError, PDFLoadError



logger = get_logger(__name__)

DATA_DIR = "data"

#download data if not present
def download_data(url, pdfname):
    '''Download PDF from URL'''
    
    #create data directory if not exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
     #download file
    pdf_path = f"{DATA_DIR}/{pdfname}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(pdf_path, "wb") as file:
            file.write(response.content)
        logger.info(f"Success! {pdf_path} downloaded.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed: {e}")
        raise NetworkError(
            "Failed to download and save PDF" )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise e



def load_pdf(url, pdfname) -> List[Document]:
    """Load PDF document"""
    
    pdf_path = f"{DATA_DIR}/{pdfname}"
    #if pdf not present, download it
    if not os.path.exists(pdf_path):
        download_data(url, pdfname)

    logger.info(f"Loading PDF from {pdf_path}")

    try:
        #load pdf using PyMuPDFLoader
        loader = PyMuPDFLoader(str(pdf_path))
        documents = loader.load()

        logger.info(f"Loaded {len(documents)} pages")
    except Exception as e:
        logger.error(f"PDF loading error: {e}")
        raise PDFLoadError(f"Failed to load PDF due to PDF loading error: {e}")
    return documents