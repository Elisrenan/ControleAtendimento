"""Testes do PessoaService (camada de aplicação).

Usa FakePessoaRepository (in-memory) para garantir isolamento total
de banco de dados. Cobre todos os casos de uso do serviço.
"""

import pytest

from tests.conftest import FakePessoaRepository
from application.pessoa_service import PessoaService
from domain.entities import Pessoa


# ==============================================================
# cadastrar
# ==============================================================


class TestCadastrarPessoa:
    def test_cadastro_valido_retorna_sucesso(self, pessoa_svc: PessoaService):
        ok, msg = pessoa_svc.cadastrar("Ana Lima", "111.111.111-11", "(11) 99999-1111")
        assert ok is True
        assert "sucesso" in msg.lower()

    def test_pessoa_cadastrada_aparece_na_listagem(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana Lima", "111.111.111-11", "")
        pessoas = pessoa_svc.listar()
        assert len(pessoas) == 1
        assert pessoas[0].nome == "Ana Lima"

    def test_nome_vazio_retorna_erro(self, pessoa_svc: PessoaService):
        ok, msg = pessoa_svc.cadastrar("", "111.111.111-11", "")
        assert ok is False
        assert "nome" in msg.lower()

    def test_nome_apenas_espacos_retorna_erro(self, pessoa_svc: PessoaService):
        ok, msg = pessoa_svc.cadastrar("   ", "111.111.111-11", "")
        assert ok is False

    def test_cpf_vazio_retorna_erro(self, pessoa_svc: PessoaService):
        ok, msg = pessoa_svc.cadastrar("Ana Lima", "", "")
        assert ok is False
        assert "cpf" in msg.lower()

    def test_cpf_duplicado_retorna_erro(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana Lima", "111.111.111-11", "")
        ok, msg = pessoa_svc.cadastrar("Outro Nome", "111.111.111-11", "")
        assert ok is False
        assert "cpf" in msg.lower() or "cadastrado" in msg.lower()


# ==============================================================
# listar
# ==============================================================


class TestListarPessoas:
    def test_lista_vazia_sem_cadastros(self, pessoa_svc: PessoaService):
        assert pessoa_svc.listar() == []

    def test_retorna_lista_de_instancias_pessoa(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana", "111.111.111-11", "")
        resultado = pessoa_svc.listar()
        assert all(isinstance(p, Pessoa) for p in resultado)

    def test_ordenacao_por_nome(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Zilda", "333.333.333-33", "")
        pessoa_svc.cadastrar("Ana", "111.111.111-11", "")
        pessoa_svc.cadastrar("Maria", "222.222.222-22", "")
        nomes = [p.nome for p in pessoa_svc.listar()]
        assert nomes == sorted(nomes)


# ==============================================================
# buscar
# ==============================================================


class TestBuscarPessoa:
    def test_busca_por_nome_parcial(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana Lima", "111.111.111-11", "")
        resultado = pessoa_svc.buscar("Lima")
        assert len(resultado) == 1
        assert resultado[0].nome == "Ana Lima"

    def test_busca_por_cpf_parcial(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Carlos", "123.456.789-00", "")
        resultado = pessoa_svc.buscar("123")
        assert len(resultado) == 1

    def test_busca_sem_resultado_retorna_lista_vazia(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana", "111.111.111-11", "")
        assert pessoa_svc.buscar("xyz") == []


# ==============================================================
# excluir
# ==============================================================


class TestExcluirPessoa:
    def test_excluir_pessoa_existente_retorna_sucesso(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana", "111.111.111-11", "")
        pessoa_id = pessoa_svc.listar()[0].id
        ok, msg = pessoa_svc.excluir(pessoa_id)
        assert ok is True
        assert "sucesso" in msg.lower()

    def test_pessoa_removida_nao_aparece_na_listagem(self, pessoa_svc: PessoaService):
        pessoa_svc.cadastrar("Ana", "111.111.111-11", "")
        pessoa_id = pessoa_svc.listar()[0].id
        pessoa_svc.excluir(pessoa_id)
        assert pessoa_svc.listar() == []

    def test_excluir_id_inexistente_retorna_erro(self, pessoa_svc: PessoaService):
        ok, msg = pessoa_svc.excluir(9999)
        assert ok is False
        assert "não encontrada" in msg.lower()

    def test_excluir_com_atendimentos_ativos_retorna_erro(self, fake_pessoa_repo: FakePessoaRepository):
        """Usa um repositório com atendimentos ativos simulados."""

        class RepoComAtivos(FakePessoaRepository):
            def tem_atendimentos_ativos(self, pessoa_id: int) -> bool:
                return True

        svc = PessoaService(repo=RepoComAtivos())
        svc.cadastrar("Ana", "111.111.111-11", "")
        pessoa_id = svc.listar()[0].id
        ok, msg = svc.excluir(pessoa_id)
        assert ok is False
        assert "atendimento" in msg.lower()
