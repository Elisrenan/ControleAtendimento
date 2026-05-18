# Sistema de Controle de Atendimentos

Sistema em Python nativo para cadastro de pessoas e gerenciamento de atendimentos, com suporte a interface de terminal (CLI) e interface gráfica (GUI).

Desenvolvido na disciplina de **Desenvolvimento Rápido de Aplicações (RAD) com Python** como demonstração prática de arquitetura em camadas profissional usando exclusivamente a biblioteca padrão do Python.

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Funcionalidades](#2-funcionalidades)
3. [Arquitetura em Camadas](#3-arquitetura-em-camadas)
4. [Estrutura do Projeto](#4-estrutura-do-projeto)
5. [Pré-requisitos](#5-pré-requisitos)
6. [Como Executar](#6-como-executar)
7. [Testes e Qualidade de Código](#7-testes-e-qualidade-de-código)
8. [Integração Contínua (CI)](#8-integração-contínua-ci)
9. [Camadas da Aplicação — Detalhamento](#9-camadas-da-aplicação--detalhamento)
10. [Banco de Dados](#10-banco-de-dados)
11. [Regras de Negócio](#11-regras-de-negócio)
12. [Conceitos Aplicados](#12-conceitos-aplicados)
13. [Regra de Ouro da Arquitetura](#13-regra-de-ouro-da-arquitetura)

---

## 1. Visão Geral

Este projeto demonstra a **Arquitetura em Camadas Limpa** (*Layered Architecture*) com Python puro — sem nenhum framework externo.

A ideia central é **separar responsabilidades**: cada parte do sistema tem uma única função bem definida e só se comunica com a camada imediatamente abaixo.

| Camada | Responsabilidade | O que ela NÃO faz |
|---|---|---|
| `ui/` | Exibir e coletar dados do usuário | Nunca executa SQL, nunca contém regras |
| `services/` | Validar e aplicar regras de negócio | Nunca executa SQL direto |
| `infrastructure/repositories/` | Executar SQL no banco de dados | Nunca contém regras de negócio |
| `domain/` | Definir o que são os dados (entidades) | Nunca depende de nada externo |

---

## 2. Funcionalidades

| Módulo | Funcionalidade |
|---|---|
| Pessoas | Cadastrar, listar, buscar por nome ou CPF, excluir |
| Atendimentos | Registrar, listar, atualizar status |
| Exportação | Exportar pessoas e atendimentos para JSON |
| Interface | Terminal (CLI) e Interface Gráfica (Tkinter) |

---

## 3. Arquitetura em Camadas

```
┌──────────────────────────────────────────────┐
│          ui/cli.py  ·  ui/gui.py             │
│              Camada de Apresentação          │
│   Sabe: como exibir · Não sabe: SQL, regras  │
├──────────────────────────────────────────────┤
│   services/pessoa_service.py                 │
│   services/atendimento_service.py            │
│              Camada de Negócio               │
│   Sabe: regras · Não sabe: SQL, widgets      │
├──────────────────────────────────────────────┤
│   infrastructure/repositories/              │
│   pessoa_repository.py                       │
│   atendimento_repository.py                  │
│              Camada de Dados                 │
│   Sabe: SQL · Não sabe: regras, widgets      │
├──────────────────────────────────────────────┤
│   domain/models.py                           │
│   @dataclass Pessoa · @dataclass Atendimento │
│              Camada de Domínio               │
│   Define as entidades · Sem dependências     │
└──────────────────────────────────────────────┘
              infrastructure/database.py
                  sqlite3 (stdlib)
```

**Direção das dependências:** cada camada aponta **somente para baixo**.

```
ui → services → repositories → domain
```

---

## 4. Estrutura do Projeto

```text
ControleAtendimento/
│
├── main.py                              # Ponto de entrada
│
├── domain/
│   ├── __init__.py
│   └── models.py                        # @dataclass Pessoa, @dataclass Atendimento
│
├── infrastructure/
│   ├── __init__.py
│   ├── database.py                      # Conexão SQLite + criar_tabelas()
│   └── repositories/
│       ├── __init__.py
│       ├── pessoa_repository.py         # SQL de pessoas (somente SQL)
│       └── atendimento_repository.py    # SQL de atendimentos (somente SQL)
│
├── services/
│   ├── __init__.py
│   ├── pessoa_service.py                # Regras de negócio de pessoas (sem SQL)
│   └── atendimento_service.py           # Regras de negócio de atendimentos (sem SQL)
│
├── ui/
│   ├── __init__.py
│   ├── cli.py                           # Interface de terminal (sem SQL, sem regras)
│   └── gui.py                           # Interface gráfica Tkinter (sem SQL, sem regras)
│
├── utils/
│   ├── __init__.py
│   └── arquivos.py                      # Escrita de arquivos JSON
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Fixture de banco temporário (pytest)
│   ├── test_pessoa_service.py           # 14 testes unitários de pessoas
│   └── test_atendimento_service.py      # 13 testes unitários de atendimentos
│
├── .github/
│   └── workflows/
│       └── deploy_local.yml             # Pipeline CI/CD (GitHub Actions)
│
├── requirements-dev.txt                 # Dependências de desenvolvimento
├── pyproject.toml                       # Configuração de black, isort e bandit
├── .flake8                              # Configuração do linter flake8
│
├── controle_atendimentos.db             # Banco SQLite (gerado na primeira execução)
├── pessoas.json                         # Exportação de pessoas (gerado sob demanda)
└── atendimentos.json                    # Exportação de atendimentos (gerado sob demanda)
```

---

## 5. Pré-requisitos

- Python 3.8 ou superior
- **Zero dependências externas para executar** — apenas bibliotecas da stdlib:

| Biblioteca | Uso |
|---|---|
| `sqlite3` | Banco de dados relacional embutido |
| `tkinter` | Interface gráfica nativa |
| `dataclasses` | Definição das entidades de domínio |
| `json` | Exportação de dados |
| `pathlib` | Caminho do banco de dados |

**Para desenvolvimento e testes**, instale as ferramentas com:

```bash
pip install -r requirements-dev.txt
```

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

## 7. Testes e Qualidade de Código

### Instalar as ferramentas

```bash
pip install -r requirements-dev.txt
```

### Rodar os testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Com relatório de cobertura
python -m pytest tests/ --cov=. --cov-report=term-missing -v
```

O projeto possui **27 testes unitários** distribuídos em dois arquivos:

| Arquivo | Testes | O que cobre |
|---|---|---|
| `tests/test_pessoa_service.py` | 14 | Cadastro, listagem, busca, exclusão de pessoas |
| `tests/test_atendimento_service.py` | 13 | Registro, listagem, status, regra de bloqueio |

**Isolamento de banco:** cada teste recebe um banco SQLite vazio e temporário via `conftest.py`, garantindo que os testes nunca afetam o banco de produção.

### Verificar qualidade do código

```bash
# Formatação (black)
python -m black . --check

# Ordenação de imports (isort)
python -m isort . --profile black --check-only

# Linting (flake8)
python -m flake8 .

# Segurança (bandit)
python -m bandit -r domain/ infrastructure/ services/ utils/ ui/ main.py
```

Para aplicar a formatação automaticamente (sem `--check`):

```bash
python -m black .
python -m isort . --profile black
```

---

## 8. Integração Contínua (CI)

O projeto usa **GitHub Actions** com o arquivo `.github/workflows/deploy_local.yml`.

### Gatilhos

O pipeline é acionado automaticamente em **qualquer branch** a cada `push` ou `pull_request`:

```yaml
on:
  push:
    branches: ['**']
  pull_request:
    branches: ['**']
```

### Jobs

| Job | Ferramenta | O que verifica |
|---|---|---|
| `test` | pytest + pytest-cov | 27 testes passando + relatório de cobertura enviado ao Codecov |
| `code-quality` | black, isort, flake8, bandit | Formatação, imports, linting e segurança |

### Configurar o `CODECOV_TOKEN`

O job de testes envia o relatório de cobertura para o [Codecov](https://codecov.io). Para isso, é necessário configurar um *secret* no repositório GitHub:

1. Acesse [codecov.io](https://codecov.io) e faça login com sua conta GitHub
2. Adicione o repositório e copie o **Upload Token**
3. No GitHub, vá em **Settings → Secrets and variables → Actions**
4. Clique em **New repository secret**
5. Nome: `CODECOV_TOKEN` — Valor: o token copiado do Codecov

> **Sem o token configurado**, o step de upload falha mas os testes continuam rodando normalmente — o `fail-fast: false` garante que o job não para nos testes.

---

## 9. Camadas da Aplicação — Detalhamento

### `domain/models.py` — Entidades de Domínio

Define **o que são** os dados do sistema usando `@dataclass`. Não tem nenhum import externo — é a camada mais independente e estável do projeto.

```python
@dataclass
class Pessoa:
    nome: str
    cpf: str
    telefone: str
    id: Optional[int] = None

@dataclass
class Atendimento:
    pessoa_id: int
    descricao: str
    status: str
    id: Optional[int] = None
    pessoa_nome: Optional[str] = None
```

> **Por que dataclass?** Substitui tuplas anônimas (`pessoa[0]`, `pessoa[1]`) por atributos nomeados (`pessoa.nome`, `pessoa.cpf`), tornando o código legível e com verificação de tipos.

---

### `infrastructure/database.py` — Conexão com o Banco

Responsável pela conexão com o SQLite e pela criação das tabelas. Usa `pathlib.Path` para localizar o arquivo do banco de forma confiável.

```python
def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    # CREATE TABLE IF NOT EXISTS pessoas ...
    # CREATE TABLE IF NOT EXISTS atendimentos ...
```

---

### `infrastructure/repositories/pessoa_repository.py` — Repositório de Pessoas

Contém **exclusivamente SQL**. Recebe e retorna objetos `Pessoa` (da camada `domain`). Não conhece nenhuma regra de negócio.

| Função | SQL executado |
|---|---|
| `inserir(pessoa)` | `INSERT INTO pessoas` |
| `listar_todos()` | `SELECT ... ORDER BY nome` |
| `buscar_por_nome_ou_cpf(termo)` | `SELECT ... WHERE nome LIKE ? OR cpf LIKE ?` |
| `buscar_por_id(pessoa_id)` | `SELECT ... WHERE id = ?` |
| `contar_atendimentos_ativos(pessoa_id)` | `SELECT COUNT(*) FROM atendimentos WHERE ...` |
| `excluir(pessoa_id)` | `DELETE FROM pessoas WHERE id = ?` |

---

### `infrastructure/repositories/atendimento_repository.py` — Repositório de Atendimentos

| Função | SQL executado |
|---|---|
| `inserir(atendimento)` | `INSERT INTO atendimentos` |
| `listar_todos()` | `SELECT ... INNER JOIN pessoas` |
| `atualizar_status(id, status)` | `UPDATE atendimentos SET status = ?` |

---

### `services/pessoa_service.py` — Serviço de Pessoas

Contém as **regras de negócio**. Não executa SQL — chama o repositório. Cada função retorna `(bool, str)` indicando sucesso e mensagem.

```python
# Exemplo: a regra de exclusão vive aqui, não no repositório
def excluir_pessoa(pessoa_id):
    total_ativos = pessoa_repository.contar_atendimentos_ativos(pessoa_id)
    if total_ativos > 0:
        return False, "Não é possível excluir pessoa com atendimento aberto ou em andamento."
    removido = pessoa_repository.excluir(pessoa_id)
    ...
```

| Função | Descrição |
|---|---|
| `cadastrar_pessoa(nome, cpf, telefone)` | Valida campos e insere via repositório |
| `listar_pessoas()` | Delega ao repositório |
| `buscar_pessoa_por_nome_ou_cpf(termo)` | Delega ao repositório |
| `buscar_pessoa_por_id(pessoa_id)` | Delega ao repositório |
| `excluir_pessoa(pessoa_id)` | Verifica atendimentos ativos antes de excluir |

---

### `services/atendimento_service.py` — Serviço de Atendimentos

| Função | Descrição |
|---|---|
| `registrar_atendimento(pessoa_id, descricao)` | Valida pessoa e descrição; cria com status `aberto` |
| `listar_atendimentos()` | Delega ao repositório |
| `atualizar_status_atendimento(id, status)` | Valida status permitido antes de atualizar |

---

### `ui/cli.py` — Interface de Terminal

Menu interativo com opções numeradas. Cada opção chama um `service` — nenhuma lógica de negócio ou SQL aqui.

---

### `ui/gui.py` — Interface Gráfica (Tkinter)

Toda a interface encapsulada em `iniciar_gui()`. Funções de ação são closures que chamam `services` e atualizam a `Listbox`. Zero SQL, zero regras.

---

### `utils/arquivos.py` — Utilitário de Arquivos

```python
def salvar_json(nome_arquivo, dados):   # Serializa lista de dicts para JSON
```

---

## 10. Banco de Dados

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

## 11. Regras de Negócio

- Nome e CPF são obrigatórios no cadastro de pessoa.
- CPF deve ser único no sistema.
- Descrição é obrigatória no registro de atendimento.
- Todo atendimento é criado com status `aberto`.
- Não é possível excluir uma pessoa com atendimentos com status `aberto` ou `em andamento`.
- O status de um atendimento só aceita os valores: `aberto`, `em andamento`, `finalizado`.

---

## 12. Conceitos Aplicados

| Conceito Python | Onde é utilizado |
|---|---|
| `@dataclass` | `domain/models.py` — entidades tipadas sem boilerplate |
| Funções | Toda a lógica organizada em funções com responsabilidade única |
| Módulos e pacotes | `domain/`, `infrastructure/`, `services/`, `ui/` com `__init__.py` |
| Tipagem (`Optional`, `List`) | Assinaturas das funções nos repositories |
| Condicionais | Validações nos services (`if not nome.strip()`) |
| Laços de repetição | Menu CLI (`while True`) e listagem de resultados (`for`) |
| Dicionários | Mapeamento de opções no menu CLI; exportação para JSON |
| Listas por compreensão | Conversão de linhas SQLite para `@dataclass` nos repositories |
| Tratamento de exceções | `try/except` nos services e leitura de IDs na CLI |
| Banco de dados SQLite | Queries parametrizadas com `?` (proteção contra SQL Injection) |
| Tkinter | Interface gráfica com closures para ações dos botões |
| Arquivos JSON | `utils/arquivos.py` para exportação e importação de dados |
| `pathlib.Path` | Localização confiável do arquivo do banco de dados |
| Padrão Repository | Isolamento do acesso a dados em `infrastructure/repositories/` |

---

## 13. Regra de Ouro da Arquitetura

> **Cada camada só conhece a camada imediatamente abaixo — nunca pula, nunca volta.**

```
ui/          →  chama  →  services/
services/    →  chama  →  infrastructure/repositories/
repositories →  usa    →  domain/models.py
```

**Verificação rápida:**
- Abra qualquer arquivo em `services/` — você **não deve** encontrar `import sqlite3`
- Abra qualquer arquivo em `ui/` — você **não deve** encontrar `import sqlite3` nem imports de `repositories/`
- Abra qualquer arquivo em `domain/` — você **não deve** encontrar nenhum import externo


**Status permitidos:** `aberto` · `em andamento` · `finalizado`
