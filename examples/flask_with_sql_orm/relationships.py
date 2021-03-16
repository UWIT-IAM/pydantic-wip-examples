from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserSettingsORM(Base):
    __tablename__ = 'UserSettings'
    email_subscription = Column(Boolean, default=False)
    private_profile = Column(Boolean, default=True)
    email_address = Column(String)
    settings_id = Column(Integer, primary_key=True)


class UserORM(Base):
    __tablename__ = 'User'
    user_id: int = Column(Integer, primary_key=True)
    username: str = Column(String, unique=True)
    settings_id: int = Column(Integer, ForeignKey('UserSettings.settings_id'), nullable=False)
    settings: UserSettingsORM = relationship('UserSettingsORM')
