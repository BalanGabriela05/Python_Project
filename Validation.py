import re

def is_valid_episode_format(episode: str) -> bool:
    """
    Check if the episode format is valid.

    Parameters:
    episode (str): The episode format to check.

    Returns:
    bool: True if the format is valid, False otherwise.
    """
    return re.match(r'^S[1-9]\d*E\d*$', episode) is not None

def is_valid_score(score: float)-> bool:
    """
    Check if the score is valid.

    Parameters:
    score (int): The score to check.

    Returns:
    bool: True if the score is valid, False otherwise.
    """
    return 1 <= score <= 10

def is_valid_link_imdb(link: str) -> bool:
    """
    Check if the IMDB link is valid.

    Parameters:
    link (str): The IMDB link to check.

    Returns:
    bool: True if the link is valid, False otherwise.
    """
    return re.match(r'^https://www.imdb.com/title/tt\d{7}/.*$', link) is not None