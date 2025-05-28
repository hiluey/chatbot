import openai
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from app.models import Chat

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_openai(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    return response.choices[0].message.content


def delete_old_chats(user_id: int, db: Session):
    chats = db.query(Chat)\
        .filter(Chat.user_id == user_id)\
        .order_by(Chat.timestamp.desc())\
        .all()

    if len(chats) > 5:
        for chat in chats[5:]:
            db.delete(chat)
        db.commit()