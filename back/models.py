from database import Base
from sqlalchemy import Column, Integer, String

class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)