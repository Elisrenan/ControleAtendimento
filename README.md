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
7. [Camadas da Aplicação](#7-camadas-da-aplicação)
8. [Banco de Dados](#8-banco-de-dados)
9. [Regras de Negócio](#9-regras-de-negócio)
10. [Conceitos Aplicados](#10-conceitos-aplicados)

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
