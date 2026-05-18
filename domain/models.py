"""
Camada de Domínio — entidades do sistema.

Este módulo não possui nenhuma dependência externa.
Todos os dados trafegam entre as camadas como objetos Pessoa ou Atendimento.

Usado por:
    infrastructure/repositories/pessoa_repository.py
    infrastructure/repositories/atendimento_repository.py
    services/pessoa_service.py
    services/atendimento_service.py
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pessoa:
    """
    Representa uma pessoa cadastrada no sistema.

    Atributos:
        nome     : Nome completo.
        cpf      : CPF — deve ser único no sistema.
        telefone : Telefone de contato (opcional).
        id       : Chave primária gerada pelo banco. None antes de ser inserida.
    """
    nome: str
    cpf: str
    telefone: str
    id: Optional[int] = field(default=None)


@dataclass
class Atendimento:
    """
    Representa um atendimento vinculado a uma Pessoa.

    Atributos:
        pessoa_id   : ID da pessoa atendida (chave estrangeira).
        descricao   : Descrição do atendimento.
        status      : Estado atual — 'aberto', 'em andamento' ou 'finalizado'.
        id          : Chave primária gerada pelo banco. None antes de ser inserido.
        pessoa_nome : Nome da pessoa — preenchido apenas em consultas com JOIN.
    """
    pessoa_id: int
    descricao: str
    status: str
    id: Optional[int] = field(default=None)
    pessoa_nome: Optional[str] = field(default=None)
