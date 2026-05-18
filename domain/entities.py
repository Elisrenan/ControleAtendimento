"""Entidades de domínio da aplicação.

Define os modelos de dados puros (sem lógica de persistência)
usados em todas as camadas. Seguindo Clean Architecture, esta
camada não depende de nada externo — apenas da stdlib Python.
"""

from dataclasses import dataclass, field
from enum import Enum


class StatusAtendimento(str, Enum):
    """Representa os estados possíveis de um atendimento.

    Herda de ``str`` para serialização direta em JSON/SQL sem
    conversão manual.

    Attributes:
        ABERTO: Atendimento recém-criado, ainda não iniciado.
        EM_ANDAMENTO: Atendimento em progresso.
        FINALIZADO: Atendimento concluído.
    """

    ABERTO = "aberto"
    EM_ANDAMENTO = "em andamento"
    FINALIZADO = "finalizado"


@dataclass
class Pessoa:
    """Representa uma pessoa cadastrada no sistema.

    Attributes:
        nome: Nome completo da pessoa.
        cpf: CPF da pessoa (string livre — validação no serviço).
        telefone: Telefone de contato (opcional).
        id: Identificador único gerado pelo banco. ``None`` antes
            de ser persistido.

    Example:
        >>> p = Pessoa(nome="João Silva", cpf="000.000.000-00", telefone="(11) 99999-9999")
        >>> p.id is None
        True
    """

    nome: str
    cpf: str
    telefone: str = ""
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        """Garante que os campos de texto sejam normalizados após criação."""
        self.nome = self.nome.strip()
        self.cpf = self.cpf.strip()
        self.telefone = self.telefone.strip() if self.telefone else ""


@dataclass
class Atendimento:
    """Representa um atendimento vinculado a uma pessoa.

    Attributes:
        pessoa_id: ID da pessoa atendida (FK para ``Pessoa.id``).
        descricao: Descrição detalhada do atendimento.
        status: Estado atual do atendimento (padrão: ``ABERTO``).
        id: Identificador único gerado pelo banco. ``None`` antes
            de ser persistido.
        nome_pessoa: Nome da pessoa atendida (preenchido por JOIN,
            não persistido).

    Example:
        >>> a = Atendimento(pessoa_id=1, descricao="Suporte técnico")
        >>> a.status
        <StatusAtendimento.ABERTO: 'aberto'>
    """

    pessoa_id: int
    descricao: str
    status: StatusAtendimento = field(default=StatusAtendimento.ABERTO)
    id: int | None = field(default=None)
    nome_pessoa: str = field(default="", compare=False)

    def __post_init__(self) -> None:
        """Normaliza a descrição e converte status string para enum, se necessário."""
        self.descricao = self.descricao.strip()
        if isinstance(self.status, str):
            self.status = StatusAtendimento(self.status)
