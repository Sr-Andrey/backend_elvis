from fastapi.exceptions import HTTPException
from fastapi import status


is_achievements = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="achievements is already",
)


is_not_achievement = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="is not achievements",
)


is_not_user = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="is not user",
)


is_connection = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="connection is already",
)
