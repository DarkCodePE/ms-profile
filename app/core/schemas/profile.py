# app/schemas/profile.py
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from uuid import UUID


class LocationSchema(BaseModel):
    country: str
    city: str
    address: Optional[str] = None


class ContactInfo(BaseModel):
    email: str
    phone: Optional[str]


class Language(BaseModel):
    language: str
    proficiency: str


class WorkExperienceCreate(BaseModel):
    company_name: str
    position: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    current: bool = False
    description: Optional[str]


class EducationCreate(BaseModel):
    institution_name: str
    degree: str
    field_of_study: Optional[str]
    start_date: date
    end_date: Optional[date]
    description: Optional[str]


class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    headline: Optional[str]
    about: Optional[str]
    location: Optional[dict]
    contact_info: Optional[ContactInfo]
    skills: List[str]
    languages: List[Language]
    experiences: List[WorkExperienceCreate] = []
    education: List[EducationCreate] = []


class ProfileUpdate(BaseModel):
    pass


class ProfileInDBBase(BaseModel):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Profile(ProfileInDBBase):
    pass
