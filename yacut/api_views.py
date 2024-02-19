"""
Файл функций и методов обработки запросов и отправки ответов через API.
"""
from http import HTTPStatus
import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id
from .constants import (
    ErrorTextYacut,
    ALLOWED_CHARACTERS,
    CUSTOM_SHORT_ID_MAX_LENGTH,
)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            ErrorTextYacut.ID_NOT_FAUND,
            HTTPStatus.NOT_FOUND
        )

    return jsonify(url=url_map.original), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
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

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
