import os

from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    # En el servidor y en el pipeline se usa DATABASE_URL.
    # En tu PC sigue funcionando con las variables MYSQL_* del .env.
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
        f"{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
