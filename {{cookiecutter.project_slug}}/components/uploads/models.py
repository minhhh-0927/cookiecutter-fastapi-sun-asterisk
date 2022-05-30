from sqlalchemy import Boolean, Column, Integer, String, text, Float
from sqlalchemy.dialects.postgresql import UUID

from components.core.models import ModelBase


class Upload(ModelBase):

    __abstract__ = True

    # Make sure the extension is uuid-ossp enabled.
    # Ref: https://stackoverflow.com/a/22446521
    id = Column(UUID, server_default=text("uuid_generate_v4()"), primary_key=True)
    filename = Column(String(256), unique=True, index=True, nullable=False)
    filesize = Column(Float, default=0.0)


class LocalUpload(Upload):

    __tablename__ = "local_uploads"

    filepath = Column(String(256), nullable=False)
