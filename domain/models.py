from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pessoa:
    nome: str
    cpf: str
    telefone: str
    id: Optional[int] = field(default=None)


@dataclass
class Atendimento:
    pessoa_id: int
    descricao: str
    status: str
    id: Optional[int] = field(default=None)
    pessoa_nome: Optional[str] = field(default=None)
