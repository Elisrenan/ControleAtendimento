"""
Testes de unidade para services/pessoa_service.py.

Cada teste exercita uma função do service isoladamente.
O banco de dados é substituído por um banco temporário via conftest.py.

Fluxo testado:
    test → pessoa_service → pessoa_repository → SQLite (temporário)
"""
from services.pessoa_service import (
    cadastrar_pessoa,
    listar_pessoas,
    buscar_pessoa_por_nome_ou_cpf,
    buscar_pessoa_por_id,
    excluir_pessoa,
)


def test_cadastrar_pessoa_com_sucesso():
    """Garante que uma pessoa válida é cadastrada e retorna True."""
    ok, msg = cadastrar_pessoa("João Silva", "111.222.333-44", "99999-0000")
    assert ok is True
    assert "sucesso" in msg.lower()


def test_cadastrar_pessoa_nome_vazio():
    """Nome formado só por espaços deve ser rejeitado com False."""
    ok, msg = cadastrar_pessoa("   ", "111.222.333-44", "")
    assert ok is False
    assert "nome" in msg.lower()


def test_cadastrar_pessoa_cpf_vazio():
    """CPF formado só por espaços deve ser rejeitado com False."""
    ok, msg = cadastrar_pessoa("João", "   ", "")
    assert ok is False
    assert "cpf" in msg.lower()


def test_cadastrar_pessoa_cpf_duplicado():
    """Inserir duas pessoas com o mesmo CPF deve retornar False na segunda tentativa."""
    cadastrar_pessoa("Nome Um", "111.222.333-44", "")
    ok, msg = cadastrar_pessoa("Outro Nome", "111.222.333-44", "")
    assert ok is False


def test_listar_pessoas_vazio():
    """Banco recém-criado deve retornar lista vazia."""
    assert listar_pessoas() == []


def test_listar_pessoas_retorna_dataclass():
    """Confirma que os registros retornados são objetos Pessoa com atributos nomeados."""
    cadastrar_pessoa("Carlos", "222.333.444-55", "")
    pessoas = listar_pessoas()
    assert len(pessoas) == 1
    assert pessoas[0].nome == "Carlos"
    assert pessoas[0].cpf == "222.333.444-55"


def test_listar_pessoas_ordenado_por_nome():
    """Garante que o resultado está ordenado alfabética e crescentemente por nome."""
    cadastrar_pessoa("Zara", "111.000.000-01", "")
    cadastrar_pessoa("Ana", "111.000.000-02", "")
    nomes = [p.nome for p in listar_pessoas()]
    assert nomes == sorted(nomes)


def test_buscar_por_nome():
    """Busca por parte do nome deve retornar a pessoa correspondente."""
    cadastrar_pessoa("Maria Souza", "333.444.555-66", "")
    resultado = buscar_pessoa_por_nome_ou_cpf("Maria")
    assert any(p.nome == "Maria Souza" for p in resultado)


def test_buscar_por_cpf():
    """Busca por CPF completo deve retornar a pessoa correspondente."""
    cadastrar_pessoa("Fernanda", "444.555.666-77", "")
    resultado = buscar_pessoa_por_nome_ou_cpf("444.555.666-77")
    assert any(p.cpf == "444.555.666-77" for p in resultado)


def test_buscar_sem_resultado():
    """Busca por termo inexistente deve retornar lista vazia."""
    resultado = buscar_pessoa_por_nome_ou_cpf("zzznaoexiste")
    assert resultado == []


def test_buscar_por_id():
    """Buscar pelo ID de uma pessoa existente deve retornar o objeto correto."""
    cadastrar_pessoa("Laura", "555.666.777-88", "")
    pessoas = listar_pessoas()
    encontrada = buscar_pessoa_por_id(pessoas[0].id)
    assert encontrada is not None
    assert encontrada.nome == "Laura"


def test_buscar_por_id_inexistente():
    """Buscar por ID que não existe deve retornar None."""
    resultado = buscar_pessoa_por_id(99999)
    assert resultado is None


def test_excluir_pessoa_sem_atendimento():
    """Pessoa sem atendimentos deve poder ser excluída. Após a exclusão o banco fica vazio."""
    cadastrar_pessoa("Pedro", "666.777.888-99", "")
    pessoa_id = listar_pessoas()[0].id
    ok, msg = excluir_pessoa(pessoa_id)
    assert ok is True
    assert listar_pessoas() == []


def test_excluir_pessoa_inexistente():
    """Tentar excluir um ID que não existe deve retornar False com mensagem adequada."""
    ok, msg = excluir_pessoa(99999)
    assert ok is False
    assert "não encontrada" in msg.lower()
