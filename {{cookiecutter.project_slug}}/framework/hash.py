import base64

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str,
                    hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def encoded_base64(plain_text: str) -> str:
    message_bytes = plain_text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def encoded_base64_basic_auth(username: str,
                              password: str) -> str:
    return encoded_base64(f"{username}:{password}")
