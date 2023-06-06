    import time
    from plyer import notification
    from win10toast import ToastNotifier

    # Sleep until the reminder time
    time.sleep(time_difference_seconds)

    # Display the notification using plyer
    notification.notify(
        title="Reminder",
        message=reminder_text,
        timeout=10  # Notification display time (in seconds)
    )

    # Display the notification using win10toast with a longer duration
    toaster = ToastNotifier()
    toaster.show_toast("Reminder", reminder_text, duration=15)