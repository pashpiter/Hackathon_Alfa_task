from http import HTTPStatus
from datetime import date

import pytest

from functional.utils.pk import get_next_pk
from functional.testdata.schemas import PlanStatus, TaskStatus


async def test_get_one_task(
        create_user,
        create_plan,
        create_task,
        tasks_get_one,
):
    user_1 = get_next_pk('user')
    await create_user(user_1, 'test_user_1', 'начальник 1', "000000", None)
    user_2 = get_next_pk('user')
    await create_user(user_2, 'test_user_2', 'сотрудник 1', "123123", user_1)
    user_3 = get_next_pk('user')
    await create_user(user_3, 'test_user_3', 'сотрудник 2', "456456", user_1)

    plan_1 = get_next_pk('plan')
    await create_plan(plan_1, str(plan_1), "CREATED", user_2)

    task_1 = get_next_pk('task')
    await create_task(
        task_1, str(task_1), str(task_1), "CREATED",
        plan_1, date.today()
    )

    # Запрос руководителя
    response = await tasks_get_one(task_1, "000000")
    assert response.status == HTTPStatus.OK
    assert response.body == {
        "name": str(task_1),
        "description": str(task_1),
        "status": "created",
        "created_at": date.today().strftime("%Y-%m-%d"),
        "expires_at": date.today().strftime("%Y-%m-%d"),
        "id": task_1,
        "comments": []
    }

    # Запрос сотрудника, для которого ИПР
    response = await tasks_get_one(task_1, "123123")
    assert response.status == HTTPStatus.OK
    assert response.body == {
        "name": str(task_1),
        "description": str(task_1),
        "status": "in_progress",
        "created_at": date.today().strftime("%Y-%m-%d"),
        "expires_at": date.today().strftime("%Y-%m-%d"),
        "id": task_1,
        "comments": []
    }

    # Запрос сотрудника не из ИПР
    response = await tasks_get_one(task_1, "456456")
    assert response.status == HTTPStatus.FORBIDDEN
