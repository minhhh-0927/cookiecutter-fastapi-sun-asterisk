from typing import Optional

from sqlalchemy import select

from components.core.repositories import BaseRepositories
from components.users.models import User


# from components.products.models import Product
# from components.products.mappers import ProductCreate


class UserRepositories(BaseRepositories):

    async def is_user_exists(self, user_id: int):
        stmt = select(User).where(User.id == user_id).exists()
        return self.db.query(stmt).scalar()

    async def retrieve_user_by_id(self, user_id: int):
        return self.db.query(User).filter_by(id=user_id).first()

    async def retrieve_user_by_email(self, email: str):
        return self.db.query(User).filter_by(email=email).first()

    async def get_users(self,
                  email: Optional[str] = None,
                  user_id: Optional[int] = None,
                  limit: Optional[int] = None,
                  offset: Optional[int] = None):
        queryset = self.db.query(
            User.email,
            User.id,
            User.is_active
        )
        if user_id:
            queryset = queryset.filter(User.id == user_id)
        if email:
            queryset = queryset.filter(User.email == email)
        total_count = queryset.count()
        data = queryset.offset(offset).limit(limit).all()
        return data, int(total_count)

    async def create_user(self,
                    email: str,
                    password: str):
        user = User(email=email, hashed_password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def update_user(self,
                    user_id: int,
                    email: Optional[str],
                    password: Optional[str]):
        data = dict(
            email=email,
            hashed_password=password
        )
        updated_fields = {k: v for k, v in data.items() if v is not None}
        self.db.query(User).filter_by(id=user_id).update(updated_fields)
        self.db.commit()
        return
