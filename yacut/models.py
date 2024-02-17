from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Модель для работы с ссылками."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Сериализатор."""
        return dict(
            url=self.original,
            short_link='http://localhost/' + self.short,
        )

    def from_dict(self, data):
        """Десериализатор."""
        API_FIELDS = {
            'url': 'original',
            'custom_id': 'short',
        }
        for field in API_FIELDS:
            if field in data:
                setattr(self, API_FIELDS[field], data[field])
