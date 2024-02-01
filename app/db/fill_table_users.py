import asyncio
from sqlalchemy import select, func
from db.database import async_session_factory
from schemas.user import User

bearer_tokens = [
    "0987654321zyxwvutsrqponmlkjihgfedcba",
    "abcdefghijklmnopqrstuvwxyz1234567890",
    "zyxwvutsrqponmlkjihgfedcba0987654321",
    "1234567890abcdefghijklmnopqrstuvwxyz0987654321",
    "0987654321zyxwvutsrqponmlkjihgfedcba1234567890",
    "abcdefghijklmnopqrstuvwxyzzyxwvutsrqponmlkjihgfedcba",
    "zyxwvutsrqponmlkjihgfedcbaabcdefghijklmnopqrstuvwxyz",
    "1234567890zyxwvutsrqponmlkjihgfedcbaabcdefghijklmnopqrstuvwxyz",
    "1a2b3c4d5e6f7g8h9i0j",
    "1234567890abcdefghijklmnopqrstuvwxyz",
    "v1w2x3y4z5a6b7c8d9e0"
]

full_names = [
    "Иванов Иван Иванович",
    "Петров Петр Петрович",
    "Сидоров Сергей Сергеевич",
    "Кузнецов Константин Константинович",
    "Смирнов Михаил Михайлович",
    "Попов Павел Павлович",
    "Васильев Василий Васильевич",
    "Николаев Николай Николаевич",
    "Александров Александр Александрович",
    "Андреев Андрей Андреевич",
    "Егоров Егор Егорович",
]
positions = [
    "Финансовый аналитик",
    "Личный финансовый консультант",
    "Менеджер по отношениям с клиентами",
    "Бухгалтер",
    "Аудитор",
    "Менеджер отделения",
    "Специалист по кредитованию",
    "Сборщик долгов",
    "Кассир банка",
    "Начальник отделения",
    "Финансовый директор"
]
supervisors_ids = [10, 10, 10, 11, 11, 11, 11, 11, 11, None, None]
async_session = async_session_factory


async def get_max_user_id_in_db():
    async with async_session() as session:
        max_id = await session.execute(select(func.max(User.id)))
        value = max_id.scalar()
        return value if value else 0


def create_users_list(max_id):
    return [{
        "id": m,
        "full_name": fn,
        "position": p,
        "token": bt,
        "supervisor_id": si + max_id if si else None
    }
        for m, fn, p, bt, si in zip(
            range(max_id + 1, max_id + 12),
            full_names,
            positions,
            bearer_tokens,
            supervisors_ids
        )
    ]


async def add_users(users_data: list[dict]):
    async with async_session() as session:
        new_users = [User(**usr_data) for usr_data in users_data]
        session.add_all(new_users)
        await session.commit()


async def create_users():
    max_user_id = await get_max_user_id_in_db()
    users = create_users_list(max_user_id)
    await add_users(users)


async def delete_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()


async def delete_users(users: list[int] | int):
    if isinstance(users, list):  # Список id юзеров
        [await delete_user(user_id) for user_id in users]
    elif isinstance(users, int):  # Количество последних юзеров, которых удалять
        max_id = await get_max_user_id_in_db()
        [await delete_user(max_id - item) for item in range(users)]
    else:
        raise TypeError("Юзеры должны быть list[int] или int")


async def main():
    await create_users()


if __name__ == '__main__':
    asyncio.run(main())
