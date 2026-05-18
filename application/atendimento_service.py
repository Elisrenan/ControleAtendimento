"""Serviço de aplicação para a entidade Atendimento.

Orquestra as regras de negócio de atendimentos delegando a persistência
ao repositório injetado. Não depende do ``PessoaService`` — a verificação
de existência da pessoa e o JOIN são responsabilidade do repositório.
"""

from config import STATUS_PERMITIDOS
from domain.entities import Atendimento
from domain.repositories import IAtendimentoRepository, IPessoaRepository


class AtendimentoService:
    """Casos de uso relacionados ao registro e atualização de atendimentos.

    Args:
        atendimento_repo: Implementação de ``IAtendimentoRepository``.
        pessoa_repo: Implementação de ``IPessoaRepository``, usada apenas para
            verificar se a pessoa existe antes de criar o atendimento.

    Example:
        >>> from tests.fakes import FakeAtendimentoRepository, FakePessoaRepository
        >>> service = AtendimentoService(FakeAtendimentoRepository(), FakePessoaRepository())
    """

    def __init__(
        self,
        atendimento_repo: IAtendimentoRepository,
        pessoa_repo: IPessoaRepository,
    ) -> None:
        self._atendimento_repo = atendimento_repo
        self._pessoa_repo = pessoa_repo

    # ------------------------------------------------------------------
    # Casos de uso
    # ------------------------------------------------------------------

    def registrar(self, pessoa_id: int, descricao: str) -> tuple[bool, str]:
        """Valida os dados e registra um novo atendimento com status ``'aberto'``.

        Regras de negócio:
        - A pessoa referenciada deve existir.
        - A descrição não pode ser vazia.

        Args:
            pessoa_id: Identificador único da pessoa a ser atendida.
            descricao: Descrição do motivo ou serviço do atendimento.

        Returns:
            Tupla ``(sucesso, mensagem)`` onde ``sucesso`` é ``True`` em caso
            de registro bem-sucedido.
        """
        if self._pessoa_repo.buscar_por_id(pessoa_id) is None:
            return False, "Pessoa não encontrada."

        if not descricao.strip():
            return False, "A descrição do atendimento é obrigatória."

        try:
            self._atendimento_repo.salvar(
                Atendimento(pessoa_id=pessoa_id, descricao=descricao)
            )
            return True, "Atendimento registrado com sucesso."
        except Exception as erro:  # noqa: BLE001
            return False, f"Erro ao registrar atendimento: {erro}"

    def listar(self) -> list[Atendimento]:
        """Retorna todos os atendimentos com o nome da pessoa, em ordem decrescente de ID.

        Returns:
            Lista de instâncias ``Atendimento`` com ``nome_pessoa`` preenchido.
        """
        return self._atendimento_repo.listar()

    def atualizar_status(self, atendimento_id: int, novo_status: str) -> tuple[bool, str]:
        """Atualiza o status de um atendimento existente.

        Regras de negócio:
        - ``novo_status`` deve ser um dos valores em ``STATUS_PERMITIDOS``.
        - O atendimento deve existir.

        Args:
            atendimento_id: Identificador único do atendimento.
            novo_status: Novo valor de status (``'aberto'``, ``'em andamento'``
                ou ``'finalizado'``).

        Returns:
            Tupla ``(sucesso, mensagem)``.
        """
        if novo_status not in STATUS_PERMITIDOS:
            return False, f"Status inválido. Valores aceitos: {', '.join(STATUS_PERMITIDOS)}."

        atualizado = self._atendimento_repo.atualizar_status(atendimento_id, novo_status)
        if not atualizado:
            return False, "Atendimento não encontrado."

        return True, "Status atualizado com sucesso."
