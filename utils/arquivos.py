"""
Utilidades de arquivos — leitura e escrita em JSON.

Chamado por:
    ui/cli.py → salvar_json()
"""
import json


def salvar_json(nome_arquivo, dados):
    """Serializa uma lista de dicionários e grava no disco em formato JSON.

    O arquivo é criado ou sobrescrito se já existir.
    Caracteres especiais (acentos) são preservados (ensure_ascii=False).

    Args:
        nome_arquivo : Caminho/nome do arquivo de saída (ex.: 'pessoas.json').
        dados        : Lista de dicionários a serializar.
    """
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
