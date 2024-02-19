"""
Файл функций и методов обработки запросов и отправки ответов через API.
"""
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import validate_data, add_to_db
from .constants import ErrorTextYacut


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
    validate_data(request.get_json())
    add_to_db(
        URLMap,
        request.get_json().get('custom_id'),
        request.get_json().get('url'),
    )

    return jsonify(URLMap(
        original = request.get_json().get('url'),
        short = request.get_json().get('custom_id')).to_dict()
    ), HTTPStatus.CREATED
