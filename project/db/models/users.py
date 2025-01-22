from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), default="user", nullable=False)
    profile_image_url = Column(Text, nullable=True)

    is_phone_number_verified = Column(Boolean, default=False)
    phone_number = Column(String(50))

    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

    status = Column(String(50), default="active")

    auth = relationship("UserAuth", back_populates="user", uselist=False)
    oauth_providers = relationship("UserAuthProvider", back_populates="user")


class UserAuth(Base):
    __tablename__ = "user_auth"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password = Column(String(255), nullable=False)  # hashed password
    last_login = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="auth")


class UserAuthProvider(Base):
    __tablename__ = "user_auth_providers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # google, facebook, etc.
    provider_id = Column(String(255), nullable=False)  # identifier from the provider
    provider_token = Column(Text, nullable=True)  # access token from the provider
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="oauth_providers")
