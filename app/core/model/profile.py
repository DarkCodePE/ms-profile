from datetime import datetime
from typing import List
import uuid
from sqlalchemy import Column, String, DateTime, JSON, ARRAY, Text, ForeignKey, Date, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.config.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    headline = Column(String(200))
    about = Column(Text)
    location = Column(JSONB)
    contact_info = Column(JSONB)
    skills = Column(ARRAY(String))
    languages = Column(ARRAY(JSONB))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    experiences = relationship("WorkExperience", back_populates="profile")
    education = relationship("Education", back_populates="profile")
    #certifications = relationship("Certification", back_populates="profile")
    documents = relationship("Document", back_populates="profile")


# app/models/experience.py
class WorkExperience(Base):
    __tablename__ = "work_experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    company_name = Column(String(200))
    position = Column(String(200))
    location = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    current = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="experiences")


# app/models/document.py
class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    type = Column(String(50))  # CV, portfolio, etc.
    file_name = Column(String(255))
    file_url = Column(String(500))
    mime_type = Column(String(100))
    size = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    extracted_text = Column(Text, nullable=True)  # Para almacenar el texto extraído del CV
    parsed_data = Column(JSONB, nullable=True)  # Para almacenar los datos estructurados extraídos

    profile = relationship("Profile", back_populates="documents")


class Education(Base):
    __tablename__ = "education"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    institution_name = Column(String(200))
    degree = Column(String(200))
    field_of_study = Column(String(200), nullable=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="education")