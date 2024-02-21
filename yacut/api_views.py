"""
Файл функций и методов обработки запросов и отправки ответов через API.
"""
from http import HTTPStatus
from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .constants import ErrorText
from .utils import validate_custom_id, add_to_db, check_in_db, get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    if check_in_db(URLMap, short_id) is None:
        raise InvalidAPIUsage(
            ErrorText.ID_NOT_FAUND,
            HTTPStatus.NOT_FOUND
        )

    return jsonify(url=check_in_db(URLMap, short_id).original), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(ErrorText.REQUEST_BODY_MISSING)
    if not data.get('url'):
        raise InvalidAPIUsage(ErrorText.URL_MISSING)
    custom_id = data.get('custom_id')
    if not custom_id or custom_id == '':
        data['custom_id'] = get_unique_short_id(data.get('url'))
        custom_id = data['custom_id']
    else:
        if validate_custom_id(custom_id):
            raise InvalidAPIUsage(
                ErrorText.SHORT_LINK_INVALID_NAME,
                HTTPStatus.BAD_REQUEST
            )
    if check_in_db(URLMap, data.get('custom_id')) is not None:
        raise InvalidAPIUsage(ErrorText.SHORT_ID_DUPLICTE)

    add_to_db(
        URLMap,
        custom_id,
        data.get('url'),
    )

    return jsonify(URLMap(
        original=data.get('url'),
        short=custom_id).to_dict()
    ), HTTPStatus.CREATED
