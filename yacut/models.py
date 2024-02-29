"""
Файл с моделями приложения 'yacut'.
"""
from datetime import datetime

from .import db
from .constants import (
    LOCALHOST,
    ORIGINAL_MAX_LENGTH,
    CUSTOM_SHORT_ID_MAX_LENGTH,
)


class URLMap(db.Model):
    """Модель для работы с ссылками."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(CUSTOM_SHORT_ID_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Сериализатор."""
        return dict(
            url=self.original,
            short_link=LOCALHOST + self.short,
        )
