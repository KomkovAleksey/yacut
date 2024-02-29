"""
Файл с view-функциями приложения 'yacut'.
"""
from http import HTTPStatus

from flask import flash, render_template, redirect, url_for, abort

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import get_short_from_db, check_custom_id
from .constants import ErrorText
from .exceptions import ShortIdDuplicateError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Функция обрабатывающая запросы к главной странице.
    'GET' запрос отображает форму на экране.
    'POST' запрос создает короткую ссылку.
    """
    if URLForm().validate_on_submit():
        try:
            custom_id = check_custom_id(URLMap, URLForm().custom_id.data, URLForm().original_link.data)
        except ShortIdDuplicateError:
            flash(ErrorText.SHORT_ID_DUPLICATE, 'error')

            return render_template('yacut.html', form=URLForm())

        flash(url_for(
            'redirect_short_url',
            short=custom_id,
            _external=True), 'short_link'
        )

        return render_template('yacut.html', form=URLForm())

    return render_template('yacut.html', form=URLForm())


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    """Перенаправляет на оригинальную ссылку."""
    url_map = get_short_from_db(URLMap, short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)

    return redirect(url_map.original)
