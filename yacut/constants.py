"""
Константы.
"""
ALLOWED_CHARACTERS = r'^[A-Za-z0-9]+$'
LOCALHOST = 'http://localhost/'
CUSTOM_SHORT_ID_MAX_LENGTH = 16
ORIGINAL_MAX_LENGTH = 256
ORIGINAL_MIN_LENGTH = 1
GENERAITED_SHORT_ID_LENGHT = 6


class ErrorText():
    """Текст ошибок."""

    SHORT_ID_DUPLICTE = 'Предложенный вариант короткой ссылки уже существует.'
    ID_NOT_FAUND = 'Указанный id не найден'
    REQUEST_BODY_MISSING = 'Отсутствует тело запроса'
    URL_MISSING = '\"url\" является обязательным полем!'
    SHORT_LINK_INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
    TOO_LONG_SHORT_LINK = 'Длинна ссылки болше 16 символов.'
    WRONG_URL = 'Проверьте вводимый адрес ссылки.'
    OBLIGATORY_FIELD = 'Обязательное поле'
