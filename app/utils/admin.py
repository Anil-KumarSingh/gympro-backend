from fastapi import Depends, HTTPException
from app.utils.auth import verify_token


def verify_admin(
    user=Depends(verify_token)
):
    """
    Allow access only to admin users.
    """

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user