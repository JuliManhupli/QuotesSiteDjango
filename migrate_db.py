import os

from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine, Column, String, ARRAY, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
postgres_uri = os.getenv("POSTGRES_URI")

# Підключення до MongoDB
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['goit']
authors_collection = mongo_db['authors']
quotes_collection = mongo_db['quotes']

# Підключення до PostgreSQL
postgres_engine = create_engine(postgres_uri)
Base = declarative_base()


# Оголошення моделей SQLAlchemy
class Author(Base):
    __tablename__ = 'quotes_author'
    id = Column(String, primary_key=True)
    fullname = Column(String, nullable=False)
    born_date = Column(String)
    born_location = Column(String)
    description = Column(String)


class Quote(Base):
    __tablename__ = 'quotes_quote'
    id = Column(String, primary_key=True)
    tags = Column(ARRAY(String))
    author_id = Column(String, ForeignKey('quotes_author.id'))
    quote = Column(String, nullable=False)


# Створення таблиць у PostgreSQL
Base.metadata.create_all(postgres_engine)

# Отримання даних з MongoDB та запис у PostgreSQL
Session = sessionmaker(bind=postgres_engine)
session = Session()


def migrate_data():
    # Міграція авторів
    for author_doc in authors_collection.find():
        author = Author(
            id=str(author_doc['_id']),
            fullname=author_doc['fullname'],
            born_date=author_doc.get('born_date', ''),
            born_location=author_doc.get('born_location', ''),
            description=author_doc.get('description', '')
        )
        session.add(author)

    session.commit()

    # Міграція цитат
    for quote_doc in quotes_collection.find():
        quote = Quote(
            id=str(quote_doc['_id']),
            tags=quote_doc['tags'],
            author_id=str(quote_doc['author']),
            quote=quote_doc['quote']
        )
        session.add(quote)

    try:
        session.commit()
    except IntegrityError:
        # Обробка конфліктів унікальності (наприклад, якщо дублюється primary key)
        session.rollback()

    session.close()


if __name__ == "__main__":
    migrate_data()
