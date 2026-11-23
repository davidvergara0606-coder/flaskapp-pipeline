import os

import pytest
from sqlalchemy import inspect, text

from app import create_app
from app.database.database import db

pytestmark = pytest.mark.skipif(
    not os.getenv("DATABASE_URL", "").startswith("mysql"),
    reason="requiere MySQL real en DATABASE_URL",
)


@pytest.fixture()
def app_mysql():
    app = create_app()
    app.config.update(TESTING=True)
    return app


def test_health_responde_200(app_mysql):
    respuesta = app_mysql.test_client().get("/health")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"status": "ok"}


def test_conexion_mysql_y_migraciones_aplicadas(app_mysql):
    with app_mysql.app_context():
        assert db.session.execute(text("SELECT 1")).scalar() == 1
        tablas = inspect(db.engine).get_table_names()
        assert "alembic_version" in tablas
