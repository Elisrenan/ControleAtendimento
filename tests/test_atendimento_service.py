"""
Testes de unidade para services/atendimento_service.py.

Cada teste exercita uma função do service isoladamente.
O banco de dados é substituído por um banco temporário via conftest.py.

Fluxo testado:
    test → atendimento_service → atendimento_repository → SQLite (temporário)
                               → pessoa_repository      → SQLite (temporário)
"""
import pytest
from services.pessoa_service import cadastrar_pessoa, listar_pessoas, excluir_pessoa
from services.atendimento_service import (
    registrar_atendimento,
    listar_atendimentos,
    atualizar_status_atendimento,
)


def _criar_pessoa(cpf="000.000.000-00"):
    """Auxiliar: cria uma pessoa e retorna seu ID. Atalho reutilizado nos testes."""
    cadastrar_pessoa("Pessoa Teste", cpf, "")
    return listar_pessoas()[0].id


# ─── registrar_atendimento ────────────────────────────────────────────────────

def test_registrar_atendimento_com_sucesso():
    """Registrar um atendimento com dados válidos deve retornar True."""
    pid = _criar_pessoa()
    ok, msg = registrar_atendimento(pid, "Consulta inicial")
    assert ok is True
    assert "sucesso" in msg.lower()


def test_registrar_atendimento_pessoa_inexistente():
    """Registrar atendimento para ID inexistente deve retornar False com mensagem 'não encontrada'."""
    ok, msg = registrar_atendimento(99999, "Consulta")
    assert ok is False
    assert "não encontrada" in msg.lower()


def test_registrar_atendimento_descricao_vazia():
    """Descrição formada só por espaços deve ser rejeitada com False."""
    pid = _criar_pessoa()
    ok, msg = registrar_atendimento(pid, "   ")
    assert ok is False
    assert "descrição" in msg.lower()


# ─── listar_atendimentos ──────────────────────────────────────────────────────

def test_listar_atendimentos_vazio():
    """Banco recém-criado deve retornar lista vazia de atendimentos."""
    assert listar_atendimentos() == []


def test_listar_atendimentos_retorna_dataclass():
    """Confirma que o resultado é lista de Atendimento com pessoa_nome preenchido pelo JOIN."""
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Primeiro atendimento")
    ats = listar_atendimentos()
    assert len(ats) == 1
    assert ats[0].descricao == "Primeiro atendimento"
    assert ats[0].pessoa_nome == "Pessoa Teste"


def test_atendimento_criado_com_status_aberto():
    """Todo atendimento recém-criado deve ter status inicial 'aberto'."""
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Novo atendimento")
    assert listar_atendimentos()[0].status == "aberto"


# ─── atualizar_status_atendimento ─────────────────────────────────────────────

@pytest.mark.parametrize("status", ["aberto", "em andamento", "finalizado"])
def test_atualizar_para_status_valido(status):
    """Cada um dos três status permitidos deve ser aceito pelo service."""
    pid = _criar_pessoa(cpf=f"000.000.000-{status[:2]}")
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    ok, msg = atualizar_status_atendimento(at_id, status)
    assert ok is True


def test_atualizar_status_invalido():
    """Status fora dos três valores permitidos deve ser rejeitado com False."""
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    ok, msg = atualizar_status_atendimento(at_id, "cancelado")
    assert ok is False
    assert "status" in msg.lower()


def test_atualizar_status_atendimento_inexistente():
    """Atualizar status de ID que não existe deve retornar False."""
    ok, msg = atualizar_status_atendimento(99999, "finalizado")
    assert ok is False
    assert "não encontrado" in msg.lower()


# ─── regra de negócio: exclusão bloqueada ────────────────────────────────────

def test_excluir_pessoa_com_atendimento_aberto_bloqueado():
    """Não deve ser possível excluir pessoa com atendimento 'aberto' ou 'em andamento'."""
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento ativo")
    ok, msg = excluir_pessoa(pid)
    assert ok is False
    assert "não é possível excluir" in msg.lower()


def test_excluir_pessoa_permitida_apos_finalizar():
    """Após finalizar o único atendimento, a pessoa deve poder ser excluída."""
    pid = _criar_pessoa()
    registrar_atendimento(pid, "Atendimento")
    at_id = listar_atendimentos()[0].id
    atualizar_status_atendimento(at_id, "finalizado")
    ok, msg = excluir_pessoa(pid)
    assert ok is True
