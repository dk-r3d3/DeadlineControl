from bot.database.database import Database


class DeadLine:
    db = Database()

    def __init__(self, event_name, event_date, description, period):
        self.event_name = event_name
        self.event_date = event_date
        self.description = description
        self.period = period

    def to_dict(self):
        return {
            "event_name": self.event_name,
            "event_date": self.event_date,
            "description": self.description,
            "period": self.period
        }
