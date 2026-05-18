````markdown
# Sistema RAD de Controle de Atendimentos em Python

## 1. Visão Geral do Projeto

Este projeto foi desenvolvido com o objetivo de demonstrar, em um único sistema, os principais conceitos estudados em uma disciplina de Desenvolvimento Rápido de Aplicações (RAD) com Python.

Ao final deste projeto, o aluno terá contato com:

- Lógica de programação;
- Funções;
- Modularização;
- Manipulação de arquivos JSON;
- Banco de dados SQLite;
- Interface gráfica com Tkinter;
- Regras de negócio;
- Organização em camadas.

---

# 2. Objetivo do Sistema

O sistema permite:

- Cadastrar pessoas;
- Listar pessoas;
- Buscar pessoas por nome ou CPF;
- Excluir pessoas;
- Registrar atendimentos;
- Listar atendimentos;
- Atualizar o status de um atendimento;
- Exportar os dados para arquivos JSON;
- Utilizar interface gráfica.

---

# 3. Conceitos Aplicados

## 3.1 Variáveis

Armazenam dados temporariamente na memória.

```python
nome = "Maria"
cpf = "12345678900"
````

---

## 3.2 Funções

Agrupam instruções que executam uma tarefa específica.

```python
def cadastrar_pessoa(nome, cpf, telefone):
    pass
```

---

## 3.3 Condicionais

Permitem tomar decisões.

```python
if not cpf.strip():
    return False, "CPF obrigatório."
```

---

## 3.4 Laços de Repetição

Percorrem listas.

```python
for pessoa in pessoas:
    print(pessoa)
```

---

## 3.5 Listas

Armazenam vários elementos.

```python
pessoas = []
```

---

## 3.6 Tuplas

Representam registros retornados pelo SQLite.

```python
(1, "Maria", "123", "79999999999")
```

---

## 3.7 Dicionários

Estrutura chave/valor.

```python
{
    "id": 1,
    "nome": "Maria"
}
```

---

## 3.8 Módulos

Cada arquivo `.py` representa um módulo.

```python
from pessoa_service import cadastrar_pessoa
```

---

## 3.9 Banco de Dados SQLite

Banco embutido no Python.

---

## 3.10 Tkinter

Biblioteca padrão para interface gráfica.

---

# 4. Estrutura do Projeto

```text
controle_atendimentos/
│
├── database.py
├── arquivos.py
├── pessoa_service.py
├── atendimento_service.py
├── main.py
├── interface.py
├── controle_atendimentos.db
├── pessoas.json
├── atendimentos.json
└── README.md
```
