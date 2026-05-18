"""
Camada de Infraestrutura — conexão com o banco de dados SQLite.

Fornece as funções de conexão e criação das tabelas para toda a aplicação.
O caminho do arquivo .db é calculado automaticamente a partir deste arquivo,
nunca dependendo do diretório de trabalho corrente.

Chamado por:
    infrastructure/repositories/pessoa_repository.py      → conectar()
    infrastructure/repositories/atendimento_repository.py → conectar()
    main.py                                               → criar_tabelas()
    ui/cli.py                                             → criar_tabelas()
    ui/gui.py                                             → criar_tabelas()
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "controle_atendimentos.db"


def conectar():
    """Abre e retorna uma conexão com o banco SQLite.

    O arquivo .db é criado automaticamente se não existir.
    Responsabilidade de fechar a conexão ( conexao.close() ) é do chamador.

    Returns:
        sqlite3.Connection: conexão ativa com o banco.
    """
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    """Cria as tabelas 'pessoas' e 'atendimentos' se ainda não existirem.

    Usa CREATE TABLE IF NOT EXISTS, por isso é seguro chamar múltiplas vezes.
    Chamado automaticamente no início da aplicação por main.py, cli.py e gui.py.
    """
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
