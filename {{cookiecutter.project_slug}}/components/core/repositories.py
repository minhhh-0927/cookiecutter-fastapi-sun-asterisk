from sqlalchemy.orm import Session


class BaseRepositories:

    def __init__(self, db: Session):
        self.db = db
