from sqlalchemy.orm import Session
from models import User, Company, Expense
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, email: str, password: str, role: str, company_id: int):
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, password=hashed_password, role=role, company_id=company_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_expense(db: Session, user_id: int, amount: float, currency: str, description: str, category: str):
    expense = Expense(user_id=user_id, amount=amount, currency=currency, description=description, category=category)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses_by_user(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()
