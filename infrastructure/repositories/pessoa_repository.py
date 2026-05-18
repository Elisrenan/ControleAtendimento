"""Implementação SQLite do repositório de Pessoa.

Responsabilidade única: traduzir operações de domínio em SQL e
converter linhas do banco em instâncias de ``Pessoa``.
"""

import sqlite3

from domain.entities import Pessoa
from domain.repositories import IPessoaRepository
from infrastructure.database import get_connection


class SQLitePessoaRepository(IPessoaRepository):
    """Repositório de ``Pessoa`` baseado em SQLite.

    Recebe o caminho do banco via construtor, permitindo que testes
    passem ``":memory:"`` sem alterar nenhuma lógica de negócio.

    Args:
        db_path: Caminho para o arquivo ``.db`` ou ``":memory:"``.
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    # ------------------------------------------------------------------
    # Métodos auxiliares privados
    # ------------------------------------------------------------------

    def _row_to_pessoa(self, row: tuple) -> Pessoa:
        """Converte uma linha do banco (tupla) em uma instância de ``Pessoa``.

        Args:
            row: Tupla ``(id, nome, cpf, telefone)``.

        Returns:
            Instância de ``Pessoa`` com todos os campos preenchidos.
        """
        return Pessoa(id=row[0], nome=row[1], cpf=row[2], telefone=row[3])

    # ------------------------------------------------------------------
    # Implementação dos métodos abstratos
    # ------------------------------------------------------------------

    def salvar(self, pessoa: Pessoa) -> Pessoa:
        """Insere uma nova pessoa no banco e retorna a entidade com o ``id`` atribuído.

        Args:
            pessoa: Instância de ``Pessoa`` com ``id=None``.

        Returns:
            A mesma instância com o ``id`` gerado pelo banco.

        Raises:
            ValueError: Se o CPF já estiver cadastrado (``UNIQUE`` constraint).
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pessoas (nome, cpf, telefone) VALUES (?, ?, ?)",
                (pessoa.nome, pessoa.cpf, pessoa.telefone),
            )
            conn.commit()
            pessoa.id = cursor.lastrowid
            return pessoa
        except sqlite3.IntegrityError as erro:
            raise ValueError(f"CPF já cadastrado: {pessoa.cpf}") from erro
        finally:
            conn.close()

    def listar(self) -> list[Pessoa]:
        """Retorna todas as pessoas em ordem alfabética de nome.

        Returns:
            Lista (possivelmente vazia) de instâncias ``Pessoa``.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nome, cpf, telefone FROM pessoas ORDER BY nome"
            )
            return [self._row_to_pessoa(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def buscar_por_nome_ou_cpf(self, termo: str) -> list[Pessoa]:
        """Retorna pessoas cujo nome ou CPF contenha o termo informado.

        Args:
            termo: Substring para busca (case-insensitive no SQLite para ASCII).

        Returns:
            Lista de ``Pessoa`` correspondentes ao critério.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            padrao = f"%{termo}%"
            cursor.execute(
                """
                SELECT id, nome, cpf, telefone FROM pessoas
                WHERE nome LIKE ? OR cpf LIKE ?
                ORDER BY nome
                """,
                (padrao, padrao),
            )
            return [self._row_to_pessoa(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, pessoa_id: int) -> Pessoa | None:
        """Retorna a pessoa com o ``id`` informado, ou ``None`` se não existir.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            Instância de ``Pessoa`` ou ``None``.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nome, cpf, telefone FROM pessoas WHERE id = ?",
                (pessoa_id,),
            )
            row = cursor.fetchone()
            return self._row_to_pessoa(row) if row else None
        finally:
            conn.close()

    def excluir(self, pessoa_id: int) -> bool:
        """Remove a pessoa com o ``id`` informado do banco.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            ``True`` se removida com sucesso; ``False`` se não encontrada.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def tem_atendimentos_ativos(self, pessoa_id: int) -> bool:
        """Verifica se a pessoa possui atendimentos 'aberto' ou 'em andamento'.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            ``True`` se existir ao menos um atendimento ativo.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM atendimentos
                WHERE pessoa_id = ? AND status IN ('aberto', 'em andamento')
                """,
                (pessoa_id,),
            )
            total: int = cursor.fetchone()[0]
            return total > 0
        finally:
            conn.close()
