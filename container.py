"""Montagem das dependências (Dependency Injection Container).

Este módulo é o único lugar da aplicação onde as implementações concretas
de infraestrutura são instanciadas e injetadas nas camadas superiores.
Seguindo Clean Architecture, somente este arquivo conhece tanto o
``application`` quanto o ``infrastructure`` ao mesmo tempo.

Exemplo de uso em ``main.py``::

    from container import criar_container
    from config import DB_PATH

    pessoa_svc, atendimento_svc = criar_container(DB_PATH)
"""

from application.atendimento_service import AtendimentoService
from application.pessoa_service import PessoaService
from infrastructure.database import init_db
from infrastructure.repositories.atendimento_repository import SQLiteAtendimentoRepository
from infrastructure.repositories.pessoa_repository import SQLitePessoaRepository


def criar_container(db_path: str) -> tuple[PessoaService, AtendimentoService]:
    """Inicializa o banco de dados, cria os repositórios e injeta nos serviços.

    Deve ser chamado uma única vez no ponto de entrada da aplicação.
    Para testes, passe ``":memory:"`` como ``db_path`` para um banco isolado.

    Args:
        db_path: Caminho do arquivo ``.db`` (ou ``":memory:"`` para testes).

    Returns:
        Tupla ``(PessoaService, AtendimentoService)`` prontos para uso.

    Example:
        >>> from config import DB_PATH
        >>> pessoa_svc, atendimento_svc = criar_container(DB_PATH)
    """
    init_db(db_path)

    pessoa_repo = SQLitePessoaRepository(db_path)
    atendimento_repo = SQLiteAtendimentoRepository(db_path)

    pessoa_svc = PessoaService(repo=pessoa_repo)
    atendimento_svc = AtendimentoService(
        atendimento_repo=atendimento_repo,
        pessoa_repo=pessoa_repo,
    )

    return pessoa_svc, atendimento_svc
