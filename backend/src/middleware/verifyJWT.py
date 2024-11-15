from fastapi import Depends, HTTPException, status, Request
import jwt
from config import JWT_SECRET

SECRET_KEY = JWT_SECRET  # Replace with your actual secret key
ALGORITHM = "HS256"


async def verify_jwt_token(request: Request):
    token = None

    # Check if the token is in the cookies
    if "access_token" in request.cookies:
        token = request.cookies.get("access_token")
    # Check if the token is in the Authorization header (Bearer Token)
    elif request.headers.get("Authorization"):
        auth_header = request.headers.get("Authorization")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if token:
        try:
            # Decode the token to verify its validity
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload  # Return the decoded payload for use in the endpoint
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing.",
        )
