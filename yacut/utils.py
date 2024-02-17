"""
Файл дополнительных функций
"""
import random
import hashlib

from flask import flash, render_template, url_for

from . import db
from .models import URLMap
from .forms import URLForm
from .constants import SHORT_ID_LENGHT


def get_unique_short_id(long_url):
    """Функция формирования short_id."""
    generaited_short_id = random.choices(
        hashlib.md5(long_url.encode()).hexdigest(),
        k=SHORT_ID_LENGHT
    )
    short_id = ''.join(generaited_short_id)
    while URLMap.query.filter_by(short=short_id).first():
        short_id = ''.join(generaited_short_id)
    return short_id


def get_add_to_db(short_id):
    """
    Функция добавляющая оригинальную ссылку и short_id в базу данных.
    Выводит сообщение с укороченной ссылкой на главную страницу.
    """
    url_map = URLMap(
        original=URLForm().original_link.data,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()
    flash(url_for('redirect_short_url', short=url_map.short, _external=True), 'short_link')
    return render_template('yacut.html', form=URLForm())
