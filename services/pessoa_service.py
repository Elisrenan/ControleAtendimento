from infrastructure.repositories import pessoa_repository
from domain.models import Pessoa


def cadastrar_pessoa(nome, cpf, telefone):
    if not nome.strip():
        return False, "O nome é obrigatório."

    if not cpf.strip():
        return False, "O CPF é obrigatório."

    try:
        pessoa = Pessoa(nome=nome, cpf=cpf, telefone=telefone)
        pessoa_repository.inserir(pessoa)
        return True, "Pessoa cadastrada com sucesso."

    except Exception as erro:
        return False, f"Erro ao cadastrar pessoa: {erro}"


def listar_pessoas():
    return pessoa_repository.listar_todos()


def buscar_pessoa_por_nome_ou_cpf(termo):
    return pessoa_repository.buscar_por_nome_ou_cpf(termo)


def buscar_pessoa_por_id(pessoa_id):
    return pessoa_repository.buscar_por_id(pessoa_id)


def excluir_pessoa(pessoa_id):
    total_ativos = pessoa_repository.contar_atendimentos_ativos(pessoa_id)

    if total_ativos > 0:
        return False, "Não é possível excluir pessoa com atendimento aberto ou em andamento."

    removido = pessoa_repository.excluir(pessoa_id)

    if not removido:
        return False, "Pessoa não encontrada."

    return True, "Pessoa excluída com sucesso."
