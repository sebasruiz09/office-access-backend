import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from models import db as _db, Visitante


@pytest.fixture(scope='session')
def test_app():
    app = create_app(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ECHO': False,
        }
    )

    ctx = app.app_context()
    ctx.push()

    yield app

    # Limpieza después de las pruebas
    ctx.pop()


@pytest.fixture(scope='session')
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture(scope='session')
def init_database(test_app):
    _db.create_all()

    # Insertar datos de prueba
    visitante1 = Visitante(
        numero_identificacion='12345678',
        tipo_identificacion='DNI',
        nombres='Juan',
        apellidos='Pérez',
        tipo_visitante='Personal',
    )

    visitante2 = Visitante(
        numero_identificacion='87654321',
        tipo_identificacion='RUC',
        nombres='Empresa',
        apellidos='S.A.',
        tipo_visitante='Empresarial',
        empresa_representa='Empresa S.A.',
    )

    _db.session.add_all([visitante1, visitante2])
    _db.session.commit()

    yield _db

    _db.session.remove()
    _db.drop_all()


@pytest.fixture
def auth_headers():
    return {
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json',
    }
