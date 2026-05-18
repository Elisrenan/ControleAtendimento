import sqlite3
from typing import List, Optional

from infrastructure.database import conectar
from domain.models import Pessoa


def inserir(pessoa: Pessoa) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO pessoas (nome, cpf, telefone) VALUES (?, ?, ?)",
        (pessoa.nome, pessoa.cpf, pessoa.telefone),
    )

    conexao.commit()
    conexao.close()


def listar_todos() -> List[Pessoa]:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, cpf, telefone FROM pessoas ORDER BY nome")

    linhas = cursor.fetchall()
    conexao.close()

    return [Pessoa(id=l[0], nome=l[1], cpf=l[2], telefone=l[3]) for l in linhas]


def buscar_por_nome_ou_cpf(termo: str) -> List[Pessoa]:
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
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))

    removido = cursor.rowcount > 0
    conexao.commit()
    conexao.close()

    return removido
