import sys
from database.Connection import get_db
from database.Models import User, Series
from SeriesService import add_series, delete_series, update_score, snooze_unsnooze_series
from UserService import login, sign_up
from Validation import is_valid_episode_format, is_valid_score, is_valid_link_imdb
from SearchSeries import save_series_notification, exist_series
from NotificationsService import list_notifications

def main():
    # Get the database session
    db = next(get_db())
    user_logged_in = None  

    while True:
        """

        Main menu for the application.

        If the user is not logged in, they can choose to login or sign up.
        If the user is logged in, they can choose to :
        a. Add series
        b. Delete series
        c. Update score
        d. Snooze/Unsnooze series
        e. List notifications for series
        f. Log out

        """
        if not user_logged_in:
            print("1. Login")
            print("2. Sign Up")
            choice_status = input("Choose an option: ")

            if choice_status == "1":
                username = input("Username: ")
                password = input("Password: ")
                if login(username, password, db):
                    user_logged_in = username
                    print(f"Welcome, {user_logged_in}!")
                else:
                    continue  

            elif choice_status == "2":
                username = input("Choose a username: ")
                password = input("Choose a password: ")
                if sign_up(username, password, db):
                    user_logged_in = username
                else:
                    continue

        else:
            user_id = db.query(User).filter(User.username == user_logged_in).first().user_id
            print("a. Add series")
            print("b. Delete series")
            print("c. Update score")
            print("d. Snooze/Unsnooze series")
            print("e. List notifications for series")
            print("f. Log out")
            choice = input("Choose an option: ")

            if choice == "a":
                name = input("Series name: ")
                imdb_link = input("IMDB link: ")
                while not is_valid_link_imdb(imdb_link):
                    print("Invalid IMDB link. Please enter a valid IMDB link.")
                    imdb_link = input("IMDB link: ")
                last_episode = input("Last episode watched (format SXEY): ")
                while not is_valid_episode_format(last_episode):
                    print("Invalid format. Please use SXEY where X and Y are numbers.")
                    last_episode = input("Last episode watched (format SXEY): ")
                while not exist_series(imdb_link, last_episode):
                    print("Series not found. Please enter a valid series.")
                    last_episode = input("Last episode watched (format SXEY): ")
                    while not is_valid_episode_format(last_episode):
                        print("Invalid format. Please use SXEY where X and Y are numbers.")
                        last_episode = input("Last episode watched (format SXEY): ")

                score = float(input("Score (1-10): "))
                while not is_valid_score(score):
                    print("Invalid score. Please enter a number between 1 and 10.")
                    score = float(input("Score (1-10): "))

                snoozed = int(input("Snoozed (1 for True, 0 for False): "))
                while not snoozed in [0, 1]:
                    print("Invalid snoozed value. Please enter 1 or 0.")
                    snoozed = int(input("Snoozed (1 for True, 0 for False): "))
                
                add_series(db, user_id, name, imdb_link, last_episode, score, snoozed)
                print("Series added!")

                # Save notification for the next episode
                series_id = db.query(Series).filter(Series.name == name, Series.user_id == user_id).first().id

                if save_series_notification(db, series_id, last_episode):
                    print("Notification saved.")
                else:
                    print("Notification not saved.")
                
            elif choice == "b":
                series_id = int(input("Enter the ID of the series to delete: "))
                if delete_series(db, user_id, series_id):
                    print("Series deleted.")
                else:
                    print("Series not found.")

            elif choice == "c":
                series_id = int(input("Enter the ID of the series to update: "))
                new_score = float(input("Enter the new score (1-10): "))
                while not is_valid_score(new_score):
                    print("Invalid score. Please enter a number between 1 and 10.")
                    new_score = float(input("Enter the new score (1-10): "))
                
                update_score(db, user_id, series_id, new_score)
                print("Score updated.")

            elif choice == "d":
                series_id = int(input("Enter the ID of the series to update: "))
                if snooze_unsnooze_series(db, user_id, series_id):
                    print("Series snoozed.")
                else:
                    print("Series unsnoozed.")


            elif choice == "e":
                list_notifications(db, user_id)

            elif choice == "f":
                print(f"Goodbye, {user_logged_in}!")
                user_logged_in = None  
                sys.exit()  
            else:
                print("Invalid choice. Please choose :")

if __name__ == "__main__":
    main()