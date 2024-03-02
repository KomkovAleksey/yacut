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


def generaite_unique_short_id(long_url):
    """Функция формирования short_id."""
    generaited_short_id = random.choices(
        hashlib.md5(long_url.encode()).hexdigest(),
        k=GENERAITED_SHORT_ID_LENGHT
    )
    short_id = ''.join(generaited_short_id)
    while get_short_from_db(short_id) is not None:
        generaite_unique_short_id(long_url)

    return short_id


def get_short_from_db(short):
    """Проверяет наличие short в базе данных."""
    return URLMap.query.filter_by(short=short).first()


def save_original_and_short_id_in_db(short_id, original):
    """
    Функция сохраняющая оригинальную ссылку и short_id в базу данных.
    """
    url_map = URLMap(
        original=original,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()


def validate_custom_id(custom_id):
    """Функция валидирующая custom_id"""
    return bool(len(custom_id) > CUSTOM_SHORT_ID_MAX_LENGTH or
                not re.match(ALLOWED_CHARACTERS, custom_id))
