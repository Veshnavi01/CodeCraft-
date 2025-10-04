from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, auth, utils

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(email: str, password: str, company_name: str, db: Session = Depends(get_db)):
    company = models.Company(name=company_name, currency="USD")
    db.add(company)
    db.commit()
    db.refresh(company)
    user = crud.create_user(db, email, password, role="Admin", company_id=company.id)
    return {"email": user.email, "company": company.name}

@app.post("/expense")
def create_expense(user_id: int, amount: float, currency: str, description: str, category: str, db: Session = Depends(get_db)):
    expense = crud.create_expense(db, user_id, amount, currency, description, category)
    return expense

@app.post("/upload_receipt")
def upload_receipt(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    text = utils.extract_text_from_receipt(file_location)
    return {"extracted_text": text}
