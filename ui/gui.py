import tkinter as tk
from tkinter import messagebox

from database import criar_tabelas
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


def iniciar_gui():
    criar_tabelas()

    janela = tk.Tk()
    janela.title("Sistema RAD de Controle de Atendimentos")
    janela.geometry("1000x650")

    tk.Label(
        janela,
        text="Sistema RAD de Controle de Atendimentos",
        font=("Arial", 18, "bold"),
    ).pack(pady=10)

    # =========================================================
    # LISTA DE RESULTADOS (declarada antes das funções auxiliares)
    # =========================================================
    frame_resultados = tk.LabelFrame(janela, text="Resultados", padx=10, pady=10)

    lista_resultados = tk.Listbox(frame_resultados, width=150, height=20)

    # =========================================================
    # FUNÇÕES AUXILIARES
    # =========================================================
    def limpar_lista():
        lista_resultados.delete(0, tk.END)

    def exibir_pessoas():
        limpar_lista()
        pessoas = listar_pessoas()

        if not pessoas:
            lista_resultados.insert(tk.END, "Nenhuma pessoa cadastrada.")
            return

        for pessoa in pessoas:
            lista_resultados.insert(
                tk.END,
                f"Pessoa | ID: {pessoa[0]} | Nome: {pessoa[1]} | "
                f"CPF: {pessoa[2]} | Telefone: {pessoa[3]}",
            )

    def exibir_atendimentos():
        limpar_lista()
        atendimentos = listar_atendimentos()

        if not atendimentos:
            lista_resultados.insert(tk.END, "Nenhum atendimento encontrado.")
            return

        for atendimento in atendimentos:
            lista_resultados.insert(
                tk.END,
                f"Atendimento | ID: {atendimento[0]} | Pessoa: {atendimento[1]} | "
                f"Descrição: {atendimento[2]} | Status: {atendimento[3]}",
            )

    # =========================================================
    # AÇÕES
    # =========================================================
    def acao_cadastrar_pessoa():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()

        sucesso, mensagem = cadastrar_pessoa(nome, cpf, telefone)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            entry_nome.delete(0, tk.END)
            entry_cpf.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            exibir_pessoas()
        else:
            messagebox.showerror("Erro", mensagem)

    def acao_buscar_pessoa():
        termo = entry_busca.get()
        pessoas = buscar_pessoa_por_nome_ou_cpf(termo)
        limpar_lista()

        if not pessoas:
            lista_resultados.insert(tk.END, "Nenhum resultado encontrado.")
            return

        for pessoa in pessoas:
            lista_resultados.insert(
                tk.END,
                f"Pessoa | ID: {pessoa[0]} | Nome: {pessoa[1]} | "
                f"CPF: {pessoa[2]} | Telefone: {pessoa[3]}",
            )

    def acao_excluir_pessoa():
        try:
            pessoa_id = int(entry_excluir_id.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return

        sucesso, mensagem = excluir_pessoa(pessoa_id)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            entry_excluir_id.delete(0, tk.END)
            exibir_pessoas()
        else:
            messagebox.showerror("Erro", mensagem)

    def acao_registrar_atendimento():
        try:
            pessoa_id = int(entry_pessoa_id.get())
        except ValueError:
            messagebox.showerror("Erro", "ID da pessoa inválido.")
            return

        descricao = entry_descricao.get()
        sucesso, mensagem = registrar_atendimento(pessoa_id, descricao)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            entry_pessoa_id.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            exibir_atendimentos()
        else:
            messagebox.showerror("Erro", mensagem)

    def acao_atualizar_status():
        try:
            atendimento_id = int(entry_atendimento_id.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do atendimento inválido.")
            return

        novo_status = status_var.get()
        sucesso, mensagem = atualizar_status_atendimento(atendimento_id, novo_status)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            entry_atendimento_id.delete(0, tk.END)
            exibir_atendimentos()
        else:
            messagebox.showerror("Erro", mensagem)

    # =========================================================
    # FRAME CADASTRO DE PESSOA
    # =========================================================
    frame_pessoa = tk.LabelFrame(janela, text="Cadastro de Pessoa", padx=10, pady=10)
    frame_pessoa.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_pessoa, text="Nome").grid(row=0, column=0)
    entry_nome = tk.Entry(frame_pessoa, width=30)
    entry_nome.grid(row=0, column=1, padx=5)

    tk.Label(frame_pessoa, text="CPF").grid(row=0, column=2)
    entry_cpf = tk.Entry(frame_pessoa, width=20)
    entry_cpf.grid(row=0, column=3, padx=5)

    tk.Label(frame_pessoa, text="Telefone").grid(row=0, column=4)
    entry_telefone = tk.Entry(frame_pessoa, width=20)
    entry_telefone.grid(row=0, column=5, padx=5)

    tk.Button(frame_pessoa, text="Cadastrar Pessoa", command=acao_cadastrar_pessoa).grid(
        row=0, column=6, padx=5
    )

    # =========================================================
    # FRAME BUSCA E EXCLUSÃO
    # =========================================================
    frame_busca = tk.LabelFrame(janela, text="Busca e Exclusão", padx=10, pady=10)
    frame_busca.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_busca, text="Nome ou CPF").grid(row=0, column=0)
    entry_busca = tk.Entry(frame_busca, width=30)
    entry_busca.grid(row=0, column=1, padx=5)

    tk.Button(frame_busca, text="Buscar", command=acao_buscar_pessoa).grid(row=0, column=2, padx=5)
    tk.Button(frame_busca, text="Listar Pessoas", command=exibir_pessoas).grid(row=0, column=3, padx=5)

    tk.Label(frame_busca, text="ID para excluir").grid(row=0, column=4)
    entry_excluir_id = tk.Entry(frame_busca, width=10)
    entry_excluir_id.grid(row=0, column=5, padx=5)

    tk.Button(frame_busca, text="Excluir Pessoa", command=acao_excluir_pessoa).grid(
        row=0, column=6, padx=5
    )

    # =========================================================
    # FRAME REGISTRO DE ATENDIMENTO
    # =========================================================
    frame_atendimento = tk.LabelFrame(janela, text="Registro de Atendimento", padx=10, pady=10)
    frame_atendimento.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_atendimento, text="ID Pessoa").grid(row=0, column=0)
    entry_pessoa_id = tk.Entry(frame_atendimento, width=10)
    entry_pessoa_id.grid(row=0, column=1, padx=5)

    tk.Label(frame_atendimento, text="Descrição").grid(row=0, column=2)
    entry_descricao = tk.Entry(frame_atendimento, width=50)
    entry_descricao.grid(row=0, column=3, padx=5)

    tk.Button(
        frame_atendimento, text="Registrar Atendimento", command=acao_registrar_atendimento
    ).grid(row=0, column=4, padx=5)

    tk.Button(
        frame_atendimento, text="Listar Atendimentos", command=exibir_atendimentos
    ).grid(row=0, column=5, padx=5)

    # =========================================================
    # FRAME ATUALIZAÇÃO DE STATUS
    # =========================================================
    frame_status = tk.LabelFrame(janela, text="Atualização de Status", padx=10, pady=10)
    frame_status.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_status, text="ID Atendimento").grid(row=0, column=0)
    entry_atendimento_id = tk.Entry(frame_status, width=10)
    entry_atendimento_id.grid(row=0, column=1, padx=5)

    status_var = tk.StringVar(value="aberto")

    tk.OptionMenu(frame_status, status_var, "aberto", "em andamento", "finalizado").grid(
        row=0, column=2, padx=5
    )

    tk.Button(frame_status, text="Atualizar Status", command=acao_atualizar_status).grid(
        row=0, column=3, padx=5
    )

    # =========================================================
    # FRAME RESULTADOS (empacotado aqui para ocupar o espaço restante)
    # =========================================================
    frame_resultados.pack(fill="both", expand=True, padx=10, pady=5)
    lista_resultados.pack(fill="both", expand=True)

    janela.mainloop()
