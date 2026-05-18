"""Serviço de aplicação para a entidade Pessoa.

Orquestra as regras de negócio de pessoas delegando a persistência ao
repositório injetado. Segue o Princípio da Inversão de Dependência:
depende da interface ``IPessoaRepository``, não de nenhuma implementação
concreta.
"""

from domain.entities import Pessoa
from domain.repositories import IPessoaRepository


class PessoaService:
    """Casos de uso relacionados ao cadastro e consulta de pessoas.

    Args:
        repo: Implementação de ``IPessoaRepository`` a ser utilizada.
            Pode ser o repositório SQLite em produção ou um repositório
            em memória nos testes.

    Example:
        >>> from tests.fakes import FakePessoaRepository
        >>> service = PessoaService(repo=FakePessoaRepository())
        >>> ok, msg = service.cadastrar("Ana", "111.111.111-11", "")
        >>> ok
        True
    """

    def __init__(self, repo: IPessoaRepository) -> None:
        self._repo = repo

    # ------------------------------------------------------------------
    # Casos de uso
    # ------------------------------------------------------------------

    def cadastrar(self, nome: str, cpf: str, telefone: str) -> tuple[bool, str]:
        """Valida os dados e cadastra uma nova pessoa.

        Regras de negócio:
        - Nome não pode ser vazio.
        - CPF não pode ser vazio.
        - CPF deve ser único no sistema.

        Args:
            nome: Nome completo da pessoa.
            cpf: CPF da pessoa (sem formatação obrigatória).
            telefone: Telefone de contato (pode ser vazio).

        Returns:
            Tupla ``(sucesso, mensagem)`` onde ``sucesso`` é ``True`` em caso
            de cadastro bem-sucedido e ``mensagem`` descreve o resultado.
        """
        if not nome.strip():
            return False, "O nome é obrigatório."

        if not cpf.strip():
            return False, "O CPF é obrigatório."

        try:
            self._repo.salvar(Pessoa(nome=nome, cpf=cpf, telefone=telefone))
            return True, "Pessoa cadastrada com sucesso."
        except ValueError as erro:
            return False, str(erro)

    def listar(self) -> list[Pessoa]:
        """Retorna todas as pessoas cadastradas em ordem alfabética.

        Returns:
            Lista de instâncias ``Pessoa`` (pode ser vazia).
        """
        return self._repo.listar()

    def buscar(self, termo: str) -> list[Pessoa]:
        """Busca pessoas pelo nome ou CPF.

        Args:
            termo: Substring para busca.

        Returns:
            Lista de ``Pessoa`` cujo nome ou CPF contém ``termo``.
        """
        return self._repo.buscar_por_nome_ou_cpf(termo)

    def excluir(self, pessoa_id: int) -> tuple[bool, str]:
        """Remove a pessoa se ela não possuir atendimentos ativos.

        Regra de negócio: não é permitido excluir uma pessoa com
        atendimentos com status ``'aberto'`` ou ``'em andamento'``.

        Args:
            pessoa_id: Identificador único da pessoa a ser removida.

        Returns:
            Tupla ``(sucesso, mensagem)``.
        """
        if self._repo.tem_atendimentos_ativos(pessoa_id):
            return (
                False,
                "Não é possível excluir pessoa com atendimento aberto ou em andamento.",
            )

        removida = self._repo.excluir(pessoa_id)
        if not removida:
            return False, "Pessoa não encontrada."

        return True, "Pessoa excluída com sucesso."
