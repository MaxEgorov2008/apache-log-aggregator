from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    timestamp = Column(DateTime)
    method = Column(String)
    url = Column(String)
    status = Column(Integer)
    size = Column(Integer)

engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5432/log_db")
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
