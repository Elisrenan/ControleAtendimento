"""Interface de terminal (CLI) do sistema de controle de atendimentos.

Responsável exclusivamente pela interação com o usuário via linha de comando.
Não contém lógica de negócio — delega todas as operações aos serviços injetados.
"""

from application.atendimento_service import AtendimentoService
from application.pessoa_service import PessoaService
from config import EXPORT_ATENDIMENTOS_PATH, EXPORT_PESSOAS_PATH
from utils.arquivos import salvar_json


# ------------------------------------------------------------------
# Exibição de menus e listas
# ------------------------------------------------------------------

def mostrar_menu() -> None:
    """Imprime o menu principal com as opções disponíveis."""
    print("\n===== Sistema RAD de Controle de Atendimentos =====")
    print("1 - Cadastrar pessoa")
    print("2 - Listar pessoas")
    print("3 - Buscar pessoa por nome ou CPF")
    print("4 - Registrar atendimento")
    print("5 - Listar atendimentos")
    print("6 - Atualizar status do atendimento")
    print("7 - Excluir pessoa")
    print("8 - Exportar dados para JSON")
    print("9 - Sair")


def imprimir_pessoas(pessoa_svc: PessoaService, pessoas: list) -> None:
    """Imprime a lista de pessoas formatada no terminal.

    Args:
        pessoa_svc: Serviço de pessoas (não utilizado diretamente aqui,
            mantido para coerência de assinatura das funções auxiliares).
        pessoas: Lista de instâncias ``Pessoa`` a serem exibidas.
    """
    if not pessoas:
        print("Nenhuma pessoa encontrada.")
        return

    for p in pessoas:
        print(f"ID: {p.id} | Nome: {p.nome} | CPF: {p.cpf} | Telefone: {p.telefone}")


def imprimir_atendimentos(atendimentos: list) -> None:
    """Imprime a lista de atendimentos formatada no terminal.

    Args:
        atendimentos: Lista de instâncias ``Atendimento`` a serem exibidas.
    """
    if not atendimentos:
        print("Nenhum atendimento encontrado.")
        return

    for a in atendimentos:
        print(
            f"ID: {a.id} | Pessoa: {a.nome_pessoa} | "
            f"Descrição: {a.descricao} | Status: {a.status.value}"
        )


# ------------------------------------------------------------------
# Ações do menu
# ------------------------------------------------------------------

def menu_cadastrar_pessoa(pessoa_svc: PessoaService) -> None:
    """Coleta dados via input e cadastra uma nova pessoa.

    Args:
        pessoa_svc: Serviço responsável pelo cadastro de pessoas.
    """
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    _, mensagem = pessoa_svc.cadastrar(nome, cpf, telefone)
    print(mensagem)


def menu_listar_pessoas(pessoa_svc: PessoaService) -> None:
    """Lista todas as pessoas cadastradas.

    Args:
        pessoa_svc: Serviço responsável pela listagem de pessoas.
    """
    imprimir_pessoas(pessoa_svc, pessoa_svc.listar())


def menu_buscar_pessoa(pessoa_svc: PessoaService) -> None:
    """Busca pessoas por nome ou CPF a partir de um termo digitado.

    Args:
        pessoa_svc: Serviço responsável pela busca de pessoas.
    """
    termo = input("Digite nome ou CPF: ")
    imprimir_pessoas(pessoa_svc, pessoa_svc.buscar(termo))


def menu_registrar_atendimento(atendimento_svc: AtendimentoService) -> None:
    """Coleta dados via input e registra um novo atendimento.

    Args:
        atendimento_svc: Serviço responsável pelo registro de atendimentos.
    """
    try:
        pessoa_id = int(input("ID da pessoa: "))
    except ValueError:
        print("ID inválido.")
        return

    descricao = input("Descrição do atendimento: ")
    _, mensagem = atendimento_svc.registrar(pessoa_id, descricao)
    print(mensagem)


def menu_listar_atendimentos(atendimento_svc: AtendimentoService) -> None:
    """Lista todos os atendimentos registrados.

    Args:
        atendimento_svc: Serviço responsável pela listagem de atendimentos.
    """
    imprimir_atendimentos(atendimento_svc.listar())


def menu_atualizar_status(atendimento_svc: AtendimentoService) -> None:
    """Solicita ID e novo status via input e atualiza o atendimento.

    Args:
        atendimento_svc: Serviço responsável pela atualização de atendimentos.
    """
    try:
        atendimento_id = int(input("ID do atendimento: "))
    except ValueError:
        print("ID inválido.")
        return

    print("Status disponíveis:")
    print("1 - aberto")
    print("2 - em andamento")
    print("3 - finalizado")

    status_map = {"1": "aberto", "2": "em andamento", "3": "finalizado"}
    opcao = input("Escolha o novo status: ")
    novo_status = status_map.get(opcao)

    if novo_status is None:
        print("Opção inválida.")
        return

    _, mensagem = atendimento_svc.atualizar_status(atendimento_id, novo_status)
    print(mensagem)


def menu_excluir_pessoa(pessoa_svc: PessoaService) -> None:
    """Solicita o ID via input e remove a pessoa.

    Args:
        pessoa_svc: Serviço responsável pela exclusão de pessoas.
    """
    try:
        pessoa_id = int(input("ID da pessoa que deseja excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    _, mensagem = pessoa_svc.excluir(pessoa_id)
    print(mensagem)


def menu_exportar_json(
    pessoa_svc: PessoaService, atendimento_svc: AtendimentoService
) -> None:
    """Exporta pessoas e atendimentos para arquivos JSON.

    Args:
        pessoa_svc: Serviço responsável pela listagem de pessoas.
        atendimento_svc: Serviço responsável pela listagem de atendimentos.
    """
    pessoas_json = [
        {"id": p.id, "nome": p.nome, "cpf": p.cpf, "telefone": p.telefone}
        for p in pessoa_svc.listar()
    ]
    atendimentos_json = [
        {"id": a.id, "pessoa": a.nome_pessoa, "descricao": a.descricao, "status": a.status.value}
        for a in atendimento_svc.listar()
    ]

    salvar_json(EXPORT_PESSOAS_PATH, pessoas_json)
    salvar_json(EXPORT_ATENDIMENTOS_PATH, atendimentos_json)
    print("Dados exportados para JSON com sucesso.")


# ------------------------------------------------------------------
# Ponto de entrada da CLI
# ------------------------------------------------------------------

def executar(pessoa_svc: PessoaService, atendimento_svc: AtendimentoService) -> None:
    """Inicia o loop principal da interface de terminal.

    Exibe o menu, lê a opção do usuário e despacha para a função correspondente.
    O banco de dados já deve estar inicializado antes de chamar esta função
    (responsabilidade do ``container.criar_container``).

    Args:
        pessoa_svc: Serviço de pessoas pronto para uso.
        atendimento_svc: Serviço de atendimentos pronto para uso.
    """
    opcoes = {
        "1": lambda: menu_cadastrar_pessoa(pessoa_svc),
        "2": lambda: menu_listar_pessoas(pessoa_svc),
        "3": lambda: menu_buscar_pessoa(pessoa_svc),
        "4": lambda: menu_registrar_atendimento(atendimento_svc),
        "5": lambda: menu_listar_atendimentos(atendimento_svc),
        "6": lambda: menu_atualizar_status(atendimento_svc),
        "7": lambda: menu_excluir_pessoa(pessoa_svc),
        "8": lambda: menu_exportar_json(pessoa_svc, atendimento_svc),
    }

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "9":
            print("Sistema encerrado.")
            break

        acao = opcoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida.")
