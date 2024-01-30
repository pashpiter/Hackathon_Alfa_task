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
        result = await session.execute(select(func.max(User.id)))
        max_id = result.scalar()
        if not max_id:
            return 0
        return max_id


def create_users_list(max_id):
    users = []
    i = 0
    for m in range(max_id + 1, max_id + 12):
        if supervisors_ids[i]:
            supervisor_id = supervisors_ids[i] + max_id
        else:
            supervisor_id = None
        users.append({
            "id": m,
            "full_name": full_names[i],
            "position": positions[i],
            "token": bearer_tokens[i],
            "supervisor_id": supervisor_id
        })
        i += 1
    return users


async def add_users(users_data: list[dict]):
    async with async_session() as session:
        new_users = [User(**usr_data) for usr_data in users_data]
        session.add_all(new_users)
        await session.commit()


async def main():
    max_user_id = await get_max_user_id_in_db()
    users = create_users_list(max_user_id)
    await add_users(users)


asyncio.run(main())
