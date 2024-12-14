from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:root@localhost:1234/pythonproject"

# The engine object is used to connect to the database and execute SQL queries
engine = create_engine(DATABASE_URL)

# The session object is used to interact with the database
Session = sessionmaker(bind=engine)

def get_db():
    """
    Generator function to get a database session.

    Yields: 
    db (Session): The database session.

    This function ensures that the database session is properly closed
    after use, and handles any exceptions that occur during the session.
    """
    db = Session()
    try:
        yield db # return the database session 
    except Exception as e:
        print(f"Database error: {e}")
        db.rollback()  # rollback the transaction in case of an error
        raise 
    finally:
        db.close()
