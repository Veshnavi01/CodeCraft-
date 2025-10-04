from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    currency = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # Admin / Manager / Employee
    company_id = Column(Integer, ForeignKey("companies.id"))
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    company = relationship("Company")
    
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    category = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")  # Pending/Approved/Rejected
    current_approver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
