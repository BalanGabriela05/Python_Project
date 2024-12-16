import requests
import re

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

# function to get show by imdb id
def get_show_by_imdb(imdb_id: str):
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

# function to get all episodes of a show
def get_episodes(show_id: int, season_number: int):
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


def main():
    episode_str = "S9E4"
    season, episode = extract_number_season_episode(episode_str)
    print(f"Season: {season}, Episode: {episode}")  # Output: Season: 9, Episode: 4

    imdb_id = input("Enter IMDb ID (e.g., tt0944947 for Game of Thrones): ")
    last_season = int(input("Last season watched: "))
    last_episode = int(input("Last episode watched: "))


    show = get_show_by_imdb(imdb_id)
    if not show:
        print("Show not found!")
        return

    print(f"Found show: {show['name']}")

    episodes = get_episodes(show["id"], last_season)

    next_episodes = []
    for episode in episodes:
        if episode["episode_number"] > last_episode:
            next_episodes.append(episode)
        if len(next_episodes) == 2:  # stop after finding 2 episodes
            break

    if len(next_episodes) < 2:
        next_season_episodes = get_episodes(show["id"], last_season + 1)
        next_episodes.extend(next_season_episodes[:2 - len(next_episodes)])

 
    if next_episodes:
        print("Next episodes:")
        for ep in next_episodes:
            print(f"Season {ep['season_number']} Episode {ep['episode_number']}: {ep['name']}")
    else:
        print("No new episodes found.")

if __name__ == "__main__":
    main()
