from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100)
    )

    email = Column(
        String(100),
        unique=True,
        index=True
    )

    password = Column(
        String(255)
    )

    google_id = Column(
    String(255),
    unique=True,
    nullable=True
   )
    auth_provider = Column(
    String(50),
    default="email"
   )