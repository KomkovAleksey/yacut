"""
Файл с view-функциями приложения 'yacut'.
"""
from flask import flash, render_template, redirect

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id, get_add_to_db


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Функция обрабатывающая запросы к главной странице.
    'GET' запрос отображает форму на экране.
    'POST' запрос создает короткую ссылку.
    """
    if URLForm().validate_on_submit():
        if URLForm().custom_id.data:
            if URLMap.query.filter_by(short=URLForm().custom_id.data).first() is not None:
                flash('"Предложенный вариант короткой ссылки уже существует."', 'error')

                return render_template('yacut.html', form=URLForm())

            get_add_to_db(URLForm().custom_id.data)
        short_id = get_unique_short_id(URLForm().original_link.data)
        get_add_to_db(short_id)

    return render_template('yacut.html', form=URLForm())


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    """Перенаправляет на оригинальную ссылку."""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
