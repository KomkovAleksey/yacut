"""
Файл дополнительных функций
"""
import re
import random
import hashlib

from . import db
from .models import URLMap
from .exceptions import ShortIdDuplicateError
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
    while get_short_from_db(URLMap, short_id) is not None:
        generaite_unique_short_id(long_url)

    return short_id


def get_short_from_db(model, short):
    """Проверяет наличие short в базе данных."""
    return model.query.filter_by(short=short).first()


def save_original_and_short_id_in_db(model, short_id, original):
    """
    Функция сохраняющая оригинальную ссылку и short_id в базу данных.
    """
    url_map = model(
        original=original,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()


def validate_custom_id(custom_id):
    """Функция валидирующая custom_id"""
    return bool(len(custom_id) > CUSTOM_SHORT_ID_MAX_LENGTH or not re.match(ALLOWED_CHARACTERS, custom_id))


def check_custom_id(model, custom_id, original):
    """
    Проверяет наличие custom_id
    Валидирует custom_id.
    Проверяет наличие custom_id в базе данных.
    Добавляет original и custom_id в базу данных.
    """
    if not custom_id or custom_id == '':
        custom_id = generaite_unique_short_id(original)
    if validate_custom_id(custom_id) is True:
        raise ValueError()
    if get_short_from_db(URLMap, custom_id)is not None:
        raise ShortIdDuplicateError()
    save_original_and_short_id_in_db(
        model,
        custom_id,
        original,
    )
    
    return custom_id
