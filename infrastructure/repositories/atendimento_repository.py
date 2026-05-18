"""
Repositório de Atendimentos — acesso ao banco de dados SQLite.

Contém exclusivamente SQL relacionado à tabela 'atendimentos'.
Não há regras de negócio aqui — apenas operações de banco.
Recebe e retorna objetos Atendimento (domain/models.py).

Chamado por:
    services/atendimento_service.py → todas as funções

Chama:
    infrastructure/database.py → conectar()
    domain/models.py           → Atendimento
"""

from typing import List

from domain.models import Atendimento
from infrastructure.database import conectar

STATUS_PERMITIDOS = ["aberto", "em andamento", "finalizado"]


def inserir(atendimento: Atendimento) -> None:
    """Insere um novo atendimento no banco de dados.

    Args:
        atendimento: objeto Atendimento com pessoa_id, descricao e status preenchidos.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO atendimentos (pessoa_id, descricao, status) VALUES (?, ?, ?)",
        (atendimento.pessoa_id, atendimento.descricao, atendimento.status),
    )

    conexao.commit()
    conexao.close()


def listar_todos() -> List[Atendimento]:
    """Retorna todos os atendimentos com o nome da pessoa via JOIN.

    O campo pessoa_nome de cada objeto Atendimento é preenchido
    com o resultado do INNER JOIN na tabela 'pessoas'.

    Returns:
        Lista de objetos Atendimento ordenada por ID decrescente
        (mais recente primeiro).
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            atendimentos.id,
            atendimentos.pessoa_id,
            atendimentos.descricao,
            atendimentos.status,
            pessoas.nome
        FROM atendimentos
        INNER JOIN pessoas ON pessoas.id = atendimentos.pessoa_id
        ORDER BY atendimentos.id DESC
    """)

    linhas = cursor.fetchall()
    conexao.close()

    return [
        Atendimento(
            id=row[0],
            pessoa_id=row[1],
            descricao=row[2],
            status=row[3],
            pessoa_nome=row[4],
        )
        for row in linhas
    ]


def atualizar_status(atendimento_id: int, novo_status: str) -> bool:
    """Atualiza o status de um atendimento existente.

    Args:
        atendimento_id: ID do atendimento a atualizar.
        novo_status   : Novo valor do status (validação dos valores
                         possíveis é feita no service).

    Returns:
        True se o atendimento foi encontrado e atualizado, False caso contrário.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE atendimentos SET status = ? WHERE id = ?",
        (novo_status, atendimento_id),
    )

    atualizado = cursor.rowcount > 0
    conexao.commit()
    conexao.close()

    return atualizado
