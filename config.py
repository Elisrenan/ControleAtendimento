"""
Configurações globais da aplicação.

Centraliza constantes e caminhos usados em todas as camadas,
evitando valores mágicos espalhados pelo código.
"""

from pathlib import Path

# Raiz do projeto (diretório onde este arquivo está)
BASE_DIR: Path = Path(__file__).parent

# Caminho do banco de dados SQLite
DB_PATH: str = str(BASE_DIR / "controle_atendimentos.db")

# Status permitidos para atendimentos (em ordem de progressão)
STATUS_PERMITIDOS: list[str] = ["aberto", "em andamento", "finalizado"]

# Caminhos padrão dos arquivos de exportação JSON
EXPORT_PESSOAS_PATH: str = str(BASE_DIR / "pessoas.json")
EXPORT_ATENDIMENTOS_PATH: str = str(BASE_DIR / "atendimentos.json")
