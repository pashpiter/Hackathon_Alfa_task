from functional.testdata.schemas import USER_PK_TYPE, PK_TYPE

CURRENT_PK = {
    'user': 1000,
    'plan': 2000,
    'task': 3000,
    'notification': 4000,
    'comment': 5000
}


def get_next_pk(table: str) -> USER_PK_TYPE | PK_TYPE:
    CURRENT_PK[table] += 1
    return CURRENT_PK[table]
