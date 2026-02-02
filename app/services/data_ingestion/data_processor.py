import re
from langchain_core.documents import Document
from typing import List
from app.utils.loggers import get_logger
from app.utils.exceptions import DocumentFilterError

logger = get_logger(__name__)

#medical section headings to identify (found in the medical pdf)
MEDICAL_SECTION_HEADINGS = ["Definition", "Purpose","Risks",
                            "Description","Preparation", "Normal results",
                            "Abnormal results","Aftercare","Causes and symptoms",
                            "Diagnosis","Treatment","Alternative treatment",
                            "Prevention","Prognosis", "Precautions",
                            "Side effects", "Recommended dosage","Research and general acceptance"
                            ]






def medical_preprocess(text: str) -> str:
    # Fix hyphenated line breaks
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    text= re.sub(
        r"G A L E E N C Y C L O P E D I A O F M E D I C I N E|\n\d+\n",
        "",
        text
    )
    # Remove a number only if it appears at the end of a page
    text = re.sub(r'\n\s*(\d+)\s*\Z', '\n', text, flags=re.MULTILINE)
    # Remove special characters that might be artifacts
    text = re.sub(r'[\x00-\x08\x02\x0b\x0c\x0e-\x1f]', '\n', text)


    # Fix newlines inside sentences
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Force hard break BEFORE known medical section headings
    SECTION_PATTERN = re.compile(
        r'(?<!\n)\b(' + "|".join(
        h.replace(" ", r"\s+") for h in MEDICAL_SECTION_HEADINGS
        ) + r')\b\s*:?'
)
    text = re.sub(
        SECTION_PATTERN,
        r"\n\n\1: ",
        text
    )

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


def medical_filter_docs(docs) -> List[Document]:
    med_filter_doc= []
    try: 
        for i, doc in enumerate(docs):
            if i>29 and doc.page_content.strip():  # Ensure non-empty and useful content
                src= doc.metadata.get('source')
                pg= doc.metadata.get('page')
                #create new Document with preprocessed content and filtered metadata
                temp_doc= Document(metadata={"page": pg, "source": src},
                        page_content= medical_preprocess(doc.page_content)
                        
                    )
                med_filter_doc.append(temp_doc)
    except Exception  as dfe:
        logger.error(f"Document filtering error in medical_filter_docs: {dfe}")
        raise DocumentFilterError(f"Failed to filter documents due to document filtering error: {dfe}")
    logger.info(f"Filtered and preprocessed to {len(med_filter_doc)} medical documents")
    return med_filter_doc

