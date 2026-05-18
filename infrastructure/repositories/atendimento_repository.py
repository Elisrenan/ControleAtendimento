"""Implementação SQLite do repositório de Atendimento.

Responsabilidade única: traduzir operações de domínio em SQL e
converter linhas do banco em instâncias de ``Atendimento``.
O JOIN com a tabela ``pessoas`` é realizado aqui, eliminando
o acoplamento entre os serviços de aplicação.
"""

from domain.entities import Atendimento, StatusAtendimento
from domain.repositories import IAtendimentoRepository
from infrastructure.database import get_connection


class SQLiteAtendimentoRepository(IAtendimentoRepository):
    """Repositório de ``Atendimento`` baseado em SQLite.

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

    def _row_to_atendimento(self, row: tuple) -> Atendimento:
        """Converte uma linha do banco em instância de ``Atendimento``.

        Args:
            row: Tupla ``(id, pessoa_id, descricao, status, nome_pessoa)``
                resultante do JOIN com a tabela ``pessoas``.

        Returns:
            Instância de ``Atendimento`` com ``nome_pessoa`` preenchido.
        """
        return Atendimento(
            id=row[0],
            pessoa_id=row[1],
            descricao=row[2],
            status=StatusAtendimento(row[3]),
            nome_pessoa=row[4],
        )

    # ------------------------------------------------------------------
    # Implementação dos métodos abstratos
    # ------------------------------------------------------------------

    def salvar(self, atendimento: Atendimento) -> Atendimento:
        """Insere um novo atendimento no banco e retorna a entidade com ``id`` atribuído.

        O status inicial é sempre ``StatusAtendimento.ABERTO``, independente do
        valor passado na entidade (proteção de invariante de domínio).

        Args:
            atendimento: Instância de ``Atendimento`` com ``id=None``.

        Returns:
            A mesma instância com o ``id`` gerado pelo banco.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO atendimentos (pessoa_id, descricao, status)
                VALUES (?, ?, ?)
                """,
                (atendimento.pessoa_id, atendimento.descricao, StatusAtendimento.ABERTO.value),
            )
            conn.commit()
            atendimento.id = cursor.lastrowid
            atendimento.status = StatusAtendimento.ABERTO
            return atendimento
        finally:
            conn.close()

    def listar(self) -> list[Atendimento]:
        """Retorna todos os atendimentos com o nome da pessoa (via JOIN), em ordem decrescente de ID.

        Returns:
            Lista (possivelmente vazia) de instâncias ``Atendimento``.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    a.id,
                    a.pessoa_id,
                    a.descricao,
                    a.status,
                    p.nome
                FROM atendimentos a
                INNER JOIN pessoas p ON p.id = a.pessoa_id
                ORDER BY a.id DESC
                """
            )
            return [self._row_to_atendimento(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, atendimento_id: int) -> Atendimento | None:
        """Retorna o atendimento com o ``id`` informado, ou ``None`` se não existir.

        Args:
            atendimento_id: Identificador único do atendimento.

        Returns:
            Instância de ``Atendimento`` (com ``nome_pessoa``) ou ``None``.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    a.id,
                    a.pessoa_id,
                    a.descricao,
                    a.status,
                    p.nome
                FROM atendimentos a
                INNER JOIN pessoas p ON p.id = a.pessoa_id
                WHERE a.id = ?
                """,
                (atendimento_id,),
            )
            row = cursor.fetchone()
            return self._row_to_atendimento(row) if row else None
        finally:
            conn.close()

    def atualizar_status(self, atendimento_id: int, novo_status: str) -> bool:
        """Atualiza o campo ``status`` do atendimento indicado.

        Args:
            atendimento_id: Identificador único do atendimento.
            novo_status: Novo valor de status (deve ser membro de ``StatusAtendimento``).

        Returns:
            ``True`` se atualizado; ``False`` se não encontrado.
        """
        conn = get_connection(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE atendimentos SET status = ? WHERE id = ?",
                (novo_status, atendimento_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
