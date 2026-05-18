"""
Camada de Serviços — regras de negócio de atendimentos.

Nenhuma query SQL está aqui. As validações e as regras vivem nesta camada;
a persistência é delegada ao repositório.

Cada função que modifica dados retorna uma tupla (bool, str):
    (True,  'mensagem de sucesso')
    (False, 'mensagem de erro')

Chamado por:
    ui/cli.py → todas as funções
    ui/gui.py → todas as funções

Chama:
    infrastructure/repositories/atendimento_repository.py → todas as funções
    infrastructure/repositories/pessoa_repository.py      → buscar_por_id()
"""
from infrastructure.repositories import atendimento_repository, pessoa_repository
from domain.models import Atendimento


STATUS_PERMITIDOS = ["aberto", "em andamento", "finalizado"]


def registrar_atendimento(pessoa_id, descricao):
    """Valida e registra um novo atendimento para uma pessoa.

    Regras:
        - A pessoa informada deve existir no banco.
        - A descrição não pode ser vazia ou apenas espaços.
        - Todo atendimento é criado com status 'aberto'.

    Args:
        pessoa_id : ID da pessoa a ser atendida.
        descricao : Descrição do atendimento.

    Returns:
        (True,  mensagem) em caso de sucesso.
        (False, mensagem) se a pessoa não existir ou a descrição for inválida.
    """
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
    """Retorna todos os atendimentos com o nome da pessoa incluso.

    Returns:
        Lista de objetos Atendimento (com pessoa_nome preenchido),
        ordenada por ID decrescente (mais recente primeiro).
    """
    return atendimento_repository.listar_todos()


def atualizar_status_atendimento(atendimento_id, novo_status):
    """Atualiza o status de um atendimento existente.

    Regra: o novo status deve ser um dos valores permitidos:
    'aberto', 'em andamento' ou 'finalizado'.

    Args:
        atendimento_id : ID do atendimento a atualizar.
        novo_status    : Novo valor do status.

    Returns:
        (True,  mensagem) em caso de sucesso.
        (False, mensagem) se o status for inválido ou o atendimento não existir.
    """
    if novo_status not in STATUS_PERMITIDOS:
        return False, "Status inválido."

    atualizado = atendimento_repository.atualizar_status(atendimento_id, novo_status)

    if not atualizado:
        return False, "Atendimento não encontrado."

    return True, "Status atualizado com sucesso."
