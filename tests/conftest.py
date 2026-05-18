"""
Configurações globais do pytest.

Como rodar os testes:
    # Todos os testes
    python -m pytest tests/ -v

    # Apenas os testes de pessoa
    python -m pytest tests/test_pessoa_service.py -v

    # Apenas os testes de atendimento
    python -m pytest tests/test_atendimento_service.py -v

    # Com relatório de cobertura (requer pytest-cov)
    python -m pytest tests/ --cov=services -v

Estágio de isolamento:
    Cada teste recebe um banco SQLite vazio e temporário (tmp_path do pytest).
    O DB_PATH do módulo infrastructure.database é substituído via monkeypatch,
    garantindo que os testes nunca toquem no banco de produção.
"""

import pytest

import infrastructure.database as db_module


@pytest.fixture(autouse=True)
def banco_temporario(tmp_path, monkeypatch):
    """Cada teste recebe um banco SQLite isolado em diretório temporário."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    db_module.criar_tabelas()
    yield
