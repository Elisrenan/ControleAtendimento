from services.pessoa_service import (
    cadastrar_pessoa,
    listar_pessoas,
    buscar_pessoa_por_nome_ou_cpf,
    buscar_pessoa_por_id,
    excluir_pessoa,
)


def test_cadastrar_pessoa_com_sucesso():
    ok, msg = cadastrar_pessoa("Ana Lima", "111.222.333-44", "(11) 91111-2222")
    assert ok is True
    assert "sucesso" in msg.lower()


def test_cadastrar_pessoa_nome_vazio():
    ok, msg = cadastrar_pessoa("   ", "111.222.333-44", "")
    assert ok is False
    assert "nome" in msg.lower()


def test_cadastrar_pessoa_cpf_vazio():
    ok, msg = cadastrar_pessoa("Ana Lima", "   ", "")
    assert ok is False
    assert "cpf" in msg.lower()


def test_cadastrar_pessoa_cpf_duplicado():
    cadastrar_pessoa("Ana Lima", "111.222.333-44", "")
    ok, msg = cadastrar_pessoa("Outro Nome", "111.222.333-44", "")
    assert ok is False


def test_listar_pessoas_vazio():
    assert listar_pessoas() == []


def test_listar_pessoas_retorna_dataclass():
    cadastrar_pessoa("Carlos", "222.333.444-55", "")
    pessoas = listar_pessoas()
    assert len(pessoas) == 1
    assert pessoas[0].nome == "Carlos"
    assert pessoas[0].cpf == "222.333.444-55"


def test_listar_pessoas_ordenado_por_nome():
    cadastrar_pessoa("Zilda", "111.000.000-01", "")
    cadastrar_pessoa("Ana", "111.000.000-02", "")
    nomes = [p.nome for p in listar_pessoas()]
    assert nomes == sorted(nomes)


def test_buscar_por_nome():
    cadastrar_pessoa("Maria Souza", "333.444.555-66", "")
    resultado = buscar_pessoa_por_nome_ou_cpf("Maria")
    assert any(p.nome == "Maria Souza" for p in resultado)


def test_buscar_por_cpf():
    cadastrar_pessoa("João Silva", "444.555.666-77", "")
    resultado = buscar_pessoa_por_nome_ou_cpf("444.555.666-77")
    assert any(p.cpf == "444.555.666-77" for p in resultado)


def test_buscar_sem_resultado():
    resultado = buscar_pessoa_por_nome_ou_cpf("nao existe")
    assert resultado == []


def test_buscar_por_id():
    cadastrar_pessoa("Laura", "555.666.777-88", "")
    pessoas = listar_pessoas()
    encontrada = buscar_pessoa_por_id(pessoas[0].id)
    assert encontrada is not None
    assert encontrada.nome == "Laura"


def test_buscar_por_id_inexistente():
    assert buscar_pessoa_por_id(99999) is None


def test_excluir_pessoa_sem_atendimento():
    cadastrar_pessoa("Pedro", "666.777.888-99", "")
    pessoa_id = listar_pessoas()[0].id
    ok, msg = excluir_pessoa(pessoa_id)
    assert ok is True
    assert listar_pessoas() == []


def test_excluir_pessoa_inexistente():
    ok, msg = excluir_pessoa(99999)
    assert ok is False
    assert "não encontrada" in msg.lower()
