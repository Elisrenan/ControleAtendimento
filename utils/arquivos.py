"""Utilitários para leitura e escrita de arquivos JSON.

Funções genéricas de serialização usadas pela camada de UI para exportar
dados. Não dependem de nenhuma camada de domínio ou infraestrutura.
"""

import json
from pathlib import Path
from typing import Any


def salvar_json(nome_arquivo: str, dados: list[dict[str, Any]]) -> None:
    """Serializa ``dados`` e grava no arquivo informado (sobrescreve se existir).

    Args:
        nome_arquivo: Caminho completo do arquivo de destino.
        dados: Lista de dicionários a serem serializados.

    Example:
        >>> import tempfile, os
        >>> with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        ...     path = f.name
        >>> salvar_json(path, [{"id": 1, "nome": "Ana"}])
        >>> os.unlink(path)
    """
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def carregar_json(nome_arquivo: str) -> list[dict[str, Any]]:
    """Lê e desserializa um arquivo JSON.

    Retorna lista vazia se o arquivo não existir ou estiver corrompido,
    evitando exceções em chamadas de inicialização.

    Args:
        nome_arquivo: Caminho completo do arquivo a ser lido.

    Returns:
        Lista de dicionários lida do arquivo, ou ``[]`` em caso de ausência
        ou conteúdo inválido.

    Example:
        >>> carregar_json("/caminho/inexistente.json")
        []
    """
    caminho = Path(nome_arquivo)

    if not caminho.exists():
        return []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []

