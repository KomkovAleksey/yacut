"""
Файл с view-функциями приложения 'yacut'.
"""
from http import HTTPStatus

from flask import flash, render_template, redirect, url_for, abort

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id, add_to_db, check_in_db
from .constants import ErrorText


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Функция обрабатывающая запросы к главной странице.
    'GET' запрос отображает форму на экране.
    'POST' запрос создает короткую ссылку.
    """
    if URLForm().validate_on_submit():
        if URLForm().custom_id.data:
            if check_in_db(URLMap, URLForm().custom_id.data) is not None:
                flash(ErrorText.SHORT_ID_DUPLICTE, 'error')

                return render_template('yacut.html', form=URLForm())

            add_to_db(
                URLMap,
                URLForm().custom_id.data,
                URLForm().original_link.data
            )
            flash(url_for(
                'redirect_short_url',
                short=URLForm().custom_id.data,
                _external=True), 'short_link'
            )

            return render_template('yacut.html', form=URLForm())

        add_to_db(
            URLMap,
            get_unique_short_id(URLForm().original_link.data),
            URLForm().original_link.data,
        )
        flash(url_for(
            'redirect_short_url',
            short=get_unique_short_id(URLForm().original_link.data),
            _external=True), 'short_link'
        )

        return render_template('yacut.html', form=URLForm())

    return render_template('yacut.html', form=URLForm())


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    """Перенаправляет на оригинальную ссылку."""
    url_map = check_in_db(URLMap, short)
    if url_map is None:
        return abort(HTTPStatus.NOT_FOUND)

    return redirect(url_map.original)
