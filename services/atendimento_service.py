from database import conectar
from .pessoa_service import buscar_pessoa_por_id


STATUS_PERMITIDOS = ["aberto", "em andamento", "finalizado"]


def registrar_atendimento(pessoa_id, descricao):
    pessoa = buscar_pessoa_por_id(pessoa_id)

    if pessoa is None:
        return False, "Pessoa não encontrada."

    if not descricao.strip():
        return False, "A descrição do atendimento é obrigatória."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO atendimentos (pessoa_id, descricao, status)
            VALUES (?, ?, ?)
        """, (pessoa_id, descricao, "aberto"))

        conexao.commit()
        return True, "Atendimento registrado com sucesso."

    except Exception as erro:
        return False, f"Erro ao registrar atendimento: {erro}"

    finally:
        conexao.close()


def listar_atendimentos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            atendimentos.id,
            pessoas.nome,
            atendimentos.descricao,
            atendimentos.status
        FROM atendimentos
        INNER JOIN pessoas
            ON pessoas.id = atendimentos.pessoa_id
        ORDER BY atendimentos.id DESC
    """)

    atendimentos = cursor.fetchall()
    conexao.close()

    return atendimentos


def atualizar_status_atendimento(atendimento_id, novo_status):
    if novo_status not in STATUS_PERMITIDOS:
        return False, "Status inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE atendimentos
        SET status = ?
        WHERE id = ?
    """, (novo_status, atendimento_id))

    if cursor.rowcount == 0:
        conexao.close()
        return False, "Atendimento não encontrado."

    conexao.commit()
    conexao.close()

    return True, "Status atualizado com sucesso."
