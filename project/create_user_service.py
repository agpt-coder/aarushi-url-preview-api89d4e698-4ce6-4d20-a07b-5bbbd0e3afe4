import prisma
import prisma.models
from fastapi import HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Confirms the creation of a new user. Returns the user ID and a message indicating success.
    """

    user_id: str
    message: str


async def create_user(email: str, username: str, password: str) -> CreateUserResponse:
    """
    Endpoint to register a new user.

    Args:
    email (str): The email address of the user. Must be unique.
    username (str): The chosen username for the user. Usernames should be unique but this is not strictly enforced.
    password (str): The password chosen by the user. It will be hashed before storage.

    Returns:
    CreateUserResponse: Confirms the creation of a new user. Returns the user ID and a message indicating success.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    hashed_password = bcrypt.hash(password)
    user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password}
    )
    return CreateUserResponse(user_id=user.id, message="User created successfully.")
