from Database.database import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Float


class Source(Base):
    __tablename__ = "source"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    location = Column(String(100))
    type = Column(String(50))
    capacity = Column(Float)
    status = Column(String(20))
    water_level = Column(Float)
    approvers = Column(String(200))
    complaints = Column(String(2000))
