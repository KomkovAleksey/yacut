"""
Файл функций и методов обработки запросов и отправки ответов через API.
"""
from http import HTTPStatus
from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .exceptions import ShortIdDuplicateError
from .constants import ErrorText
from .utils import get_short_from_db, check_custom_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    url_map = get_short_from_db(URLMap, short_id)
    if url_map is None:
        raise InvalidAPIUsage(
            ErrorText.ID_NOT_FAUND,
            HTTPStatus.NOT_FOUND
        )

    return jsonify(url=url_map.original), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(ErrorText.REQUEST_BODY_MISSING)
    if not data.get('url'):
        raise InvalidAPIUsage(ErrorText.URL_MISSING)
    original = data.get('url')
    try:
        custom_id = check_custom_id(URLMap, data.get('custom_id'), original)
    except ValueError:
        raise InvalidAPIUsage(
            ErrorText.SHORT_LINK_INVALID_NAME
        )
    except ShortIdDuplicateError:
        raise InvalidAPIUsage(ErrorText.SHORT_ID_DUPLICATE)

    return jsonify(URLMap(
        original=original,
        short=custom_id).to_dict()
    ), HTTPStatus.CREATED
