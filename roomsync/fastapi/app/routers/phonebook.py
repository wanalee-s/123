# fastapi/app/routers/phonebook.py
import logging
from typing import List, Dict
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime

from app.db import get_db
from app.models.authuser import PrivateContact, AuthUser
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()  # Align with Express’s /lab10 prefix


def serialize_contacts(contacts: List[PrivateContact]) -> List[Dict]:
    """
    Helper function to serialize a list of PrivateContact objects.
    Assumes each model instance has a to_dict() method.
    """
    return [contact.to_dict() for contact in contacts]


@router.get("/contacts")
async def get_contacts(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.debug(f"Authenticated user ID: {current_user.id}")
    if not current_user:
        raise HTTPException(
            status_code=401, detail="Unauthorized: No current user")
    try:
        contacts = (
            db.query(PrivateContact)
            .filter(PrivateContact.owner_id == current_user.id)
            .filter(PrivateContact.deletedAt.is_(None))  # Updated to deletedAt
            .all()
        )
        return serialize_contacts(contacts)
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/remove_contact")
async def remove_contact(
    request: Request,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Error reading request body: {e}")
        data = {}

    contact_id = data.get("id")
    if not contact_id:
        logger.error("Error: No ID provided for removal.")
        contacts = (
            db.query(PrivateContact)
            .filter(PrivateContact.owner_id == current_user.id)
            .filter(PrivateContact.deletedAt.is_(None))
            .all()
        )
        return serialize_contacts(contacts)

    try:
        try:
            contact_id = int(contact_id)
        except ValueError:
            logger.error(f"Invalid contact ID for removal: {contact_id}")
            raise HTTPException(status_code=400, detail="Invalid contact ID")

        contact = db.query(PrivateContact).get(contact_id)
        if contact and contact.owner_id == current_user.id:
            logger.info(f"Soft deleting contact: {contact.id} (Owner: {contact.owner_id})")
            contact.delete()  # Uses custom delete()
            db.add(contact) # Explicitly add to session
            db.commit()
        else:
            logger.error(
                f"Error: Contact {contact_id} not found or unauthorized removal attempt.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing contact with id {contact_id}: {e}")

    contacts = (
        db.query(PrivateContact)
        .filter(PrivateContact.owner_id == current_user.id)
        .filter(PrivateContact.deletedAt.is_(None))  # Updated to deletedAt
        .all()
    )
    return serialize_contacts(contacts)


@router.post("/")
async def create_or_update_contact(
    request: Request,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Error reading request body: {e}")
        data = {}

    valid_keys = ["firstname", "lastname", "phone"]
    validated = {}
    for key in valid_keys:
        if key not in data:
            logger.debug(f"Key {key} missing in request data")
            contacts = (
                db.query(PrivateContact)
                .filter(PrivateContact.owner_id == current_user.id)
                # Updated to deletedAt
                .filter(PrivateContact.deletedAt.is_(None))
                .all()
            )
            return serialize_contacts(contacts)
        value = str(data.get(key)).strip()
        if not value or value == "undefined":
            logger.debug(f"Key {key} is invalid in request data")
            contacts = (
                db.query(PrivateContact)
                .filter(PrivateContact.owner_id == current_user.id)
                # Updated to deletedAt
                .filter(PrivateContact.deletedAt.is_(None))
                .all()
            )
            return serialize_contacts(contacts)
        validated[key] = value

    if len(validated) != len(valid_keys):
        logger.debug("Validated data incomplete: " + str(validated))
        contacts = (
            db.query(PrivateContact)
            .filter(PrivateContact.owner_id == current_user.id)
            .filter(PrivateContact.deletedAt.is_(None))  # Updated to deletedAt
            .all()
        )
        return serialize_contacts(contacts)

    try:
        if not data.get("id"):
            validated["owner_id"] = current_user.id
            logger.debug(f"Creating new contact with data: {validated}")
            new_contact = PrivateContact(**validated)
            db.add(new_contact)
        else:
            try:
                contact_id = int(data["id"])
            except ValueError:
                logger.error(f"Invalid contact ID format: {data['id']}")
                raise HTTPException(status_code=400, detail="Invalid contact ID")

            contact = db.query(PrivateContact).get(contact_id)
            if contact:
                logger.debug(f"Found contact {contact.id}, owner: {contact.owner_id}, current_user: {current_user.id}")
                
            if contact and contact.owner_id == current_user.id:
                logger.info(f"Updating contact id {contact_id} with data: {validated}")
                for key, value in validated.items():
                    setattr(contact, key, value)
                contact.updatedAt = datetime.utcnow() 
                db.add(contact) # Explicitly add to session to be safe
            else:
                logger.error(f"Error: Contact {contact_id} not found or unauthorized update. Owner: {contact.owner_id if contact else 'None'} vs User: {current_user.id}")
                contacts = (
                    db.query(PrivateContact)
                    .filter(PrivateContact.owner_id == current_user.id)
                    .filter(PrivateContact.deletedAt.is_(None))
                    .all()
                )
                return serialize_contacts(contacts)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        contacts = (
            db.query(PrivateContact)
            .filter(PrivateContact.owner_id == current_user.id)
            .filter(PrivateContact.deletedAt.is_(None))  # Updated to deletedAt
            .all()
        )
        return serialize_contacts(contacts)

    contacts = (
        db.query(PrivateContact)
        .filter(PrivateContact.owner_id == current_user.id)
        .filter(PrivateContact.deletedAt.is_(None))  # Updated to deletedAt
        .all()
    )
    return serialize_contacts(contacts)
