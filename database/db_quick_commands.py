from sqlalchemy.exc import IntegrityError
from database.database import User, session, Character, History
from datetime import datetime
from utils.amplitude import track_user_register, change_character, send_message, take_answer


# Регистрация пользователя в БД
def register_user(message):
    date_now = datetime.now()
    username = message.from_user.username if message.from_user.username else None
    surname = message.from_user.last_name if message.from_user.last_name else None
    user = User(id=int(message.from_user.id), username=username, name=message.from_user.full_name, surname=surname,
                time=date_now)
    session.add(user)
    try:
        session.commit()
        track_user_register(message.from_user.id)
        return True
    except IntegrityError:
        session.rollback()
        return False


# Изменение персонажа в БД
def choice_character(message, character):
    user = session.query(User).filter(User.id == int(message.from_user.id)).first()
    if user:
        user.character = character
        try:
            session.commit()
            change_character(character, message.from_user.id)
            return True
        except IntegrityError:
            session.rollback()
            return False
    else:
        return False


# Считывание приветственного сообщения
def get_message(name):
    character = session.query(Character).filter(Character.name == name).first()
    if character:
        return character.meeting_message
    else:
        return "Здесь ничего нет"


# Считывание настроек персонажа из БД
def get_content(message):
    user = session.query(User).filter(User.id == int(message.from_user.id)).first()
    content = session.query(Character).filter(Character.name == user.character).first()
    if content:
        return content.content
    else:
        return None


# Сохранение сообщения пользователя в БД
def save_message(message):
    date_now = datetime.now()
    messages = History(message_user=message.text, time=date_now)
    session.add(messages)
    try:
        session.commit()
        send_message(message.from_user.id, message.text)
        return True
    except IntegrityError:
        session.rollback()
        return False


# Сохранение ответа от GPT в БД
def save_answer(message, answer):
    messages = session.query(History).filter(History.message_user == message.text).order_by(History.time).first()
    if messages:
        messages.answer_user = answer
        try:
            session.commit()
            take_answer(message.from_user.id, answer)
            return True
        except IntegrityError:
            session.rollback()
            return False
    else:
        return False
