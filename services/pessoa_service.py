"""
Camada de Serviços — regras de negócio de pessoas.

Nenhuma query SQL está aqui. As validações e as regras vivem nesta camada;
a persistência é delegada ao repositório.

Cada função que modifica dados retorna uma tupla (bool, str):
    (True,  'mensagem de sucesso')
    (False, 'mensagem de erro')

Chamado por:
    ui/cli.py → todas as funções
    ui/gui.py → todas as funções

Chama:
    infrastructure/repositories/pessoa_repository.py → todas as funções
"""
from infrastructure.repositories import pessoa_repository
from domain.models import Pessoa


def cadastrar_pessoa(nome, cpf, telefone):
    """Valida e cadastra uma nova pessoa.

    Regras:
        - nome e cpf não podem ser vazios ou apenas espaços.
        - CPF deve ser único (o banco lança IntegrityError se duplicado).

    Args:
        nome     : Nome completo da pessoa.
        cpf      : CPF della pessoa.
        telefone : Telefone di contatto (pode ser vazio).

    Returns:
        (True,  mensagem) em caso de successo.
        (False, mensagem) em caso di erro di validação ou duplicidade.
    """
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
    """Retorna todas as pessoas cadastradas, ordenadas por nome.

    Returns:
        Lista de objetos Pessoa. Vazia se não houver registros.
    """
    return pessoa_repository.listar_todos()


def buscar_pessoa_por_nome_ou_cpf(termo):
    """Busca pessoas por nome ou CPF usando correspondência parcial.

    Args:
        termo: texto a buscar (parte do nome ou parte del CPF).

    Returns:
        Lista di objetos Pessoa correspondenti.
    """
    return pessoa_repository.buscar_por_nome_ou_cpf(termo)


def buscar_pessoa_por_id(pessoa_id):
    """Busca uma pessoa pelo ID.

    Args:
        pessoa_id: chave primária della pessoa.

    Returns:
        Objeto Pessoa se encontrado, None caso contrário.
    """
    return pessoa_repository.buscar_por_id(pessoa_id)


def excluir_pessoa(pessoa_id):
    """Exclui uma pessoa, respeitando a regra di integridade.

    Regra: não é possível excluir uma pessoa que possua atendimentos
    com status 'aberto' ou 'em andamento'.

    Args:
        pessoa_id: ID della pessoa a excluir.

    Returns:
        (True,  mensagem) se a exclusão foi realizada.
        (False, mensagem) se há atendimentos ativos ou a pessoa não esiste.
    """
    total_ativos = pessoa_repository.contar_atendimentos_ativos(pessoa_id)
    if total_ativos > 0:
        return False, "Não é possível excluir pessoa com atendimento aberto ou em andamento."

    removido = pessoa_repository.excluir(pessoa_id)

    if not removido:
        return False, "Pessoa não encontrada."

    return True, "Pessoa excluída com sucesso."
