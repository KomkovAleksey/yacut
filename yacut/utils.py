"""
Файл дополнительных функций
"""
import re
import random
import hashlib

from . import db
from .models import URLMap
from .constants import (
    GENERAITED_SHORT_ID_LENGHT,
    CUSTOM_SHORT_ID_MAX_LENGTH,
    ALLOWED_CHARACTERS,
)


def get_unique_short_id(long_url):
    """Функция формирования short_id."""
    generaited_short_id = random.choices(
        hashlib.md5(long_url.encode()).hexdigest(),
        k=GENERAITED_SHORT_ID_LENGHT
    )
    short_id = ''.join(generaited_short_id)
    while check_in_db(URLMap, short_id) is not None:
        get_unique_short_id(long_url)

    return short_id


def check_in_db(model, short_id):
    """Проверяет наличие short_id в базе."""
    return model.query.filter_by(short=short_id).first()


def add_to_db(model, short_id, original):
    """
    Функция добавляющая оригинальную ссылку и short_id в базу данных.
    """
    url_map = model(
        original=original,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()


def validate_custom_id(custom_id):
    """Функция валидирующа custom_id"""
    return bool(len(custom_id) > CUSTOM_SHORT_ID_MAX_LENGTH or not re.match(ALLOWED_CHARACTERS, custom_id))
