from sqlalchemy.orm import Session
from database.Models import Series

def add_series(db: Session, user_id: int, name: str, imdb_link: str, last_episode: str, score: int) -> Series:
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
        score=score
    )
    db.add(new_series)
    db.commit()
    db.refresh(new_series)
    return new_series