from sqlalchemy.orm import Session
from database.Models import Series

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

def delete_series(db: Session, user_id: int, series_id: int) -> bool:
    """
    Deletes a series from the database.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user deleting the series.
    series_id (int): The ID of the series to delete.

    Returns:
    bool: True if the series is successfully deleted, False otherwise.

    """
    series = db.query(Series).filter(Series.id == series_id, Series.user_id == user_id).first()
    if not series:
        # series not found
        return False
    db.delete(series)
    db.commit()
    return True

def update_score(db: Session, user_id: int, series_id: int, new_score: int) -> Series:
    """
    Updates the score of a series.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user updating the score.
    series_id (int): The ID of the series to update.
    new_score (int): The new score of the series between 1 and 10.

    Returns:
    updated_series (Series): The updated series.

    """
    series = db.query(Series).filter(Series.id == series_id, Series.user_id == user_id).first()
    if not series:
        print("Series not found.")
        return None
    series.score = new_score
    db.commit()
    db.refresh(series)
    return series

def snooze_unsnooze_series(db: Session, user_id: int, series_id: int) -> Series:
    """
    Snoozes a series.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user snoozing the series.
    series_id (int): The ID of the series to snooze.

    Returns:
    snoozed_series (Series): The snoozed series.

    """
    series = db.query(Series).filter(Series.id == series_id, Series.user_id == user_id).first()
    if not series:
        print("Series not found.")
        return None
    series.snoozed = not series.snoozed
    db.commit()
    db.refresh(series)
    print(f"New snoozed status: {series.snoozed}")

    return series.snoozed