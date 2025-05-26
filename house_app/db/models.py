from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from house_app.db.database import Base
from datetime import datetime
from typing import Optional, List


class House(Base):
    __tablename__ = "house"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    GrLivArea: Mapped[int] = mapped_column(Integer)
    YearBuilt: Mapped[int] = mapped_column(Integer)
    GarageCars: Mapped[int] = mapped_column(Integer)
    TotalBsmtSF: Mapped[int] = mapped_column(Integer)
    FullBath: Mapped[int] = mapped_column(Integer)
    OverallQual: Mapped[int] = mapped_column(Integer)
    Neighborhood: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates='user',
                                                        cascade='all, delete')


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')