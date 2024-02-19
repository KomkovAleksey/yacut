"""
Файл дополнительных функций
"""
import re
import random
import hashlib
from http import HTTPStatus

from . import db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .constants import (
    ErrorTextYacut,
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
    while URLMap.query.filter_by(short=short_id).first() is not None:
        get_unique_short_id(long_url)
    return short_id


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


def validate_data(data):
    """Функция проверяющая данные из POST запроса."""
    if not data:
        raise InvalidAPIUsage(ErrorTextYacut.REQUEST_BODY_MISSING)
    if not data.get('url'):
        raise InvalidAPIUsage(ErrorTextYacut.URL_MISSING)
    custom_id = data.get('custom_id')
    if not custom_id or custom_id == '':
        custom_id = get_unique_short_id(data.get('url'))
        data['custom_id'] = custom_id
    else:
        if len(custom_id) > CUSTOM_SHORT_ID_MAX_LENGTH or not re.match(ALLOWED_CHARACTERS, custom_id):
            raise InvalidAPIUsage(
                ErrorTextYacut.SHORT_LINK_INVALID_NAME,
                HTTPStatus.BAD_REQUEST
            )
        if URLMap.query.filter_by(short=data.get('custom_id')).first() is not None:
            raise InvalidAPIUsage(ErrorTextYacut.SHORT_ID_DUPLICTE)
