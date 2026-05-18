"""Gerenciamento de conexão e inicialização do banco de dados SQLite.

Este módulo é o único ponto da aplicação que conhece os detalhes de
conexão com o SQLite. Toda outra camada recebe a conexão como parâmetro
ou usa os repositórios concretos — nunca importa ``sqlite3`` diretamente.
"""

import sqlite3
from sqlite3 import Connection


def get_connection(db_path: str) -> Connection:
    """Cria e retorna uma conexão SQLite com chaves estrangeiras ativas.

    Args:
        db_path: Caminho completo para o arquivo ``.db`` (use ``":memory:"``
            para banco em memória nos testes).

    Returns:
        Conexão SQLite pronta para uso.

    Example:
        >>> conn = get_connection(":memory:")
        >>> conn.execute("SELECT 1").fetchone()
        (1,)
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str) -> None:
    """Cria as tabelas do banco de dados caso ainda não existam.

    Idempotente: pode ser chamada múltiplas vezes sem efeitos colaterais.
    Deve ser invocada uma única vez na inicialização da aplicação.

    Args:
        db_path: Caminho completo para o arquivo ``.db`` (use ``":memory:"``
            para banco em memória nos testes).

    Example:
        >>> init_db(":memory:")  # não levanta exceção
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      TEXT    NOT NULL,
                cpf       TEXT    NOT NULL UNIQUE,
                telefone  TEXT    NOT NULL DEFAULT ''
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atendimentos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoa_id  INTEGER NOT NULL,
                descricao  TEXT    NOT NULL,
                status     TEXT    NOT NULL DEFAULT 'aberto',
                FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
            )
        """)

        conn.commit()
    finally:
        conn.close()
