from typing import List

from fastapi import APIRouter, status, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.contacts import ContactResponse, ContactModel, ContactUpdate
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/birthdays", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db=db)
    return await contact_service.get_upcoming_birthdays()


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    first_name: str | None = Query(default=None, description="Search by first name"),
    last_name: str | None = Query(default=None, description="Search by last name"),
    email: str | None = Query(default=None, description="Search by exact or partial email"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db=db)
    contacts = await contact_service.get_contacts(skip, limit, first_name, last_name, email)
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db=db)
    return await contact_service.create_contact(contact)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db=db)
    contact = await contact_service.get_contact(contact_id)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db=db)
    new_contact = await contact_service.update_contact(contact_id, contact)
    return new_contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db=db)
    deleted_contact = await contact_service.delete_contact(contact_id)
    return deleted_contact
