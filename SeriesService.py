from sqlalchemy.orm import Session
from database.Models import Series
from sqlalchemy import func

def add_series(db: Session, user_id: int, name: str, imdb_link: str, last_episode: str, score: int, snoozed: bool) -> Series:
    """
    Adds a new series to the database.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user adding the series.
    name (str): The name of the series.
    imdb_link (str): The IMDB link of the series.
    last_episode (str): The last episode watched in format SXEY.
    score (int): The score of the series between 1 and 10.

    Returns:
    new_series (Series): The newly added series.

    """
    new_series = Series(
        user_id=user_id,
        name=name,
        imdb_link=imdb_link,
        last_episode=last_episode,
        score=score,
        snoozed=snoozed
    )
    db.add(new_series)
    db.commit()
    db.refresh(new_series)
    return new_series


def delete_series(db: Session, user_id: int, series_name: str) -> bool:
    """
    Deletes a series from the database.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.
    series_name (str): The name of the series to delete.

    Returns:
    bool: True if the series is deleted successfully, False otherwise.
    """
    # func.lower is used to make the search case-insensitive
    series = db.query(Series).filter(func.lower(Series.name) == func.lower(series_name), Series.user_id == user_id).first()
    if series:
        db.delete(series)
        db.commit()
        return True
    return False

def update_score(db: Session, user_id: int, series_name: str, new_score: float) -> bool:
    """
    Updates the score of a series.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user updating the series.
    series_name (str): The name of the series.
    new_score (float): The new score to set.

    Returns:
    bool: True if the score is updated successfully, False otherwise.
    """
    series = db.query(Series).filter(func.lower(Series.name) == func.lower(series_name), Series.user_id == user_id).first()
    if series:
        series.score = new_score
        db.commit()
        db.refresh(series)
        return True
    return False

def snooze_unsnooze_series_old(db: Session, user_id: int, series_name: str) -> bool:
    """
    Toggles the snoozed status of a series.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.
    series_name (str): The name of the series.

    Returns:
    bool: The new snoozed status of the series.
    """
    series = db.query(Series).filter(func.lower(Series.name) == func.lower(series_name), Series.user_id == user_id).first()
    if series:
        series.snoozed = not series.snoozed
        db.commit()
        db.refresh(series)
        print(f"New snoozed status: {series.snoozed}")
        return series.snoozed
    return False

def series_exists(db: Session, user_id: int, name: str) -> bool:
    """
    Checks if a series exists in the database.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.
    name (str): The name of the series.

    Returns:
    bool: True if the series exists, False otherwise.
    """
    series = db.query(Series).filter(func.lower(Series.name) == func.lower(name), Series.user_id == user_id).first()
    return series is not None

def update_last_episode(db: Session, user_id: int, series_id: int, last_episode: str) -> Series:
    """
    Updates the last watched episode of a series.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user updating the series.
    series_id (int): The ID of the series to update.
    last_episode (str): The last episode watched in format SXEY.

    Returns:
    updated_series (Series): The updated series.

    """
    series = db.query(Series).filter(Series.id == series_id, Series.user_id == user_id).first()
    if not series:
        print("Series not found.")
        return None
    series.last_episode = last_episode
    db.commit()
    db.refresh(series)
    return series

from sqlalchemy.orm import Session
from database.Models import Series

def snooze_unsnooze_series(db: Session, user_id: int, series_id: int):
    """
    Function to snooze or unsnooze a series.
    
    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.
    series_id (int): The ID of the series.
    
    Returns: The updated series.
    """
    series = db.query(Series).filter(Series.id == series_id, Series.user_id == user_id).first()
    if not series:
        print("Series not found.")
        return None
    series.snoozed = not series.snoozed
    db.commit()
    db.refresh(series)
    return series 

def get_series_by_name(db: Session, user_id: int, series_name: str) -> Series:
    """
    Returns a series by name.
    
    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.
    series_name (str): The name of the series.
    
    Returns: The series with the given name.
    
    """
    series = db.query(Series).filter(func.lower(Series.name) == func.lower(series_name), Series.user_id == user_id).first()
    return series