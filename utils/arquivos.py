import json
from pathlib import Path


def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def carregar_json(nome_arquivo):
    caminho = Path(nome_arquivo)

    if not caminho.exists():
        return []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []
