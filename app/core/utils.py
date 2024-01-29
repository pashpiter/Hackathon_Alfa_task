from datetime import date
from pathlib import Path


def create_mock_file(
        directory: Path,
        filename: str
) -> str:
    """Создаёт файл в директории directory с именем filename. Если такой файл
    уже существует, добавляет к имени цифру в скобках до тех пор, пока не
    найдётся свободное имя."""
    directory.mkdir(exist_ok=True)
    new_filename = filename
    i = 1
    while True:
        try:
            Path.touch(directory / new_filename, exist_ok=False)
            break
        except FileExistsError:
            new_filename = f'{filename} ({i})'
            i += 1

    return new_filename


def date_today() -> date:
    return date.today()
