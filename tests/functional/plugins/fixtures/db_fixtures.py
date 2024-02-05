import asyncpg
import pytest_asyncio
from functional.settings import test_settings
from functional.testdata.schemas import PK_TYPE, USER_PK_TYPE, NotificationType, PlanStatus
from datetime import date


@pytest_asyncio.fixture(scope="session")
async def db_connection():
    postgres = test_settings.postgres
    conn = await asyncpg.connect(
        host=postgres.host,
        port=postgres.port,
        user=postgres.user,
        password=postgres.password,
        database=postgres.db_name,
        server_settings={'search_path': postgres.search_path}
    )
    yield conn
    conn.close()


@pytest_asyncio.fixture(scope='session')
async def make_db_request(db_connection):
    async def inner(method: str, sql: str):
        allowed_methods = {
            'EXECUTE': 'EXECUTE',
            'FETCHALL': 'FETCH',
            'FETCHONE': 'FETCHROW'
        }
        if method not in allowed_methods:
            raise ValueError(f'Method should be one of the allowed: {allowed_methods.keys()}')
        if method == 'EXECUTE':
            sql = sql.replace('None', 'NULL')
        caller = getattr(db_connection, allowed_methods[method].lower())
        return await caller(sql)
    return inner


@pytest_asyncio.fixture(scope='session')
async def clear_data(make_db_request):
    async def inner():
        sql = """
        DELETE FROM "comment" CASCADE;
        DELETE FROM "unreadcomment" CASCADE;
        DELETE FROM "notification" CASCADE;
        DELETE FROM "task" CASCADE;
        DELETE FROM "plan" CASCADE;
        DELETE FROM "user" CASCADE;
        """
        await make_db_request('EXECUTE', sql)
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def db_init(
        clear_data
):
    await clear_data()
    yield
    # await clear_data()


@pytest_asyncio.fixture(scope='session')
async def create_user(make_db_request):
    async def inner(
            id: USER_PK_TYPE,
            full_name: str,
            position: str,
            token: str,
            supervisor_id: USER_PK_TYPE | None
    ):
        sql = f"""
        INSERT INTO "user"
        (id, full_name, position, token, supervisor_id)
        VALUES ({id}, '{full_name}', '{position}', '{token}', {supervisor_id});
        """
        await make_db_request('EXECUTE', sql)

    return inner


@pytest_asyncio.fixture(scope='session')
async def create_plan(make_db_request):
    async def inner(
            id: PK_TYPE,
            aim_description: str,
            status: PlanStatus,
            employee_id: USER_PK_TYPE
    ):
        sql = f"""
        INSERT INTO "plan"
        (id, aim_description, status, employee_id)
        VALUES ({id}, '{aim_description}', '{status}', '{employee_id}');
        """
        await make_db_request('EXECUTE', sql)

    return inner


@pytest_asyncio.fixture(scope='session')
async def create_task(make_db_request):
    async def inner(
            id: PK_TYPE,
            name: str,
            description: str,
            status: PlanStatus,
            plan_id: PK_TYPE,
            expires_at: date | None
    ):
        if expires_at:
            values = f"""VALUES ('{id}', '{name}', '{description}', '{status}', '{plan_id}', '{expires_at}');"""
        else:
            values = f"""VALUES ('{id}', '{name}', '{description}', '{status}', '{plan_id}', {expires_at});"""
        sql = f"""
        INSERT INTO "task"
        (id, name, description, status, plan_id, expires_at)
        {values}
        """
        await make_db_request('EXECUTE', sql)

    return inner


@pytest_asyncio.fixture(scope='session')
async def create_notification(make_db_request):
    async def inner(
            id: PK_TYPE,
            recipient_id: USER_PK_TYPE,
            type: NotificationType,
            header: str,
            content: str,
            is_read: bool,
            task_id: PK_TYPE,
    ):
        sql = f"""
        INSERT INTO "notification"
        (id, recipient_id, type, header, content, is_read, task_id)
        VALUES ({id}, '{recipient_id}', '{type}', '{header}', '{content}', {is_read}, {task_id});
        """
        await make_db_request('EXECUTE', sql)

    return inner
