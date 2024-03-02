from .exceptions import ShortIdDuplicateError
from .utils import (
    generaite_unique_short_id,
    validate_custom_id,
    get_short_from_db,
    save_original_and_short_id_in_db,
)


def creating_custom_id(custom_id, original):
    """
    Проверяет наличие custom_id
    Валидирует custom_id.
    Проверяет наличие custom_id в базе данных.
    Добавляет original и custom_id в базу данных.
    """
    if not custom_id or custom_id == '':
        custom_id = generaite_unique_short_id(original)
    else:
        if validate_custom_id(custom_id):
            raise ValueError()
        if get_short_from_db(custom_id) is not None:
            raise ShortIdDuplicateError()

    save_original_and_short_id_in_db(
        custom_id,
        original,
    )

    return custom_id
