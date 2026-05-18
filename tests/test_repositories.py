"""Testes de integração dos repositórios SQLite.

Usa banco SQLite em arquivo temporário (fixture ``db_path`` do conftest).
Verifica que as implementações concretas satisfazem os contratos do domínio.
"""

import pytest

from domain.entities import Atendimento, Pessoa, StatusAtendimento
from infrastructure.repositories.atendimento_repository import SQLiteAtendimentoRepository
from infrastructure.repositories.pessoa_repository import SQLitePessoaRepository


# ==============================================================
# Helpers
# ==============================================================


def _salvar_pessoa(repo: SQLitePessoaRepository, cpf: str = "111.111.111-11") -> Pessoa:
    return repo.salvar(Pessoa(nome="Ana Lima", cpf=cpf, telefone=""))


# ==============================================================
# SQLitePessoaRepository
# ==============================================================


class TestSQLitePessoaRepository:
    def test_salvar_retorna_id(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        pessoa = _salvar_pessoa(repo)
        assert pessoa.id is not None
        assert pessoa.id > 0

    def test_listar_retorna_pessoas(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        _salvar_pessoa(repo)
        assert len(repo.listar()) == 1

    def test_listar_retorna_ordenado_por_nome(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        repo.salvar(Pessoa(nome="Zilda", cpf="333.333.333-33"))
        repo.salvar(Pessoa(nome="Ana", cpf="111.111.111-11"))
        nomes = [p.nome for p in repo.listar()]
        assert nomes == sorted(nomes)

    def test_buscar_por_nome(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        _salvar_pessoa(repo)
        resultado = repo.buscar_por_nome_ou_cpf("Lima")
        assert len(resultado) == 1

    def test_buscar_por_cpf(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        _salvar_pessoa(repo)
        resultado = repo.buscar_por_nome_ou_cpf("111")
        assert len(resultado) == 1

    def test_buscar_sem_resultado(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        assert repo.buscar_por_nome_ou_cpf("xyz") == []

    def test_buscar_por_id_existente(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        pessoa = _salvar_pessoa(repo)
        encontrada = repo.buscar_por_id(pessoa.id)  # type: ignore[arg-type]
        assert encontrada is not None
        assert encontrada.cpf == "111.111.111-11"

    def test_buscar_por_id_inexistente_retorna_none(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        assert repo.buscar_por_id(9999) is None

    def test_cpf_duplicado_levanta_value_error(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        _salvar_pessoa(repo)
        with pytest.raises(ValueError, match="CPF já cadastrado"):
            _salvar_pessoa(repo)  # mesmo CPF

    def test_excluir_existente_retorna_true(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        pessoa = _salvar_pessoa(repo)
        assert repo.excluir(pessoa.id) is True  # type: ignore[arg-type]
        assert repo.buscar_por_id(pessoa.id) is None  # type: ignore[arg-type]

    def test_excluir_inexistente_retorna_false(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        assert repo.excluir(9999) is False

    def test_tem_atendimentos_ativos_false_sem_atendimentos(self, db_path: str):
        repo = SQLitePessoaRepository(db_path)
        pessoa = _salvar_pessoa(repo)
        assert repo.tem_atendimentos_ativos(pessoa.id) is False  # type: ignore[arg-type]

    def test_tem_atendimentos_ativos_true_com_aberto(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)
        atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="Teste"))  # type: ignore[arg-type]
        assert pessoa_repo.tem_atendimentos_ativos(pessoa.id) is True  # type: ignore[arg-type]


# ==============================================================
# SQLiteAtendimentoRepository
# ==============================================================


class TestSQLiteAtendimentoRepository:
    def test_salvar_retorna_id_e_status_aberto(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)

        atendimento = atend_repo.salvar(
            Atendimento(pessoa_id=pessoa.id, descricao="Suporte")  # type: ignore[arg-type]
        )
        assert atendimento.id is not None
        assert atendimento.status == StatusAtendimento.ABERTO

    def test_listar_retorna_atendimentos_com_nome_pessoa(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)
        atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="X"))  # type: ignore[arg-type]

        atendimentos = atend_repo.listar()
        assert len(atendimentos) == 1
        assert atendimentos[0].nome_pessoa == "Ana Lima"

    def test_listar_ordem_decrescente(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)
        atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="A"))  # type: ignore[arg-type]
        atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="B"))  # type: ignore[arg-type]

        ids = [a.id for a in atend_repo.listar()]
        assert ids == sorted(ids, reverse=True)

    def test_buscar_por_id_existente(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)
        salvo = atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="Y"))  # type: ignore[arg-type]

        encontrado = atend_repo.buscar_por_id(salvo.id)  # type: ignore[arg-type]
        assert encontrado is not None
        assert encontrado.descricao == "Y"

    def test_buscar_por_id_inexistente_retorna_none(self, db_path: str):
        atend_repo = SQLiteAtendimentoRepository(db_path)
        assert atend_repo.buscar_por_id(9999) is None

    def test_atualizar_status_retorna_true(self, db_path: str):
        pessoa_repo = SQLitePessoaRepository(db_path)
        atend_repo = SQLiteAtendimentoRepository(db_path)
        pessoa = _salvar_pessoa(pessoa_repo)
        salvo = atend_repo.salvar(Atendimento(pessoa_id=pessoa.id, descricao="Z"))  # type: ignore[arg-type]

        resultado = atend_repo.atualizar_status(salvo.id, "finalizado")  # type: ignore[arg-type]
        assert resultado is True

        atualizado = atend_repo.buscar_por_id(salvo.id)  # type: ignore[arg-type]
        assert atualizado is not None
        assert atualizado.status == StatusAtendimento.FINALIZADO

    def test_atualizar_status_inexistente_retorna_false(self, db_path: str):
        atend_repo = SQLiteAtendimentoRepository(db_path)
        assert atend_repo.atualizar_status(9999, "finalizado") is False
