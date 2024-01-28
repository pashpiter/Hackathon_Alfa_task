import asyncio
from db.database import async_engine, async_session_factory
from schemas.user import User

bearer_tokens = [
    "Bearer 0987654321zyxwvutsrqponmlkjihgfedcba",
    "Bearer abcdefghijklmnopqrstuvwxyz1234567890",
    "Bearer zyxwvutsrqponmlkjihgfedcba0987654321",
    "Bearer 1234567890abcdefghijklmnopqrstuvwxyz0987654321",
    "Bearer 0987654321zyxwvutsrqponmlkjihgfedcba1234567890",
    "Bearer abcdefghijklmnopqrstuvwxyzzyxwvutsrqponmlkjihgfedcba",
    "Bearer zyxwvutsrqponmlkjihgfedcbaabcdefghijklmnopqrstuvwxyz",
    "Bearer 1234567890zyxwvutsrqponmlkjihgfedcbaabcdefghijklmnopqrstuvwxyz",
    "Bearer 1a2b3c4d5e6f7g8h9i0j",
    "Bearer 1234567890abcdefghijklmnopqrstuvwxyz",
    "Bearer v1w2x3y4z5a6b7c8d9e0"
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

all_users = [{
    "id": i + 1,
    "full_name": full_names[i],
    "position": positions[i],
    "token": bearer_tokens[i],
    "supervisor_id": supervisors_ids[i]
}
    for i in range(0, 11)
]

engine = async_engine
async_session = async_session_factory


async def add_user(usr_data: dict):
    async with async_session() as session:
        new_user = User(**usr_data)
        session.add(new_user)
        await session.commit()


async def main():
    for item in all_users:
        await add_user(item)


asyncio.run(main())
