from datetime import date
from pathlib import Path


class File:
    name: str
    extension: str = ''
    _version: int = 0

    EMPTY_NAME_ERROR = 'Имя не может быть пустым'

    def __init__(self, filename: str):
        if not filename:
            raise ValueError(self.EMPTY_NAME_ERROR)

        _file = filename.rsplit('.', 1)
        self.name = _file[0]
        if len(_file) == 2:
            self.extension = _file[1]

    def __str__(self):
        return '{name}{version}{extension}'.format(
            name=self.name,
            version=f' ({self._version})' if self._version else '',
            extension=f'.{self.extension}' if self.extension else ''
        )

    def increase_version(self):
        self._version += 1


def create_mock_file(
        directory: Path,
        filename: str
) -> str:
    """Создаёт файл в директории directory с именем filename. Если такой файл
    уже существует, добавляет к имени цифру в скобках до тех пор, пока не
    найдётся свободное имя."""
    directory.mkdir(exist_ok=True)
    file = File(filename)
    while True:
        try:
            Path.touch(directory / str(file), exist_ok=False)
            break
        except FileExistsError:
            file.increase_version()

    return str(file)


def date_today() -> date:
    return date.today()
