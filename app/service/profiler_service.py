import uuid
from datetime import datetime, date

from sqlalchemy.orm import Session

from app.core.model.profile import Profile, Document, WorkExperience, Education
from app.core.schemas.profile import ProfileCreate


def serialize_to_json(data):
    """Convierte datos a JSON serializable."""
    if isinstance(data, dict):
        return {key: serialize_to_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_to_json(item) for item in data]
    elif isinstance(data, (datetime, date)):
        return data.isoformat()  # Convierte fechas a formato ISO
    return data


def save_to_database(parsed_data: ProfileCreate,
                     file_name: str,
                     file_url: str,
                     db: Session,
                     user_id: str
                     ) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=parsed_data.first_name,
        last_name=parsed_data.last_name,
        headline=parsed_data.headline,
        about=parsed_data.about,
        location=parsed_data.location,
        contact_info=parsed_data.contact_info.dict() if parsed_data.contact_info else None,  # Convierte a dict
        skills=parsed_data.skills,
        languages=[lang.dict() for lang in parsed_data.languages] if parsed_data.languages else None,
        # Convierte cada lenguaje a dict
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Guardar experiencias laborales
    if parsed_data.experiences:
        for exp in parsed_data.experiences:
            work_experience = WorkExperience(
                profile_id=profile.id,
                company_name=exp.company_name,
                position=exp.position,
                location=exp.location,
                start_date=exp.start_date,
                end_date=exp.end_date,
                current=exp.current,
                description=exp.description,
            )
            db.add(work_experience)

    # Guardar educación
    if parsed_data.education:
        for edu in parsed_data.education:
            education_entry = Education(
                profile_id=profile.id,
                institution_name=edu.institution_name,
                degree=edu.degree,
                field_of_study=edu.field_of_study,
                start_date=edu.start_date,
                end_date=edu.end_date,
                description=edu.description,
            )
            db.add(education_entry)

    db.commit()
    # Serializar parsed_data
    serialized_data = serialize_to_json(parsed_data.dict())

    document = Document(
        profile_id=profile.id,
        type="CV",
        file_name=file_name,
        file_url=file_url,
        mime_type="application/pdf",
        parsed_data=serialized_data,
    )
    db.add(document)
    db.commit()

    return profile
