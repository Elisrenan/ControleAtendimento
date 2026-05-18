from database import conectar


def cadastrar_pessoa(nome, cpf, telefone):
    if not nome.strip():
        return False, "O nome é obrigatório."

    if not cpf.strip():
        return False, "O CPF é obrigatório."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO pessoas (nome, cpf, telefone)
            VALUES (?, ?, ?)
        """, (nome, cpf, telefone))

        conexao.commit()
        return True, "Pessoa cadastrada com sucesso."

    except Exception as erro:
        return False, f"Erro ao cadastrar pessoa: {erro}"

    finally:
        conexao.close()


def listar_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, telefone
        FROM pessoas
        ORDER BY nome
    """)

    pessoas = cursor.fetchall()
    conexao.close()

    return pessoas


def buscar_pessoa_por_nome_ou_cpf(termo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, telefone
        FROM pessoas
        WHERE nome LIKE ? OR cpf LIKE ?
        ORDER BY nome
    """, (f"%{termo}%", f"%{termo}%"))

    pessoas = cursor.fetchall()
    conexao.close()

    return pessoas


def buscar_pessoa_por_id(pessoa_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, telefone
        FROM pessoas
        WHERE id = ?
    """, (pessoa_id,))

    pessoa = cursor.fetchone()
    conexao.close()

    return pessoa


def excluir_pessoa(pessoa_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM atendimentos
        WHERE pessoa_id = ? AND status = 'aberto'
    """, (pessoa_id,))

    total_abertos = cursor.fetchone()[0]

    if total_abertos > 0:
        conexao.close()
        return False, "Não é possível excluir pessoa com atendimento aberto."

    cursor.execute("""
        DELETE FROM pessoas
        WHERE id = ?
    """, (pessoa_id,))

    conexao.commit()
    conexao.close()

    return True, "Pessoa excluída com sucesso."