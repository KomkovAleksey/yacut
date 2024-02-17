"""
Файл с классами форм приложения 'yacut'.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import (
    ErrorTextYacut,
    ALLOWED_CHARACTERS,
    CUSTOM_ID_MAX_LENGTH,
    ORIGINAL_MAX_LENGTH,
    ORIGINAL_MIN_LENGTH,
)


class URLForm(FlaskForm):
    """Класс формы для создания короткой ссылки."""

    original_link = URLField(
        'Длинная ссылка.',
        validators=[
            DataRequired(message=ErrorTextYacut.OBLIGATORY_FIELD),
            Length(ORIGINAL_MIN_LENGTH, ORIGINAL_MAX_LENGTH),
            URL(require_tld=True, message=ErrorTextYacut.WRONG_URL)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки.',
        validators=[
            Length(
                max=CUSTOM_ID_MAX_LENGTH,
                message=ErrorTextYacut.TOO_LONG_SHORT_LINK
            ),
            Optional(),
            Regexp(
                regex=ALLOWED_CHARACTERS,
                message=ErrorTextYacut.SHORT_LINK_INVALID_NAME
            ),
        ]
    )
    create = SubmitField('Создать')
