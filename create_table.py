from utils import postgres_execute


def create_tables() -> None:

    command = """
        CREATE TABLE IF NOT EXISTS animes_viewed (
        id SERIAL PRIMARY KEY,
        canonical_title TEXT UNIQUE NOT NULL,
        synopsis TEXT NOT NULL,
        rating VARCHAR ( 10 ) UNIQUE NOT NULL,
        image VARCHAR ( 255 ) UNIQUE NOT NULL,
        published_at DATE NOT NULL
    );
    """

    postgres_execute(command)


if __name__ == '__main__':
    create_tables()
