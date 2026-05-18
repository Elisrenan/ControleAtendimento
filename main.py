from database import criar_tabelas
from pessoa_service import (
    cadastrar_pessoa,
    listar_pessoas,
    buscar_pessoa_por_nome_ou_cpf,
    excluir_pessoa
)
from atendimento_service import (
    registrar_atendimento,
    listar_atendimentos,
    atualizar_status_atendimento
)
from arquivos import salvar_json


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
        print(f"ID: {pessoa[0]} | Nome: {pessoa[1]} | CPF: {pessoa[2]} | Telefone: {pessoa[3]}")


def imprimir_atendimentos(atendimentos):
    if not atendimentos:
        print("Nenhum atendimento encontrado.")
        return

    for atendimento in atendimentos:
        print(
            f"ID: {atendimento[0]} | Pessoa: {atendimento[1]} | "
            f"Descrição: {atendimento[2]} | Status: {atendimento[3]}"
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
            "3": "finalizado"
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
        {
            "id": pessoa[0],
            "nome": pessoa[1],
            "cpf": pessoa[2],
            "telefone": pessoa[3]
        }
        for pessoa in pessoas
    ]

    atendimentos_json = [
        {
            "id": atendimento[0],
            "pessoa": atendimento[1],
            "descricao": atendimento[2],
            "status": atendimento[3]
        }
        for atendimento in atendimentos
    ]

    salvar_json("pessoas.json", pessoas_json)
    salvar_json("atendimentos.json", atendimentos_json)

    print("Dados exportados para JSON com sucesso.")


def executar():
    criar_tabelas()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cadastrar_pessoa()
        elif opcao == "2":
            menu_listar_pessoas()
        elif opcao == "3":
            menu_buscar_pessoa()
        elif opcao == "4":
            menu_registrar_atendimento()
        elif opcao == "5":
            menu_listar_atendimentos()
        elif opcao == "6":
            menu_atualizar_status()
        elif opcao == "7":
            menu_excluir_pessoa()
        elif opcao == "8":
            menu_exportar_json()
        elif opcao == "9":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    executar()