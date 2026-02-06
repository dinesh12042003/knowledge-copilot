from sqlalchemy.orm import Session
from backend.models import User, Message


# ---------- USER ----------

def get_or_create_user(db: Session, google_id, email, name):
    user = db.query(User).filter(User.google_id == google_id).first()

    if not user:
        user = User(
            google_id=google_id,
            email=email,
            name=name
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


# ---------- MESSAGE ----------

def save_message(db: Session, user_id, role, content):
    msg = Message(
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()


def get_chat_history(db: Session, user_id):
    return db.query(Message)\
        .filter(Message.user_id == user_id)\
        .order_by(Message.timestamp)\
        .all()
