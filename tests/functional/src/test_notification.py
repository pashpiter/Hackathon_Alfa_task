from http import HTTPStatus

import pytest

from functional.utils.pk import get_next_pk
from functional.testdata.schemas import NotificationType, PlanStatus, TaskStatus


async def test_notification(
        create_user,
        create_plan,
        create_task,
        create_notification,
        notification_get_all,
        notification_make_read
):
    user_1 = get_next_pk('user')
    await create_user(user_1, 'test_user_1', 'начальник 1', user_1, None)

    plan_1 = get_next_pk('plan')
    await create_plan(plan_1, str(plan_1), PlanStatus.CREATED, user_1)

    task_1 = get_next_pk('task')
    await create_task(task_1, str(task_1), str(task_1), TaskStatus.CREATED, plan_1, None)

    notifications_amount = 3
    notifications_ids = []
    for _ in range(notifications_amount):
        notification_id = get_next_pk('notification')
        notifications_ids.append(notification_id)
        await create_notification(
            notification_id,
            user_1,
            NotificationType.COMMON,
            'заголовок',
            'содержимое',
            False,
            task_1
        )

    response = await notification_get_all(user_1, unread_only=True)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == notifications_amount

    response = await notification_make_read(user_1, notifications_ids)
    assert response.status == HTTPStatus.NO_CONTENT

    response = await notification_get_all(user_1, unread_only=True)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 0
