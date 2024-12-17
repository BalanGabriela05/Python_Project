from database.Models import Notifications, Series

def list_notifications(db, user_id):
    """
    Lists all notifications for a user.

    Parameters:
    db (Session): The database session.
    user_id (int): The ID of the user.

    """
    notifications = db.query(Notifications).join(Series).filter(Series.user_id == user_id, Series.snoozed == False).all()
    if notifications:
        for notification in notifications:
            series = db.query(Series).filter(Series.id == notification.series_id).first()
            if series:
                print(f"Series name: {series.name}")
                print(f"Next episode to watch: {notification.new_episode}")
                print(f"Episode air date: {notification.notification_date}")
    else:
        print("No notifications found.")