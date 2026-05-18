"""Fixtures e repositórios falsos compartilhados entre todos os testes.

Estratégia: testes de serviço usam ``FakePessoaRepository`` e
``FakeAtendimentoRepository`` (em memória pura, sem SQLite) para
garantir isolamento total e execução instantânea.

Testes de integração de repositório usam SQLite ``":memory:"``,
reinicializado a cada sessão de teste via fixture ``db_path``.
"""

import pytest

from application.atendimento_service import AtendimentoService
from application.pessoa_service import PessoaService
from domain.entities import Atendimento, Pessoa, StatusAtendimento
from domain.repositories import IAtendimentoRepository, IPessoaRepository
from infrastructure.database import init_db


# ==============================================================
# Repositórios falsos (in-memory) para testes unitários
# ==============================================================


class FakePessoaRepository(IPessoaRepository):
    """Repositório de Pessoa em memória para uso nos testes unitários."""

    def __init__(self) -> None:
        self._store: dict[int, Pessoa] = {}
        self._next_id: int = 1

    def salvar(self, pessoa: Pessoa) -> Pessoa:
        for p in self._store.values():
            if p.cpf == pessoa.cpf:
                raise ValueError(f"CPF já cadastrado: {pessoa.cpf}")
        pessoa.id = self._next_id
        self._store[self._next_id] = pessoa
        self._next_id += 1
        return pessoa

    def listar(self) -> list[Pessoa]:
        return sorted(self._store.values(), key=lambda p: p.nome)

    def buscar_por_nome_ou_cpf(self, termo: str) -> list[Pessoa]:
        termo_lower = termo.lower()
        return [
            p for p in self._store.values()
            if termo_lower in p.nome.lower() or termo_lower in p.cpf
        ]

    def buscar_por_id(self, pessoa_id: int) -> Pessoa | None:
        return self._store.get(pessoa_id)

    def excluir(self, pessoa_id: int) -> bool:
        if pessoa_id in self._store:
            del self._store[pessoa_id]
            return True
        return False

    def tem_atendimentos_ativos(self, pessoa_id: int) -> bool:
        return False  # comportamento padrão; sobrescreva no teste quando necessário


class FakeAtendimentoRepository(IAtendimentoRepository):
    """Repositório de Atendimento em memória para uso nos testes unitários."""

    def __init__(self) -> None:
        self._store: dict[int, Atendimento] = {}
        self._next_id: int = 1

    def salvar(self, atendimento: Atendimento) -> Atendimento:
        atendimento.id = self._next_id
        atendimento.status = StatusAtendimento.ABERTO
        self._store[self._next_id] = atendimento
        self._next_id += 1
        return atendimento

    def listar(self) -> list[Atendimento]:
        return sorted(self._store.values(), key=lambda a: -(a.id or 0))

    def buscar_por_id(self, atendimento_id: int) -> Atendimento | None:
        return self._store.get(atendimento_id)

    def atualizar_status(self, atendimento_id: int, novo_status: str) -> bool:
        if atendimento_id in self._store:
            self._store[atendimento_id].status = StatusAtendimento(novo_status)
            return True
        return False


# ==============================================================
# Fixtures pytest
# ==============================================================


@pytest.fixture
def fake_pessoa_repo() -> FakePessoaRepository:
    """Retorna um repositório de pessoas em memória limpo."""
    return FakePessoaRepository()


@pytest.fixture
def fake_atendimento_repo() -> FakeAtendimentoRepository:
    """Retorna um repositório de atendimentos em memória limpo."""
    return FakeAtendimentoRepository()


@pytest.fixture
def pessoa_svc(fake_pessoa_repo: FakePessoaRepository) -> PessoaService:
    """Retorna um PessoaService pronto com repositório em memória."""
    return PessoaService(repo=fake_pessoa_repo)


@pytest.fixture
def atendimento_svc(
    fake_atendimento_repo: FakeAtendimentoRepository,
    fake_pessoa_repo: FakePessoaRepository,
) -> AtendimentoService:
    """Retorna um AtendimentoService pronto com repositórios em memória."""
    return AtendimentoService(
        atendimento_repo=fake_atendimento_repo,
        pessoa_repo=fake_pessoa_repo,
    )


@pytest.fixture
def db_path(tmp_path) -> str:
    """Cria um banco SQLite temporário (em arquivo) para testes de integração."""
    path = str(tmp_path / "test.db")
    init_db(path)
    return path
