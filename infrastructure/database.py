import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "controle_atendimentos.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
        )
    """)

    conexao.commit()
    conexao.close()
