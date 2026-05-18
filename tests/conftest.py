import pytest
import infrastructure.database as db_module


@pytest.fixture(autouse=True)
def banco_temporario(tmp_path, monkeypatch):
    """Cada teste recebe um banco SQLite isolado em diretório temporário."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    db_module.criar_tabelas()
    yield
