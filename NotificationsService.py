from database.Models import Notifications, Series
from sqlalchemy.orm import joinedload

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
                print(f"Youtube trailer: {notification.youtube_trailer}")
                
    else:
        print("No notifications found.")
        

def all_notifications(db, user_id):
    """
    Returnează notificările unui utilizator, inclusiv numele seriei asociate,
    doar pentru seriile care nu sunt snoozed.
    """
    return (
        db.query(Notifications)
        .join(Series, Notifications.series_id == Series.id)
        .filter(Series.user_id == user_id, Series.snoozed == False)  # Adaugă condiția pentru unsnoozed
        .options(joinedload(Notifications.series))  # Încarcă detalii despre serie
        .all()
    )
