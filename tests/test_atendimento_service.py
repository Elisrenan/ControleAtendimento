"""Testes do AtendimentoService (camada de aplicação).

Usa FakeAtendimentoRepository e FakePessoaRepository (in-memory) para
garantir isolamento total de banco de dados. Cobre todos os casos de uso.
"""

import pytest

from application.atendimento_service import AtendimentoService
from application.pessoa_service import PessoaService
from domain.entities import Atendimento, StatusAtendimento
from tests.conftest import FakeAtendimentoRepository, FakePessoaRepository


# ==============================================================
# Helpers
# ==============================================================


def _criar_pessoa_e_obter_id(pessoa_svc: PessoaService) -> int:
    """Cadastra uma pessoa e retorna o ID gerado."""
    pessoa_svc.cadastrar("Ana Lima", "111.111.111-11", "")
    return pessoa_svc.listar()[0].id  # type: ignore[return-value]


# ==============================================================
# registrar
# ==============================================================


class TestRegistrarAtendimento:
    def test_registrar_valido_retorna_sucesso(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        ok, msg = atendimento_svc.registrar(pessoa_id, "Suporte técnico")
        assert ok is True
        assert "sucesso" in msg.lower()

    def test_atendimento_registrado_aparece_na_listagem(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Suporte técnico")
        atendimentos = atendimento_svc.listar()
        assert len(atendimentos) == 1
        assert atendimentos[0].descricao == "Suporte técnico"

    def test_status_inicial_e_aberto(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Manutenção")
        atendimento = atendimento_svc.listar()[0]
        assert atendimento.status == StatusAtendimento.ABERTO

    def test_pessoa_inexistente_retorna_erro(self, atendimento_svc: AtendimentoService):
        ok, msg = atendimento_svc.registrar(9999, "Descrição qualquer")
        assert ok is False
        assert "não encontrada" in msg.lower()

    def test_descricao_vazia_retorna_erro(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        ok, msg = atendimento_svc.registrar(pessoa_id, "")
        assert ok is False
        assert "descrição" in msg.lower()

    def test_descricao_apenas_espacos_retorna_erro(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        ok, msg = atendimento_svc.registrar(pessoa_id, "   ")
        assert ok is False


# ==============================================================
# listar
# ==============================================================


class TestListarAtendimentos:
    def test_lista_vazia_sem_registros(self, atendimento_svc: AtendimentoService):
        assert atendimento_svc.listar() == []

    def test_retorna_instancias_atendimento(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Consulta")
        resultado = atendimento_svc.listar()
        assert all(isinstance(a, Atendimento) for a in resultado)

    def test_ordem_decrescente_por_id(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Primeiro")
        atendimento_svc.registrar(pessoa_id, "Segundo")
        ids = [a.id for a in atendimento_svc.listar()]
        assert ids == sorted(ids, reverse=True)


# ==============================================================
# atualizar_status
# ==============================================================


class TestAtualizarStatus:
    def test_atualizar_para_em_andamento(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Suporte")
        atendimento_id = atendimento_svc.listar()[0].id

        ok, msg = atendimento_svc.atualizar_status(atendimento_id, "em andamento")
        assert ok is True
        assert "sucesso" in msg.lower()

    def test_atualizar_para_finalizado(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Suporte")
        atendimento_id = atendimento_svc.listar()[0].id

        ok, _ = atendimento_svc.atualizar_status(atendimento_id, "finalizado")
        assert ok is True

        atendimento_atualizado = atendimento_svc.listar()[0]
        assert atendimento_atualizado.status == StatusAtendimento.FINALIZADO

    def test_status_invalido_retorna_erro(
        self,
        atendimento_svc: AtendimentoService,
        pessoa_svc: PessoaService,
    ):
        pessoa_id = _criar_pessoa_e_obter_id(pessoa_svc)
        atendimento_svc.registrar(pessoa_id, "Suporte")
        atendimento_id = atendimento_svc.listar()[0].id

        ok, msg = atendimento_svc.atualizar_status(atendimento_id, "cancelado")
        assert ok is False
        assert "inválido" in msg.lower()

    def test_id_inexistente_retorna_erro(self, atendimento_svc: AtendimentoService):
        ok, msg = atendimento_svc.atualizar_status(9999, "finalizado")
        assert ok is False
        assert "não encontrado" in msg.lower()
