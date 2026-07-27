# docs

Documentação central da Raiz-Labs: PRDs, arquitetura e decisões técnicas que atravessam múltiplos repositórios.

## Estrutura

- `projects/<nome-do-projeto>/prds/` — PRDs específicos daquele projeto.
- `projects/<nome-do-projeto>/architecture/` — Arquitetura e ADRs específicos daquele projeto.
- `shared/prds/` e `shared/architecture/adr/` — PRDs e decisões que atravessam múltiplos projetos/times.
- `templates/` — Modelos para criar novos PRDs e ADRs.
- `.claude/skills/architecture-doc/` — skill do Claude Code que gera o `architecture.md` de um projeto a partir do PRD dele.

## Gerando o architecture.md de um projeto

Depois que o PRD do projeto já estiver em `projects/<slug>/prds/`, rode no Claude Code:

```
/architecture-doc <slug-do-projeto>
```

A skill lê o PRD, monta o `architecture.md` seguindo o padrão [arc42](https://arc42.org) (12 seções) com diagramas [C4](https://c4model.com) em Mermaid, só pergunta o que o PRD não cobre, e propõe ADRs pras decisões que o PRD deixa em aberto.

## Quando usar este repo vs. o repo do projeto

- **Aqui**: PRDs, visão de arquitetura, ADRs — de um projeto específico ou cross-projeto.
- **No repo do projeto**: docs de setup/dev, coisas atreladas ao dia a dia do código daquele repo.

## Como contribuir

1. Copie o template relevante de `templates/`.
2. Se for específico de um projeto, salve em `projects/<nome-do-projeto>/prds/` ou `projects/<nome-do-projeto>/architecture/`. Se atravessa múltiplos projetos, salve em `shared/`.
3. Nomeie com `AAAA-MM-DD-titulo-curto.md` (PRDs) ou `NNNN-titulo-curto.md` (ADRs, número sequencial).
4. Abra um PR para revisão.
