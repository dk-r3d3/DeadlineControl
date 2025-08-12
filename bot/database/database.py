import sqlite3
from datetime import datetime

from bot.logs import logger


class Database:
    def __init__(self):
        # Подключаемся к базе данных (файл database.db)
        try:
            self.conn = sqlite3.connect("database.db")
            logger.info("Соединение с БД установлено!")
            self.create_tables()
        except sqlite3.Error as e:
            logger.critical(f"Ошибка соединения с БД: {str(e)}")
            raise

    def create_tables(self):
        try:
            self.conn.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    user_at TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_name TEXT NOT NULL,
                    event_date TIMESTAMP NOT NULL,
                    description TEXT,
                    event_at TIMESTAMP,
                    period TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            ''')
            self.conn.commit()
            logger.info("Таблицы созданы")
        except Exception as e:
            logger.info(f"Ошибка создания таблиц\nError: {e}")

    def add_user(self, user_id, username):
        """Добавить пользователя в базу"""
        try:
            self.conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, user_at)
                VALUES (?, ?, ?);
            ''', (user_id, username, datetime.now()))
            self.conn.commit()
            logger.info(f"Пользователь '{username}' добавлен в базу")
        except Exception as e:
            logger.info(f"Ошибка добавления пользователя '{username}' в базу\nError: {e}")

    def add_event(self, user_id, event_name, event_date, description, period):
        """Добавить событие (user_id, event_name, event_date, description, period)"""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO events (user_id, event_name, event_date, description, event_at, period)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', (user_id, event_name, event_date, description, datetime.now().date(), period))
            self.conn.commit()
            logger.info(f"Событие '{event_name}' добавлено в базу к юзеру {user_id}")
        except Exception as e:
            logger.info(f"Ошибка добавления события '{event_name}' в базу\nError: {e}")

    def get_events(self, user_id):
        """Получить все события пользователя"""
        try:
            cursor = self.conn.execute('''
            SELECT event_name, event_date, description, event_at, period
            FROM events WHERE user_id=?;
            ''', (user_id,))
            result = cursor.fetchall()
            logger.info(f"События {result} получены")
            return result

        except Exception as e:
            logger.info(f"Ошибка получения событий из базы\nError: {e}")

    def delete_event(self, user_id, event_name):
        """Удалить событие пользователя"""
        try:
            cursor = self.conn.execute('''
            SELECT event_name FROM events WHERE user_id=? AND event_name=?;
            ''', (user_id, event_name,))
            if not cursor.fetchone():
                logger.info(f"Событие {event_name} не найдено")
                return False
            self.conn.execute('''
            DELETE FROM events WHERE user_id=? AND event_name=?
            ''', (user_id, event_name))
            self.conn.commit()
            logger.info(f"Событие {event_name} удалено")
            return True
        except Exception as e:
            logger.info(f"Ошибка удаления события {event_name}\nError: {e}")

    def close(self):
        # Закрываем соединение с базой
        self.conn.close()
