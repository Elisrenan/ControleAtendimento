"""Testes das entidades de domínio.

Verifica criação, normalização e comportamento dos dataclasses e enum,
sem nenhuma dependência de banco de dados ou serviços.
"""

import pytest

from domain.entities import Atendimento, Pessoa, StatusAtendimento


# ==============================================================
# StatusAtendimento
# ==============================================================


class TestStatusAtendimento:
    def test_valores_corretos(self):
        assert StatusAtendimento.ABERTO.value == "aberto"
        assert StatusAtendimento.EM_ANDAMENTO.value == "em andamento"
        assert StatusAtendimento.FINALIZADO.value == "finalizado"

    def test_criacao_a_partir_de_string(self):
        status = StatusAtendimento("aberto")
        assert status == StatusAtendimento.ABERTO

    def test_string_invalida_levanta_value_error(self):
        with pytest.raises(ValueError):
            StatusAtendimento("inexistente")


# ==============================================================
# Pessoa
# ==============================================================


class TestPessoa:
    def test_criacao_basica(self):
        p = Pessoa(nome="João Silva", cpf="000.000.000-00", telefone="(11) 99999-9999")
        assert p.nome == "João Silva"
        assert p.cpf == "000.000.000-00"
        assert p.telefone == "(11) 99999-9999"
        assert p.id is None

    def test_nome_e_cpf_sao_normalizados(self):
        p = Pessoa(nome="  Ana  ", cpf="  111.111.111-11  ")
        assert p.nome == "Ana"
        assert p.cpf == "111.111.111-11"

    def test_telefone_padrao_vazio(self):
        p = Pessoa(nome="Carlos", cpf="222.222.222-22")
        assert p.telefone == ""

    def test_telefone_none_vira_string_vazia(self):
        p = Pessoa(nome="Carlos", cpf="222.222.222-22", telefone=None)  # type: ignore[arg-type]
        assert p.telefone == ""

    def test_id_pode_ser_atribuido(self):
        p = Pessoa(nome="Maria", cpf="333.333.333-33", id=42)
        assert p.id == 42


# ==============================================================
# Atendimento
# ==============================================================


class TestAtendimento:
    def test_criacao_basica(self):
        a = Atendimento(pessoa_id=1, descricao="Suporte técnico")
        assert a.pessoa_id == 1
        assert a.descricao == "Suporte técnico"
        assert a.status == StatusAtendimento.ABERTO
        assert a.id is None
        assert a.nome_pessoa == ""

    def test_descricao_normalizada(self):
        a = Atendimento(pessoa_id=1, descricao="  Manutenção  ")
        assert a.descricao == "Manutenção"

    def test_status_string_convertido_para_enum(self):
        a = Atendimento(pessoa_id=1, descricao="Teste", status="finalizado")  # type: ignore[arg-type]
        assert a.status == StatusAtendimento.FINALIZADO

    def test_status_padrao_aberto(self):
        a = Atendimento(pessoa_id=2, descricao="Outro")
        assert a.status == StatusAtendimento.ABERTO

    def test_nome_pessoa_nao_participa_da_comparacao(self):
        a1 = Atendimento(pessoa_id=1, descricao="X", id=1, nome_pessoa="João")
        a2 = Atendimento(pessoa_id=1, descricao="X", id=1, nome_pessoa="Maria")
        assert a1 == a2
