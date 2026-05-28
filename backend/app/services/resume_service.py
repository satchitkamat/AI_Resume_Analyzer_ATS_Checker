import os
import shutil
import uuid
import fitz

from docx import Document

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.resume import Resume

UPLOAD_DIR = "app/uploads/resumes"
UPLOAD_FOLDER = "uploaded_resumes"

ALLOWED_EXTENSIONS =[
    ".pdf",
    ".docx"
]

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

def extract_text_from_pdf(
        file_path: str
):
    text=""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text

def extract_text_from_docx(
        file_path: str
):
    doc = Document(file_path)

    text= ""

    for para in doc.paragraphs:
        text += para.text+ "\n"

    return text


def upload_resume(
        db: Session,
        file: UploadFile,
        current_user
):
    # Validate extension
    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Only PDF or DOCX files allowed"
        )
    
    # Create unique filename
    unique_filename = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    # Final storage path
    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract file text

    extracted_text = ""

    if file_extension == ".pdf":

        extracted_text = extract_text_from_pdf(
            file_path
        )
    
    elif file_extension == ".docx":

        extracted_text = extract_text_from_docx(
            file_path
        )

    # Create DB record
    new_resume = Resume(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id,
        extracted_text=extracted_text
    )

    db.add(new_resume)

    db.commit()

    db.refresh(new_resume)

    return new_resume