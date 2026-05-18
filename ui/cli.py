from infrastructure.database import criar_tabelas
from services.pessoa_service import (
    cadastrar_pessoa,
    listar_pessoas,
    buscar_pessoa_por_nome_ou_cpf,
    excluir_pessoa,
)
from services.atendimento_service import (
    registrar_atendimento,
    listar_atendimentos,
    atualizar_status_atendimento,
)
from utils.arquivos import salvar_json


def mostrar_menu():
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


def imprimir_pessoas(pessoas):
    if not pessoas:
        print("Nenhuma pessoa encontrada.")
        return

    for pessoa in pessoas:
        print(f"ID: {pessoa.id} | Nome: {pessoa.nome} | CPF: {pessoa.cpf} | Telefone: {pessoa.telefone}")


def imprimir_atendimentos(atendimentos):
    if not atendimentos:
        print("Nenhum atendimento encontrado.")
        return

    for atendimento in atendimentos:
        print(
            f"ID: {atendimento.id} | Pessoa: {atendimento.pessoa_nome} | "
            f"Descrição: {atendimento.descricao} | Status: {atendimento.status}"
        )


def menu_cadastrar_pessoa():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    sucesso, mensagem = cadastrar_pessoa(nome, cpf, telefone)
    print(mensagem)


def menu_listar_pessoas():
    pessoas = listar_pessoas()
    imprimir_pessoas(pessoas)


def menu_buscar_pessoa():
    termo = input("Digite nome ou CPF: ")
    pessoas = buscar_pessoa_por_nome_ou_cpf(termo)
    imprimir_pessoas(pessoas)


def menu_registrar_atendimento():
    try:
        pessoa_id = int(input("ID da pessoa: "))
        descricao = input("Descrição do atendimento: ")

        sucesso, mensagem = registrar_atendimento(pessoa_id, descricao)
        print(mensagem)

    except ValueError:
        print("ID inválido.")


def menu_listar_atendimentos():
    atendimentos = listar_atendimentos()
    imprimir_atendimentos(atendimentos)


def menu_atualizar_status():
    try:
        atendimento_id = int(input("ID do atendimento: "))

        print("Status disponíveis:")
        print("1 - aberto")
        print("2 - em andamento")
        print("3 - finalizado")

        opcao = input("Escolha o novo status: ")

        status_map = {
            "1": "aberto",
            "2": "em andamento",
            "3": "finalizado",
        }

        novo_status = status_map.get(opcao)

        if novo_status is None:
            print("Opção inválida.")
            return

        sucesso, mensagem = atualizar_status_atendimento(atendimento_id, novo_status)
        print(mensagem)

    except ValueError:
        print("ID inválido.")


def menu_excluir_pessoa():
    try:
        pessoa_id = int(input("ID da pessoa que deseja excluir: "))
        sucesso, mensagem = excluir_pessoa(pessoa_id)
        print(mensagem)

    except ValueError:
        print("ID inválido.")


def menu_exportar_json():
    pessoas = listar_pessoas()
    atendimentos = listar_atendimentos()

    pessoas_json = [
        {"id": p.id, "nome": p.nome, "cpf": p.cpf, "telefone": p.telefone}
        for p in pessoas
    ]

    atendimentos_json = [
        {"id": a.id, "pessoa": a.pessoa_nome, "descricao": a.descricao, "status": a.status}
        for a in atendimentos
    ]

    salvar_json("pessoas.json", pessoas_json)
    salvar_json("atendimentos.json", atendimentos_json)

    print("Dados exportados para JSON com sucesso.")


def executar():
    criar_tabelas()

    opcoes = {
        "1": menu_cadastrar_pessoa,
        "2": menu_listar_pessoas,
        "3": menu_buscar_pessoa,
        "4": menu_registrar_atendimento,
        "5": menu_listar_atendimentos,
        "6": menu_atualizar_status,
        "7": menu_excluir_pessoa,
        "8": menu_exportar_json,
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
