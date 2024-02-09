from pathlib import Path
from typing import Iterable, Type

from schemas.plan import Plan, PlanStatus
from schemas.task import Task, TaskStatus


class File:
    name: str
    extension: str = ""
    _version: int = 0

    EMPTY_NAME_ERROR = "Имя файла не может быть пустым"

    def __init__(self, filename: str):
        if not filename:
            raise ValueError(self.EMPTY_NAME_ERROR)

        _file = filename.rsplit(".", 1)
        self.name = _file[0]
        if len(_file) == 2:
            self.extension = _file[1]

    def __str__(self):
        return "{name}{version}{extension}".format(
            name=self.name,
            version=f" ({self._version})" if self._version else "",
            extension=f".{self.extension}" if self.extension else ""
        )

    def increase_version(self):
        self._version += 1


def create_empty_file(
        directory: Path,
        filename: str
) -> str:
    """Создаёт пустой файл в директории directory с именем filename. Если
    такой файл уже существует, добавляет к имени цифру в скобках до тех пор,
    пока не найдётся свободное имя."""
    directory.mkdir(exist_ok=True)
    file = File(filename)  # noqa VNE002
    while True:
        try:
            Path.touch(directory / str(file), exist_ok=False)
            break
        except FileExistsError:
            file.increase_version()

    return str(file)


def get_status_statistic(
        elements: Iterable[Plan | Task],
        statuses: Type[PlanStatus | TaskStatus]
):
    el_amount = 0
    el_statuses = {status: 0 for status in statuses}
    for element in elements:
        el_amount += 1
        el_statuses[element.status] += 1

    el_done_rate = el_statuses[statuses.DONE] / el_amount * 100
    return {
        "total": el_amount,
        "complete_percentage": f'{el_done_rate:.0f}',
        "statuses": el_statuses,
    }
