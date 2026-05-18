from infrastructure.repositories import atendimento_repository, pessoa_repository
from domain.models import Atendimento


STATUS_PERMITIDOS = ["aberto", "em andamento", "finalizado"]


def registrar_atendimento(pessoa_id, descricao):
    pessoa = pessoa_repository.buscar_por_id(pessoa_id)

    if pessoa is None:
        return False, "Pessoa não encontrada."

    if not descricao.strip():
        return False, "A descrição do atendimento é obrigatória."

    try:
        atendimento = Atendimento(pessoa_id=pessoa_id, descricao=descricao, status="aberto")
        atendimento_repository.inserir(atendimento)
        return True, "Atendimento registrado com sucesso."

    except Exception as erro:
        return False, f"Erro ao registrar atendimento: {erro}"


def listar_atendimentos():
    return atendimento_repository.listar_todos()


def atualizar_status_atendimento(atendimento_id, novo_status):
    if novo_status not in STATUS_PERMITIDOS:
        return False, "Status inválido."

    atualizado = atendimento_repository.atualizar_status(atendimento_id, novo_status)

    if not atualizado:
        return False, "Atendimento não encontrado."

    return True, "Status atualizado com sucesso."
