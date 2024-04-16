from typing import Dict, Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Provides feedback on the login process, including a session token on successful authentication.
    """

    success: bool
    message: str
    token: Optional[str] = None
    user: Dict[str, str]


async def user_login(username_or_email: str, password: str) -> UserLoginResponse:
    """
    Endpoint for user authentication and login.

    Args:
    username_or_email (str): The username or email address associated with the user's account.
    password (str): The password for the user account. This should be securely transmitted and stored.

    Returns:
    UserLoginResponse: Provides feedback on the login process, including a session token on successful authentication.
    """
    user = await prisma.models.User.prisma().find_first(
        where={"OR": [{"email": username_or_email}, {"id": username_or_email}]}
    )
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    ):
        return UserLoginResponse(
            success=False,
            message="Invalid username/email or password.",
            token=None,
            user={},
        )
    session_token = "generated_session_token"
    user_data = {
        "username": user.id,
        "roles": user.role.name if hasattr(user, "role") else "USER",
    }
    return UserLoginResponse(
        success=True, message="Login successful.", token=session_token, user=user_data
    )
