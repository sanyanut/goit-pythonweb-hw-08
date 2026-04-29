from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contacts_repository = ContactRepository(db)

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ):
        return await self.contacts_repository.get_contacts(
            skip, limit, first_name, last_name, email
        )

    async def get_upcoming_birthdays(self):
        return await self.contacts_repository.get_upcoming_birthdays()

    async def get_contact(self, contact_id: int):
        contact = await self.contacts_repository.get_contact_by_id(contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    async def create_contact(self, contact: ContactModel):
        existing_contact = await self.contacts_repository.get_contact_by_email_or_phone(
            contact.email, contact.phone
        )

        if existing_contact:
            if existing_contact.email == contact.email:
                raise HTTPException(
                    status_code=400, detail="Contact with this email already exists"
                )

            if existing_contact.phone == contact.phone:
                raise HTTPException(
                    status_code=400, detail="Contact with this phone already exists"
                )

        return await self.contacts_repository.create_contact(contact)

    async def update_contact(self, contact_id: int, contact: ContactUpdate):
        updated_contact = await self.contacts_repository.update_contact(
            contact_id, contact
        )

        if not updated_contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return updated_contact

    async def delete_contact(self, contact_id: int):
        deleted_contact = await self.contacts_repository.delete_contact(contact_id)

        if not deleted_contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return deleted_contact
