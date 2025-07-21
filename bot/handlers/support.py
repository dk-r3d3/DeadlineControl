from datetime import datetime


def date_validation(date):
    event_dt = datetime.strptime(date, "%d.%m.%Y").date()
    date_now = datetime.now().date()
    if date_now > event_dt:
        return False
    else:
        return True


def display_period(period, event_date):
    # 1 день
    # 2, 3, 4 дня
    # 5, 6, 7, 8, 9, 0 (else) дней
    event_dt = datetime.strptime(event_date, "%d.%m.%Y")
    remained = (event_dt.date() - datetime.now().date()).days

    if period == "on_the_date" and remained == 0:
        return "Событие сегодня!"

    elif period == "everyday" and remained >= 0:
        remained_str = str(remained)
        last_index = remained_str[len(remained_str) - 1]
        if last_index == "1":
            return f"{remained} день"
        elif last_index == "2" \
                or last_index == "3" \
                or last_index == "4":
            return f"{remained} дня"
        else:
            return f"{remained} дней"

    elif period == "weekly" and remained >= 0:
        week_left = remained // 7
        remained_str = str(week_left)
        last_index = remained_str[len(remained_str) - 1]
        if last_index == "1":
            return f"{week_left} неделя"
        elif last_index == "2" \
                or last_index == "3" \
                or last_index == "4":
            return f"{week_left} недели"
        else:
            return f"{week_left} недель"  # Каждые 7 дней до события

    elif period == "monthly" and remained == 0:
        month_left = remained // 30
        remained_str = str(month_left)
        last_index = remained_str[len(remained_str) - 1]
        if last_index == "1":
            return f"{month_left} месяц"
        elif last_index == "2" \
                or last_index == "3" \
                or last_index == "4":
            return f"{month_left} месяца"
        else:
            return f"{month_left} месяцев"  # Каждые 7 дней до события


def period_remain(period):
    if period == 'everyday':
        return "Ежедневно"
    elif period == 'weekly':
        return "Еженедельно"
    elif period == 'monthly':
        return "Ежемесячно"
    elif period == 'on_the_date':
        return "В день события"
