from config_data.config import Config, load_config
from sqlalchemy import create_engine, Column, String, BigInteger, DateTime
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker


config: Config = load_config('.env')

engine = create_engine(f"postgresql+psycopg2://postgres:{config.db.db_password}@{config.db.db_host}/"
                       f"{config.db.database}")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)                   # Ид
    username = Column(String)                                   # Логин
    name = Column(String)                                       # Имя
    surname = Column(String)                                    # Фамилия
    character = Column(String, default='mario')                 # Персонаж
    time = Column(DateTime)                                     # Дата и время


class Character(Base):
    __tablename__ = 'characters'

    id = Column(BigInteger, primary_key=True)                    # Ид
    name = Column(String)                                        # Имя
    meeting_message = Column(String)                             # Приветственное сообщение
    content = Column(String)                                     # Инструкция


class History(Base):
    __tablename__ = 'history'

    id = Column(BigInteger, primary_key=True)                    # Ид
    message_user = Column(String)                                # Вопрос
    answer_user = Column(String)                                 # Ответ
    time = Column(DateTime)                                      # Дата и время


Base.metadata.create_all(bind=engine)
