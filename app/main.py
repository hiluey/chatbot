from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, auth, chatbot
from app.models import User, Chat
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.database import Base
from fastapi import APIRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix="/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router_v1.post("/ask", response_model=schemas.ChatOut)

def ask_question(
    chat: schemas.ChatCreate,
    current_user: str = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()

    previous_chats = db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.timestamp.desc()).limit(5).all()
    
    messages = [{"role": "system", "content": "Você é um agente amigável de ajuda."}]
    for c in reversed(previous_chats):
        messages.append({"role": "user", "content": c.question})
        messages.append({"role": "assistant", "content": c.answer})
    
    messages.append({"role": "user", "content": chat.question})
    
    answer = chatbot.ask_openai(messages)

    new_chat = Chat(user_id=user.id, question=chat.question, answer=answer)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    all_chats = db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.timestamp.desc()).all()
    if len(all_chats) > 5:
        for c in all_chats[5:]:
            db.delete(c)
        db.commit()

    return new_chat
app.include_router(router_v1)
