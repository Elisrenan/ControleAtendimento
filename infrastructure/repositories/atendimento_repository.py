from typing import List

from infrastructure.database import conectar
from domain.models import Atendimento


STATUS_PERMITIDOS = ["aberto", "em andamento", "finalizado"]


def inserir(atendimento: Atendimento) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO atendimentos (pessoa_id, descricao, status) VALUES (?, ?, ?)",
        (atendimento.pessoa_id, atendimento.descricao, atendimento.status),
    )

    conexao.commit()
    conexao.close()


def listar_todos() -> List[Atendimento]:
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
        Atendimento(id=l[0], pessoa_id=l[1], descricao=l[2], status=l[3], pessoa_nome=l[4])
        for l in linhas
    ]


def atualizar_status(atendimento_id: int, novo_status: str) -> bool:
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
