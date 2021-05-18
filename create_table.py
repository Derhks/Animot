from settings import db


def create_table() -> None:
    db.create_all()
    db.close_all_sessions()


if __name__ == '__main__':
    create_table()
