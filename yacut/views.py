from flask import flash, render_template, redirect

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_url, get_add_url_to_db


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Обрабатывает 'GET' и 'POST' запросы к главной странице.
    'GET' запрос отображает форму на экране.
    'POST' запрос создает короткую ссылку.
    """
    if URLForm().validate_on_submit():
        if URLForm().custom_id.data:
            if URLMap.query.filter_by(short=URLForm().custom_id.data).first() is not None:
                flash('"Предложенный вариант короткой ссылки уже существует."', 'error')

                return render_template('yacut.html', form=URLForm())

            get_add_url_to_db(URLForm().custom_id.data)
        short_url = get_unique_short_url(URLForm().original_link.data)
        if URLMap.query.filter_by(short=short_url).first() is not None:
            short_url = get_unique_short_url(URLForm().original_link.data)
            get_add_url_to_db(short_url)

        get_add_url_to_db(short_url)

    return render_template('yacut.html', form=URLForm())


@app.route('/<string:short>', methods=['GET'])
def redirect_short_url(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
