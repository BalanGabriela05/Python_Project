from sqlalchemy.orm import Session
from database.Models import User

def login(username: str, password: str, db: Session) -> bool:
    """
    Logs in a user.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.
    db (Session): The database session.

    Returns:
    bool: True if the login is successful, False otherwise.

    """
    user = db.query(User).filter(User.username == username).first() # query the database for the user with the given username
    if not user:
        print("Username not found. Please try again.")
        return False
    if user.password != password:
        print("Incorrect password. Please try again.")
        return False
    return True

def sign_up(username: str, password: str, db: Session) -> bool:
    """
    Signs up a new user.

    Parameters:
    username (str): The username of the new user.
    password (str): The password of the new user.
    db (Session): The database session.

    Returns:
    bool: True if the sign up is successful, False otherwise.
    
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print("Username already exists. Please choose a different username.")
        return False

    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    print("Account created successfully!")
    return True
