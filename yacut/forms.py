"""
Файл с классами форм приложения 'yacut'.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка.',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message='Проверьте вводимый адрес ссылки.')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки.',
        validators=[
            Length(1, 16, message='Длинна ссылки болше 16 символов.'),
            Optional(),
            Regexp(
                regex=r'^[A-Za-z0-9]+$',
                message='Недопустимое имя короткой ссылки.'
            ),
        ]
    )
    create = SubmitField('Создать')
