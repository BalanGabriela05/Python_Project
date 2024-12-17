import requests
import re
from sqlalchemy.orm import Session
from database.Models import Series, Notifications

def extract_imdb_id(imdb_link):
    """
    Extracts the IMDB ID from an IMDB link.

    Parameters:
    imdb_link (str): The IMDB link.

    Returns:
    str: The IMDB ID.
    """
    parts = imdb_link.split('/')
    for part in parts:
        if part.startswith('tt'):
            return part
    return None

def extract_number_season_episode(episode_str):
    """
    Extracts the season and episode number from a string in the format SXEY.

    Parameters:
    episode_str (str): The episode string (e.g., S9E4).

    Returns:
    tuple: A tuple containing the season number and episode number.
    """
    match = re.match(r'S(\d+)E(\d+)', episode_str)
    if match:
        season_number = int(match.group(1))
        episode_number = int(match.group(2))
        return season_number, episode_number
    else:
        raise ValueError("Invalid episode format. Please use SXEY where X and Y are numbers.")


TMDB_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmVhYzUwM2M5MDUzNGJiZGZlMDI2NmQzYTU3YTlmMiIsIm5iZiI6MTczNDI5MjcyMy44MzksInN1YiI6IjY3NWYzNGYzZDZmNWU4NDU4YjhiNDZmOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.66CEr0xeGc7xysF7MQb-dxur891eTM45roAfJZzZgI0" 
BASE_URL = "https://api.themoviedb.org/3"

def get_show_by_imdb(imdb_id: str):
    """
    Get show information by IMDB ID.

    Parameters:
    imdb_id (str): The IMDB ID.

    Returns: show ID
    """

    url = f"{BASE_URL}/find/{imdb_id}"
    headers = {
        "Authorization": f"Bearer {TMDB_API_TOKEN}",
        "accept": "application/json"
    }
    params = {
        "external_source": "imdb_id"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["tv_results"][0]  # return first result
    else:
        print(f"Error fetching show: {response.status_code}")
        return None


def get_episodes(show_id: int, season_number: int):
    """
    Get episodes of a show by show ID and season number.

    Parameters:
    show_id (int): The show ID.
    season_number (int): The season number.

    Returns: the next episode of the show afeter the last watched episode
    """

    url = f"{BASE_URL}/tv/{show_id}/season/{season_number}"
    headers = {
        "Authorization": f"Bearer {TMDB_API_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["episodes"]
    else:
        print(f"Error fetching episodes: {response.status_code}")
        return []


def save_series_notification(db: Session, series_id: int, last_episode: str) -> bool:
    """
    Save a notification for the next episode of a series.

    Parameters:
    db (Session): The database session.
    series_id (int): The ID of the series.
    last_episode (str): The last episode watched in format SXEY.

    Returns: True if the notification is saved successfully, False otherwise.
    """

    series = db.query(Series).filter(Series.id == series_id).first()
    if not series:
        print("Series not found.")
        return

    show = get_show_by_imdb(extract_imdb_id(series.imdb_link))
    if not show:
        print("Show not found.")
        return
    
    nr_season, nr_episode = extract_number_season_episode(last_episode)
    episodes = get_episodes(show["id"], nr_season)
    if not episodes:
        print("No episodes found.")
        return

    next_episodes = []
    for episode in episodes:
        if episode["episode_number"] > nr_episode:
            next_episodes.append(episode)
        if len(next_episodes) == 1:  # stop after finding 1 episode
            break

    if len(next_episodes) < 1:
        next_season_episodes = get_episodes(show["id"], nr_season + 1)
        next_episodes.extend(next_season_episodes[:1 - len(next_episodes)])  

    if next_episodes:
        for episode in next_episodes:
            notification = Notifications(
                series_id=series_id,
                notification_date=episode["air_date"],
                new_episode=f"Season {episode['season_number']} Episode {episode['episode_number']}: {episode['name']}",
                youtube_trailer=f"https://www.youtube.com"
            )
            db.add(notification)
    else:
        notification = Notifications(
            series_id=series_id,
            notification_date=None,
            new_episode="The next episode has not been released yet.",
            youtube_trailer=f"https://www.youtube.com"
        )
        db.add(notification)

    db.commit()
    return True

def exist_series(imdb_link: str, last_episode: str) -> bool:
    """
    Check if a series exists in the TMDB API.

    Parameters:
    imdb_link (str): The IMDB link of the series.
    last_episode (str): The last episode watched in format SXEY.

    Returns:
    bool: True if the series exists, False otherwise.
    """
    imdb_id = extract_imdb_id(imdb_link)
    show = get_show_by_imdb(imdb_id)
    if not show:
        return False

    nr_season, nr_episode = extract_number_season_episode(last_episode)
    episodes = get_episodes(show["id"], nr_season)
    if not episodes:
        return False

    for episode in episodes:
        if episode["episode_number"] == nr_episode:
            return True

    return False