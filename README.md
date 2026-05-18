# Sistema de Controle de Atendimentos

Sistema em Python nativo para cadastro de pessoas e gerenciamento de atendimentos, com suporte a interface de terminal (CLI) e interface gráfica (GUI).

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Funcionalidades](#2-funcionalidades)
3. [Arquitetura](#3-arquitetura)
4. [Estrutura do Projeto](#4-estrutura-do-projeto)
5. [Pré-requisitos](#5-pré-requisitos)
6. [Como Executar](#6-como-executar)
7. [Como Rodar os Testes](#7-como-rodar-os-testes)
8. [Como Replicar em Outro Projeto](#8-como-replicar-em-outro-projeto)
9. [Camadas da Aplicação](#9-camadas-da-aplicação)
10. [Banco de Dados](#10-banco-de-dados)
11. [Princípios SOLID Aplicados](#11-princípios-solid-aplicados)

---

## 1. Visão Geral

Projeto desenvolvido na disciplina de Desenvolvimento Rápido de Aplicações (RAD) com Python.  
Demonstra na prática a organização de um sistema seguindo **Clean Architecture** e os princípios **SOLID**, com separação total entre regras de negócio, persistência e interface com o usuário.

---

## 2. Funcionalidades

| Módulo | Funcionalidade |
|---|---|
| Pessoas | Cadastrar, listar, buscar por nome ou CPF, excluir |
| Atendimentos | Registrar, listar, atualizar status |
| Exportação | Exportar pessoas e atendimentos para JSON |
| Interface | Terminal (CLI) e Interface Gráfica (Tkinter) |

---

## 3. Arquitetura

O projeto segue **Clean Architecture** com 4 camadas concêntricas.  
A regra de ouro: **dependências apontam sempre para dentro** (nunca o domínio depende da infraestrutura).

```
┌──────────────────────────────────────────────────────┐
│                   UI (Apresentação)                  │
│              ui/cli.py  ·  ui/gui.py                 │
├──────────────────────────────────────────────────────┤
│              Application (Casos de Uso)              │
│  application/pessoa_service.py                       │
│  application/atendimento_service.py                  │
├──────────────────────────────────────────────────────┤
│                  Domain (Núcleo)                     │
│  domain/entities.py   (Pessoa, Atendimento, Enum)    │
│  domain/repositories.py  (Interfaces ABC)            │
├──────────────────────────────────────────────────────┤
│             Infrastructure (Persistência)            │
│  infrastructure/database.py                          │
│  infrastructure/repositories/pessoa_repository.py   │
│  infrastructure/repositories/atendimento_repository │
└──────────────────────────────────────────────────────┘
           ↑ container.py monta as dependências ↑
```

A cola entre as camadas é o `container.py`, que instancia os repositórios concretos e os injeta nos serviços (Dependency Injection manual, sem framework).

---

## 4. Estrutura do Projeto

```text
ControleAtendimento/
│
├── main.py                            # Ponto de entrada da aplicação
├── config.py                          # Constantes: DB_PATH, STATUS_PERMITIDOS, exports
├── container.py                       # Montagem de dependências (DI)
│
├── domain/
│   ├── __init__.py
│   ├── entities.py                    # @dataclass Pessoa, Atendimento; Enum StatusAtendimento
│   └── repositories.py               # ABC IPessoaRepository, IAtendimentoRepository
│
├── infrastructure/
│   ├── __init__.py
│   ├── database.py                    # get_connection(), init_db()
│   └── repositories/
│       ├── __init__.py
│       ├── pessoa_repository.py       # SQLitePessoaRepository
│       └── atendimento_repository.py  # SQLiteAtendimentoRepository
│
├── application/
│   ├── __init__.py
│   ├── pessoa_service.py              # PessoaService (casos de uso de pessoas)
│   └── atendimento_service.py        # AtendimentoService (casos de uso de atendimentos)
│
├── ui/
│   ├── __init__.py
│   ├── cli.py                         # Interface de terminal
│   └── gui.py                         # Interface gráfica (Tkinter)
│
├── utils/
│   ├── __init__.py
│   └── arquivos.py                    # salvar_json(), carregar_json()
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures + FakeRepositories (in-memory)
│   ├── test_domain.py                 # Testes das entidades e enum
│   ├── test_pessoa_service.py         # Testes unitários do PessoaService
│   ├── test_atendimento_service.py    # Testes unitários do AtendimentoService
│   └── test_repositories.py          # Testes de integração dos repositórios SQLite
│
├── requirements-dev.txt               # Dependências de desenvolvimento (pytest)
├── controle_atendimentos.db           # Banco SQLite (gerado na primeira execução)
└── README.md
```

---

## 5. Pré-requisitos

- **Python 3.10+** (para uso de `int | None` e `list[str]` sem `from __future__ import annotations`)
- Nenhuma dependência de produção — apenas bibliotecas da stdlib:
  - `sqlite3`, `tkinter`, `json`, `pathlib`, `abc`, `dataclasses`, `enum`
- Para desenvolvimento e testes:
  - `pytest` (veja [Como Rodar os Testes](#7-como-rodar-os-testes))

---

## 6. Como Executar

```bash
# Clonar o repositório
git clone https://github.com/Elisrenan/ControleAtendimento.git
cd ControleAtendimento

# Interface de terminal (padrão)
python main.py

# Interface gráfica (Tkinter)
python main.py --gui
```

O banco de dados `controle_atendimentos.db` é criado automaticamente na primeira execução.

---

## 7. Como Rodar os Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Rodar todos os testes
pytest tests/ -v

# Rodar com relatório de cobertura (requer pytest-cov)
pip install pytest-cov
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Estratégia de Testes

| Arquivo | Tipo | Estratégia |
|---|---|---|
| `test_domain.py` | Unitário | Sem I/O — testa entidades e enum isoladamente |
| `test_pessoa_service.py` | Unitário | `FakePessoaRepository` em memória — sem banco |
| `test_atendimento_service.py` | Unitário | `FakeAtendimentoRepository` em memória — sem banco |
| `test_repositories.py` | Integração | SQLite em arquivo temporário (`tmp_path` do pytest) |

---

## 8. Como Replicar em Outro Projeto

Siga os passos abaixo para usar a mesma arquitetura em um novo sistema:

### Passo 1 — Crie as entidades de domínio
Em `domain/entities.py`, defina seus modelos como `@dataclass` sem imports externos.

### Passo 2 — Defina os contratos de repositório
Em `domain/repositories.py`, crie ABCs com `abc.ABC` + `abc.abstractmethod` para cada entidade.

### Passo 3 — Implemente os repositórios
Em `infrastructure/repositories/`, crie uma classe que herde da ABC e implemente cada método em SQL (ou outro banco).

### Passo 4 — Crie os serviços
Em `application/`, crie classes que recebam o repositório no `__init__` e implementem os casos de uso.

### Passo 5 — Monte as dependências
Em `container.py`, instancie os repositórios concretos e injete nos serviços.

### Passo 6 — Conecte a UI
Em `ui/`, receba os serviços como parâmetro. A UI não conhece banco de dados.

### Passo 7 — Adicione testes
Em `tests/conftest.py`, crie `FakeRepository` em memória para testes unitários rápidos.

---

## 9. Camadas da Aplicação

### `domain/` — Núcleo (sem dependências externas)
- **`entities.py`**: `Pessoa`, `Atendimento` (dataclasses) e `StatusAtendimento` (Enum).  
  Nenhuma camada pode ignorar esses contratos.
- **`repositories.py`**: Interfaces ABCs `IPessoaRepository` e `IAtendimentoRepository`.  
  Definem *o quê* pode ser feito com os dados, mas não *como*.

### `infrastructure/` — Implementações Concretas
- **`database.py`**: Único arquivo que importa `sqlite3`. Gerencia conexão e inicialização do banco.
- **`repositories/`**: Implementações SQLite das interfaces de domínio.

### `application/` — Regras de Negócio
- **`pessoa_service.py`**: Orquestra cadastro, busca e exclusão de pessoas com validações.
- **`atendimento_service.py`**: Orquestra registro e atualização de atendimentos.

### `container.py` — Ponto de Composição
Instancia repositórios concretos e os injeta nos serviços. É o único arquivo que conhece ambas as camadas `application` e `infrastructure` simultaneamente.

### `ui/` — Interface com o Usuário
Recebe os serviços prontos como parâmetro. Não faz acesso direto ao banco.

---

## 10. Banco de Dados

```sql
-- Tabela de pessoas
CREATE TABLE pessoas (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT    NOT NULL,
    cpf      TEXT    NOT NULL UNIQUE,
    telefone TEXT    NOT NULL DEFAULT ''
);

-- Tabela de atendimentos
CREATE TABLE atendimentos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    pessoa_id INTEGER NOT NULL,
    descricao TEXT    NOT NULL,
    status    TEXT    NOT NULL DEFAULT 'aberto',
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);
```

---

## 11. Princípios SOLID Aplicados

| Princípio | Onde é aplicado |
|---|---|
| **S** — Single Responsibility | Cada classe/módulo tem uma única razão para mudar: `SQLitePessoaRepository` só persiste; `PessoaService` só orquestra regras |
| **O** — Open/Closed | Para trocar SQLite por PostgreSQL, basta criar `PostgresPessoaRepository` sem alterar `PessoaService` |
| **L** — Liskov Substitution | `FakePessoaRepository` substitui `SQLitePessoaRepository` nos testes sem quebrar nenhum serviço |
| **I** — Interface Segregation | `IPessoaRepository` e `IAtendimentoRepository` são interfaces específicas — nenhuma classe é forçada a implementar métodos que não usa |
| **D** — Dependency Inversion | `PessoaService` depende de `IPessoaRepository` (abstração), não de `SQLitePessoaRepository` (implementação concreta) |


---

## 1. Visão Geral

Projeto desenvolvido na disciplina de Desenvolvimento Rápido de Aplicações (RAD) com Python. Demonstra na prática a organização de um sistema em camadas, separando responsabilidades entre infraestrutura, serviços e interface com o usuário.

---

## 2. Funcionalidades

| Módulo | Funcionalidade |
|---|---|
| Pessoas | Cadastrar, listar, buscar por nome ou CPF, excluir |
| Atendimentos | Registrar, listar, atualizar status |
| Exportação | Exportar pessoas e atendimentos para JSON |
| Interface | Terminal (CLI) e Interface Gráfica (Tkinter) |

---

## 3. Arquitetura

O projeto segue uma arquitetura em camadas simples:

```
┌─────────────────────────────┐
│        UI (Apresentação)    │  ui/cli.py · ui/gui.py
├─────────────────────────────┤
│     Services (Negócio)      │  services/pessoa_service.py
│                             │  services/atendimento_service.py
├─────────────────────────────┤
│   Infrastructure (Dados)    │  database.py
├─────────────────────────────┤
│       Utils                 │  utils/arquivos.py
└─────────────────────────────┘
```

Cada camada depende apenas da camada imediatamente abaixo, sem dependências circulares.

---

## 4. Estrutura do Projeto

```text
ControleAtendimento/
│
├── main.py                        # Ponto de entrada da aplicação
├── database.py                    # Conexão e criação do banco SQLite
│
├── services/
│   ├── __init__.py
│   ├── pessoa_service.py          # Regras de negócio de pessoas
│   └── atendimento_service.py     # Regras de negócio de atendimentos
│
├── ui/
│   ├── __init__.py
│   ├── cli.py                     # Interface de terminal
│   └── gui.py                     # Interface gráfica (Tkinter)
│
├── utils/
│   ├── __init__.py
│   └── arquivos.py                # Leitura e escrita de arquivos JSON
│
├── controle_atendimentos.db       # Banco de dados SQLite (gerado em execução)
├── pessoas.json                   # Exportação de pessoas (gerado sob demanda)
├── atendimentos.json              # Exportação de atendimentos (gerado sob demanda)
└── README.md
```

---

## 5. Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa — apenas bibliotecas da stdlib:
  - `sqlite3`
  - `tkinter`
  - `json`
  - `pathlib`

---

## 6. Como Executar

**Interface de terminal (CLI):**

```bash
python main.py
```

**Interface gráfica (Tkinter):**

```bash
python main.py --gui
```

O banco de dados `controle_atendimentos.db` é criado automaticamente na primeira execução.

---

## 7. Camadas da Aplicação

### `database.py` — Infraestrutura

Responsável pela conexão com o SQLite e pela criação das tabelas.

```python
def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    # Cria as tabelas pessoas e atendimentos se não existirem
```

---

### `services/pessoa_service.py` — Serviço de Pessoas

Contém todas as operações relacionadas a pessoas. Cada função retorna uma tupla `(bool, str)` indicando sucesso e mensagem.

| Função | Descrição |
|---|---|
| `cadastrar_pessoa(nome, cpf, telefone)` | Insere uma nova pessoa |
| `listar_pessoas()` | Retorna todas as pessoas ordenadas por nome |
| `buscar_pessoa_por_nome_ou_cpf(termo)` | Busca por nome ou CPF (LIKE) |
| `buscar_pessoa_por_id(pessoa_id)` | Retorna uma pessoa pelo ID |
| `excluir_pessoa(pessoa_id)` | Exclui se não houver atendimentos ativos |

---

### `services/atendimento_service.py` — Serviço de Atendimentos

| Função | Descrição |
|---|---|
| `registrar_atendimento(pessoa_id, descricao)` | Cria atendimento com status `aberto` |
| `listar_atendimentos()` | Lista todos com JOIN em pessoas |
| `atualizar_status_atendimento(id, status)` | Atualiza para `aberto`, `em andamento` ou `finalizado` |

---

### `ui/cli.py` — Interface de Terminal

Menu interativo com as opções numeradas. Cada opção é mapeada para uma função de ação, sem lógica de negócio direta.

---

### `ui/gui.py` — Interface Gráfica

Toda a interface Tkinter encapsulada na função `iniciar_gui()`. Widgets e funções de ação são declarados como variáveis e closures locais, sem estado global.

---

### `utils/arquivos.py` — Utilitário de Arquivos

```python
def salvar_json(nome_arquivo, dados):   # Serializa dados para JSON
def carregar_json(nome_arquivo):        # Lê JSON do disco com fallback para []
```

---

## 8. Banco de Dados

Banco SQLite local (`controle_atendimentos.db`) com duas tabelas:

**Tabela `pessoas`**

| Coluna | Tipo | Restrição |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `nome` | TEXT | NOT NULL |
| `cpf` | TEXT | NOT NULL UNIQUE |
| `telefone` | TEXT | — |

**Tabela `atendimentos`**

| Coluna | Tipo | Restrição |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `pessoa_id` | INTEGER | FOREIGN KEY → pessoas(id) |
| `descricao` | TEXT | NOT NULL |
| `status` | TEXT | NOT NULL |

**Status permitidos:** `aberto` · `em andamento` · `finalizado`

---

## 9. Regras de Negócio

- Nome e CPF são obrigatórios no cadastro de pessoa.
- CPF deve ser único no sistema.
- Descrição é obrigatória no registro de atendimento.
- Todo atendimento é criado com status `aberto`.
- Não é possível excluir uma pessoa com atendimentos com status `aberto` ou `em andamento`.
- O status de um atendimento só aceita os valores: `aberto`, `em andamento`, `finalizado`.

---

## 10. Conceitos Aplicados

| Conceito | Onde é utilizado |
|---|---|
| Funções | Toda a lógica está organizada em funções com responsabilidade única |
| Módulos e pacotes | `services/`, `ui/`, `utils/` são pacotes Python com `__init__.py` |
| Condicionais | Validações nos services (`if not nome.strip()`) |
| Laços de repetição | Menu CLI (`while True`) e listagem de resultados (`for`) |
| Tuplas | Registros retornados pelo SQLite (`pessoa[0]`, `pessoa[1]`...) |
| Dicionários | Mapeamento de opções no menu CLI; exportação para JSON |
| Listas por compreensão | Conversão de tuplas SQLite para dicts na exportação JSON |
| Tratamento de exceções | `try/except` nos services e na leitura de IDs na CLI |
| Banco de dados SQLite | `database.py` com queries parametrizadas (proteção contra SQL Injection) |
| Tkinter | Interface gráfica encapsulada em `ui/gui.py` |
| Arquivos JSON | `utils/arquivos.py` para exportação e importação de dados |
| Closures | Funções de ação da GUI referenciam widgets locais via closure |
