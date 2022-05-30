from sqlalchemy import func, Column, DateTime, Boolean

from config.settings import Base


class ModelBase(Base):
    
    __abstract__ = True

    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())
    del_flag = Column(Boolean, default=False) # del_flag = True is deleted
