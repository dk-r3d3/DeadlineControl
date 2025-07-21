import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('logging.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
