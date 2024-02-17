"""
Файл дополнительных функций
"""
import random
import hashlib

from flask import flash, render_template, url_for

from . import db
from .models import URLMap
from .forms import URLForm


def get_unique_short_url(long_url):
    """Функция формирования короткой ссылки."""
    short_url = random.choices(
        hashlib.md5(long_url.encode()).hexdigest(),
        k=6
    )
    return ''.join(short_url)


def get_add_url_to_db(short_url):
    """
    Функция добавляющая оригинальную и укороченную ссылку в базу данных.
    Выводит сообщение с укороченной ссылкой на главную страницу.
    """
    url_map = URLMap(
        original=URLForm().original_link.data,
        short=short_url,
    )
    db.session.add(url_map)
    db.session.commit()
    flash(url_for('redirect_short_url', short=url_map.short, _external=True), 'short_link')
    return render_template('yacut.html', form=URLForm())
