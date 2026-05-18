import pytest
from services.pessoa_service import cadastrar_pessoa, listar_pessoas, excluir_pessoa
from services.atendimento_service import (
    registrar_atendimento,
    listar_atendimentos,
    atualizar_status_atendimento,
)


def _criar_pessoa(cpf="000.000.000-00"):
    cadastrar_pessoa("Pessoa Teste", cpf, "")
    return listar_pessoas()[0].id


# ─── registrar_atendimento ────────────────────────────────────────────────────

def test_registrar_atendimento_com_sucesso():
    pid = _criar_pessoa()
    ok, msg = registrar_atendimento(pid, "Consulta inicial")
    assert ok is True
    assert "sucesso" in msg.lower()


def test_registrar_atendimento_pessoa_inexistente():
    ok, msg = registrar_atendimento(99999, "Consulta")
    assert ok is False
    assert "não encontrada" in msg.lower()


def test_registrar_atendimento_descricao_vazia():
    pid = _criar_pessoa()
    ok, msg = registrar_atendimento(pid, "   ")
    assert ok is False
    assert "descrição" in msg.lower()


# ─── listar_atendimentos ──────────────────────────────────────────────────────

def test_listar_atendimentos_vazio():
    assert listar_atendimentos() == []


def test_listar_atendimentos_retorna_dataclass():
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Primeiro atendimento")
    ats = listar_atendimentos()
    assert len(ats) == 1
    assert ats[0].descricao == "Primeiro atendimento"
    assert ats[0].pessoa_nome == "Pessoa Teste"


def test_atendimento_criado_com_status_aberto():
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Novo atendimento")
    assert listar_atendimentos()[0].status == "aberto"


# ─── atualizar_status_atendimento ─────────────────────────────────────────────

@pytest.mark.parametrize("status", ["aberto", "em andamento", "finalizado"])
def test_atualizar_para_status_valido(status):
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    ok, msg = atualizar_status_atendimento(at_id, status)
    assert ok is True


def test_atualizar_status_invalido():
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    ok, msg = atualizar_status_atendimento(at_id, "cancelado")
    assert ok is False
    assert "status" in msg.lower()


def test_atualizar_status_atendimento_inexistente():
    ok, msg = atualizar_status_atendimento(99999, "finalizado")
    assert ok is False
    assert "não encontrado" in msg.lower()


# ─── regra de negócio: exclusão bloqueada ────────────────────────────────────

def test_excluir_pessoa_com_atendimento_aberto_bloqueado():
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento ativo")
    ok, msg = excluir_pessoa(pid)
    assert ok is False
    assert "não é possível excluir" in msg.lower()


def test_excluir_pessoa_permitida_apos_finalizar():
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    atualizar_status_atendimento(at_id, "finalizado")
    ok, msg = excluir_pessoa(pid)
    assert ok is True
