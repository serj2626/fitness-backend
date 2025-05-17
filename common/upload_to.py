from datetime import datetime
import os
from uuid import uuid4


def upload_to_folder(folder_name):
    """
    Возвращает функцию, которую можно использовать как `upload_to` в ImageField/FileField.
    Сохраняет файл в указанную папку с уникальным именем.
    """

    def wrapper(instance, filename):
        # Генерация уникального имени: uuid + оригинальное расширение
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"

        # Например: "uploads/products/2025/05/filename.jpg"
        return os.path.join(folder_name, datetime.now().strftime("%Y/%m"), filename)

    return wrapper
