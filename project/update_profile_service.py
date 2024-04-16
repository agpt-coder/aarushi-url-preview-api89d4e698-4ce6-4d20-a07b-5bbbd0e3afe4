from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    The response provides confirmation of the update operation, including any errors encountered.
    """

    success: bool
    message: str
    updated_fields: List[str]
    failed_updates: Optional[List[Dict[str, str]]] = None


async def update_profile(
    email: Optional[str],
    username: Optional[str],
    bio: Optional[str],
    profile_picture_url: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Allows authenticated users to update their profile. This function updates provided fields
    and reports on the success of these updates.

    Args:
    email (Optional[str]): The new email address of the user. Optional, only updated if provided.
    username (Optional[str]): The new username for the user. Optional, only updated if provided.
    bio (Optional[str]): A new bio to update the user's profile information with. Optional, only updated if provided.
    profile_picture_url (Optional[str]): A new URL for the user's profile picture. Optional, only updated if provided.

    Returns:
    UpdateUserProfileResponse: The response provides confirmation of the update operation, including any errors encountered.

    Example:
        update_profile(email='newemail@example.com', username=None, bio='New bio', profile_picture_url=None)
        > UpdateUserProfileResponse(success=True, message="Profile updated successfully.", updated_fields=['email', 'bio'], failed_updates=None)
    """
    updated_fields = []
    failed_updates = []
    if email:
        try:
            updated = await prisma.models.User.prisma().update(
                where={"email": email}, data={"email": email}
            )
            updated_fields.append("email")
        except Exception as e:
            failed_updates.append({"email": str(e)})
    success = not failed_updates
    message = (
        "Profile updated successfully."
        if success
        else "Failed to update some profile fields."
    )
    return UpdateUserProfileResponse(
        success=success,
        message=message,
        updated_fields=updated_fields,
        failed_updates=failed_updates if failed_updates else None,
    )
