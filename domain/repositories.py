"""Interfaces (contratos) de repositório do domínio.

Define os ABCs que toda implementação de persistência deve respeitar.
Seguindo o Princípio da Inversão de Dependência (DIP), as camadas de
aplicação dependem destas abstrações — nunca das implementações concretas.
"""

from abc import ABC, abstractmethod

from domain.entities import Atendimento, Pessoa


class IPessoaRepository(ABC):
    """Contrato de persistência para a entidade ``Pessoa``.

    Qualquer implementação (SQLite, PostgreSQL, em memória para testes)
    deve herdar desta classe e implementar todos os métodos abstratos.
    """

    @abstractmethod
    def salvar(self, pessoa: Pessoa) -> Pessoa:
        """Persiste uma nova pessoa e retorna a entidade com o ``id`` preenchido.

        Args:
            pessoa: Instância de ``Pessoa`` com ``id=None``.

        Returns:
            A mesma instância com o ``id`` atribuído pelo banco.

        Raises:
            ValueError: Se o CPF já estiver cadastrado.
        """

    @abstractmethod
    def listar(self) -> list[Pessoa]:
        """Retorna todas as pessoas ordenadas por nome.

        Returns:
            Lista (possivelmente vazia) de instâncias ``Pessoa``.
        """

    @abstractmethod
    def buscar_por_nome_ou_cpf(self, termo: str) -> list[Pessoa]:
        """Busca pessoas cujo nome ou CPF contenha o termo informado.

        Args:
            termo: Substring para busca (case-insensitive).

        Returns:
            Lista de ``Pessoa`` que correspondem ao critério.
        """

    @abstractmethod
    def buscar_por_id(self, pessoa_id: int) -> Pessoa | None:
        """Retorna a pessoa com o ``id`` informado, ou ``None`` se não existir.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            Instância de ``Pessoa`` ou ``None``.
        """

    @abstractmethod
    def excluir(self, pessoa_id: int) -> bool:
        """Remove a pessoa com o ``id`` informado.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            ``True`` se o registro foi removido; ``False`` se não encontrado.
        """

    @abstractmethod
    def tem_atendimentos_ativos(self, pessoa_id: int) -> bool:
        """Verifica se a pessoa possui atendimentos com status 'aberto' ou 'em andamento'.

        Args:
            pessoa_id: Identificador único da pessoa.

        Returns:
            ``True`` se existir ao menos um atendimento ativo.
        """


class IAtendimentoRepository(ABC):
    """Contrato de persistência para a entidade ``Atendimento``.

    Qualquer implementação deve herdar desta classe e implementar
    todos os métodos abstratos.
    """

    @abstractmethod
    def salvar(self, atendimento: Atendimento) -> Atendimento:
        """Persiste um novo atendimento e retorna a entidade com o ``id`` preenchido.

        Args:
            atendimento: Instância de ``Atendimento`` com ``id=None``.

        Returns:
            A mesma instância com o ``id`` atribuído pelo banco.
        """

    @abstractmethod
    def listar(self) -> list[Atendimento]:
        """Retorna todos os atendimentos em ordem decrescente de ID.

        O campo ``nome_pessoa`` é preenchido via JOIN.

        Returns:
            Lista (possivelmente vazia) de instâncias ``Atendimento``.
        """

    @abstractmethod
    def buscar_por_id(self, atendimento_id: int) -> Atendimento | None:
        """Retorna o atendimento com o ``id`` informado, ou ``None`` se não existir.

        Args:
            atendimento_id: Identificador único do atendimento.

        Returns:
            Instância de ``Atendimento`` ou ``None``.
        """

    @abstractmethod
    def atualizar_status(self, atendimento_id: int, novo_status: str) -> bool:
        """Atualiza o status do atendimento indicado.

        Args:
            atendimento_id: Identificador único do atendimento.
            novo_status: Novo valor de status (deve ser membro de ``StatusAtendimento``).

        Returns:
            ``True`` se atualizado; ``False`` se não encontrado.
        """
