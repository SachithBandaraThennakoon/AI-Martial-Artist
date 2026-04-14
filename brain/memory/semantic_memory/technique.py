from sqlalchemy import Column, Integer, String
from core.database import Base


class Technique(Base):
    __tablename__ = "techniques"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)