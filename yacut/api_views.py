from flask import jsonify, request
import re

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_url


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify(url=url_map.original), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage("\"url\" является обязательным полем!")
    custom_id = data.get('custom_id')
    if not custom_id or custom_id == '':
        custom_id = get_unique_short_url(data.get('url'))
        data['custom_id'] = custom_id
    else:
        if len(custom_id) > 16 or not re.match(r'^[A-Za-z0-9]+$', custom_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
        if URLMap.query.filter_by(short=data.get('custom_id')).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
            )

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), 201