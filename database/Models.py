from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# This is the base class for all models in the application
Base = declarative_base()

class User(Base):
    """
    User model for storing user information

    Attributes:
    user_id (int): The ID of the user.
    username (str): The username of the user.
    password (str): The password of the user.

    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Series(Base):
    """
    Series model for storing series information

    Attributes:
    id (int): The ID of the series.
    user_id (int): The ID of the user adding the series.
    name (str): The name of the series.
    imdb_link (str): The IMDB link of the series.
    last_episode (str): The last episode watched in format SXEY.
    last_viewed_date (Date): The date the series was last viewed.
    score (int): The score of the series between 1 and 10.
    snoozed (bool): Whether the series is snoozed or not.

    """
    __tablename__ = 'infoseries'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    imdb_link = Column(String, nullable=False)
    last_episode = Column(String, nullable=False)
    last_viewed_date = Column(Date)
    score = Column(Integer, nullable=False)
    snoozed = Column(Boolean, default=False)

class Notifications(Base):
    """
    Notification model for storing series notifications

    Attributes:
    id (int): The ID of the notification.
    series_id (int): The ID of the series.
    notification_date (Date): The date of the notification.
    new_episode (str): The new episode information.

    """
    
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('infoseries.id'))
    notification_date = Column(Date)
    new_episode = Column(String)
    youtube_trailer = Column(String)