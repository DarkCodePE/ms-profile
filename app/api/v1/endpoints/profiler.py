# app/api/v1/endpoints/profile.py

from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.loader import extract_text_with_pypdfloader
from app.agent.model import parse_cv_with_openai
from app.config.database import get_db
from app.core.model.profile import Profile
from app.middleware.auth_middleware import require_auth
from app.service.profiler_service import save_to_database
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...),
                    db: Session = Depends(get_db),
                    user: dict = Depends(require_auth())
                    ):
    user_id = user.get("userId")  # Extraer el `user_id` del token validado

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")

    # Guarda el archivo localmente
    directory = "uploaded_files/"
    if not os.path.exists(directory):
        os.makedirs(directory)  # Crear el directorio si no existe

    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extrae texto usando PyPDFLoader
    try:
        pages = extract_text_with_pypdfloader(file_path)
        cv_text = " ".join([page.page_content for page in pages])  # Unimos el contenido de todas las páginas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el PDF: {str(e)}")

    # Procesa el texto con OpenAI
    try:
        parsed_data = parse_cv_with_openai(cv_text)
    except Exception as e:
        logger.error(f"Error al leer el PDF: {e}")
        print(f"Error al leer el PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el CV: {str(e)}")

    # Guarda los datos en la base de datos
    profile = save_to_database(parsed_data, file.filename, file_path, db, user_id)

    return {"profile_id": profile.id, "parsed_data": parsed_data}


@router.get("/{user_id}")
async def get_profile_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Recupera un perfil específico por su ID.
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Serializar datos relacionados del perfil
    experiences = [
        {
            "company_name": exp.company_name,
            "position": exp.position,
            "location": exp.location,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "current": exp.current,
            "description": exp.description,
        }
        for exp in profile.experiences
    ]

    education = [
        {
            "institution_name": edu.institution_name,
            "degree": edu.degree,
            "field_of_study": edu.field_of_study,
            "start_date": edu.start_date.isoformat() if edu.start_date else None,
            "end_date": edu.end_date.isoformat() if edu.end_date else None,
            "description": edu.description,
        }
        for edu in profile.education
    ]

    documents = [
        {
            "file_name": doc.file_name,
            "file_url": doc.file_url,
            "parsed_data": doc.parsed_data,
        }
        for doc in profile.documents
    ]

    return {
        "id": str(profile.id),
        "user_id": profile.user_id,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "headline": profile.headline,
        "about": profile.about,
        "location": profile.location,
        "contact_info": profile.contact_info,
        "skills": profile.skills,
        "languages": profile.languages,
        "experiences": experiences,
        "education": education,
        "documents": documents,
    }
