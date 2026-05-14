# LangGraph: Guia Introdutório

## O que é o LangGraph?

LangGraph é uma biblioteca Python (e JavaScript) construída sobre o **LangChain** que permite criar aplicações de IA na forma de **grafos de estado**. Em vez de fluxos lineares, o LangGraph modela a lógica de uma aplicação como um grafo direcionado, onde cada nó representa uma etapa de processamento e as arestas definem as transições entre essas etapas.

Foi criado para resolver um problema central em sistemas de IA mais sofisticados: a necessidade de **ciclos, ramificações e memória persistente** — características que pipelines lineares simples não conseguem expressar bem.

---

## Para que ele serve?

O LangGraph é especialmente útil para construir:

- **Agentes autônomos** — que decidem por conta própria quais ferramentas usar e quando parar
- **Sistemas multi-agentes** — onde vários agentes colaboram ou supervisionam uns aos outros
- **Fluxos de trabalho com loops** — como "tentar → verificar resultado → corrigir → tentar novamente"
- **Chatbots com memória de longo prazo** — que mantêm contexto entre sessões
- **Pipelines de aprovação humana (human-in-the-loop)** — onde um humano pode intervir em pontos específicos do processo

A grande vantagem sobre abordagens tradicionais é o controle fino sobre o **fluxo de execução** e o **estado compartilhado** entre as etapas.

---

## Estrutura Básica

Um grafo no LangGraph é composto por três elementos principais:

### 1. Estado (`State`)

O estado é um dicionário tipado (geralmente usando `TypedDict`) que representa as informações compartilhadas entre todos os nós do grafo. Cada nó pode ler e modificar esse estado.

```python
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]  # lista que acumula mensagens
    contador: int
```

### 2. Nós (`Nodes`)

Nós são funções Python que recebem o estado atual e retornam um dicionário com as atualizações a serem aplicadas ao estado.

```python
def meu_no(state: State) -> dict:
    # Processa o estado e retorna as atualizações
    novo_contador = state["contador"] + 1
    return {"contador": novo_contador}
```

### 3. Arestas (`Edges`)

Arestas definem para onde o fluxo vai após cada nó. Podem ser:

- **Arestas simples** — sempre vão para o mesmo nó seguinte
- **Arestas condicionais** — escolhem o próximo nó com base no estado atual

```python
def decidir_proximo_passo(state: State) -> str:
    if state["contador"] >= 3:
        return "finalizar"
    else:
        return "continuar"
```

---

## Exemplo Completo Mínimo

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Definir o estado
class State(TypedDict):
    valor: int

# 2. Definir os nós
def incrementar(state: State) -> dict:
    return {"valor": state["valor"] + 1}

def verificar(state: State) -> str:
    if state["valor"] >= 3:
        return "fim"
    return "continuar"

# 3. Montar o grafo
grafo = StateGraph(State)

grafo.add_node("incrementar", incrementar)

grafo.set_entry_point("incrementar")

grafo.add_conditional_edges(
    "incrementar",
    verificar,
    {
        "continuar": "incrementar",  # volta para si mesmo (loop)
        "fim": END
    }
)

# 4. Compilar e executar
app = grafo.compile()
resultado = app.invoke({"valor": 0})

print(resultado)  # {'valor': 3}
```

---

## Diagrama da Estrutura

```
┌─────────────┐
│  ENTRADA    │  Estado inicial: { valor: 0 }
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  incrementar│  Nó: valor += 1
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  verificar  │  Aresta condicional
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
loop     ┌─────┐
(volta)  │ END │
         └─────┘
```

---

## Conceitos Avançados Importantes

| Conceito | Descrição |
|---|---|
| **Checkpointing** | Salva o estado em cada passo, permitindo pausar e retomar execuções |
| **Human-in-the-loop** | Interrompe o grafo em pontos específicos para aguardar input humano |
| **Subgrafos** | Grafos aninhados dentro de outros grafos para modularização |
| **Multi-agentes** | Múltiplos grafos se comunicando, com papéis de supervisor e executor |
| **Streaming** | Transmite atualizações de estado em tempo real para a interface |

---

## Quando usar LangGraph?

Use o LangGraph quando sua aplicação precisar de:

- Lógica **não-linear** (loops, ramificações complexas)
- **Memória persistente** entre chamadas ou sessões
- Múltiplos agentes ou etapas que precisam **compartilhar estado**
- **Controle explícito** sobre o fluxo de execução
- Capacidade de **pausar e retomar** em qualquer ponto

Para pipelines simples e lineares, o LangChain puro (chains) ainda pode ser a escolha mais direta.

---

## Recursos Oficiais

- Documentação: [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)
- Repositório: [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- Tutoriais interativos: [https://academy.langchain.com](https://academy.langchain.com)