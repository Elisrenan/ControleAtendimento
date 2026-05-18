"""
Repositório de Pessoas — acesso ao banco de dados SQLite.

Contém exclusivamente SQL relacionado à tabela 'pessoas'.
Não há regras de negócio aqui — apenas operações de banco.
Recebe e retorna objetos Pessoa (domain/models.py).

Chamado por:
    services/pessoa_service.py      → todas as funções
    services/atendimento_service.py → buscar_por_id()

Chama:
    infrastructure/database.py → conectar()
    domain/models.py           → Pessoa
"""
import sqlite3
from typing import List, Optional

from infrastructure.database import conectar
from domain.models import Pessoa


def inserir(pessoa: Pessoa) -> None:
    """Insere uma nova pessoa no banco de dados.

    Args:
        pessoa: objeto Pessoa com nome, cpf e telefone preenchidos.

    Raises:
        sqlite3.IntegrityError: se o CPF já existir (UNIQUE constraint).
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO pessoas (nome, cpf, telefone) VALUES (?, ?, ?)",
        (pessoa.nome, pessoa.cpf, pessoa.telefone),
    )

    conexao.commit()
    conexao.close()


def listar_todos() -> List[Pessoa]:
    """Retorna todas as pessoas ordenadas por nome.

    Returns:
        Lista de objetos Pessoa. Vazia se não houver registros.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, cpf, telefone FROM pessoas ORDER BY nome")
    linhas = cursor.fetchall()
    conexao.close()

    return [Pessoa(id=l[0], nome=l[1], cpf=l[2], telefone=l[3]) for l in linhas]


def buscar_por_nome_ou_cpf(termo: str) -> List[Pessoa]:
    """Busca pessoas pelo nome ou CPF usando correspondência parcial (LIKE).

    Args:
        termo: texto a buscar. Pode ser parte do nome ou parte do CPF.

    Returns:
        Lista de objetos Pessoa correspondentes, ordenada por nome.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, cpf, telefone FROM pessoas WHERE nome LIKE ? OR cpf LIKE ? ORDER BY nome",
        (f"%{termo}%", f"%{termo}%"),
    )

    linhas = cursor.fetchall()
    conexao.close()

    return [Pessoa(id=l[0], nome=l[1], cpf=l[2], telefone=l[3]) for l in linhas]


def buscar_por_id(pessoa_id: int) -> Optional[Pessoa]:
    """Busca uma pessoa pelo seu ID.

    Args:
        pessoa_id: chave primária da pessoa.

    Returns:
        Objeto Pessoa se encontrado, None caso contrário.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, cpf, telefone FROM pessoas WHERE id = ?",
        (pessoa_id,),
    )

    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return None

    return Pessoa(id=linha[0], nome=linha[1], cpf=linha[2], telefone=linha[3])


def contar_atendimentos_ativos(pessoa_id: int) -> int:
    """Conta quantos atendimentos com status 'aberto' ou 'em andamento' a pessoa possui.

    Usado pelo service antes de excluir uma pessoa, para garantir a regra de negócio.

    Args:
        pessoa_id: ID da pessoa a verificar.

    Returns:
        Quantidade de atendimentos ativos (inteiro >= 0).
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM atendimentos WHERE pessoa_id = ? AND status IN ('aberto', 'em andamento')",
        (pessoa_id,),
    )

    total = cursor.fetchone()[0]
    conexao.close()

    return total


def excluir(pessoa_id: int) -> bool:
    """Remove uma pessoa do banco pelo ID.

    Args:
        pessoa_id: ID da pessoa a excluir.

    Returns:
        True se o registro foi removido, False se não foi encontrado.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))
    removido = cursor.rowcount > 0

    conexao.commit()
    conexao.close()

    return removido
