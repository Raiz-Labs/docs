# docs

Documentação central da Raiz-Labs: PRDs, arquitetura e decisões técnicas que atravessam múltiplos repositórios.

## Estrutura

- `projects/<nome-do-projeto>/prds/` — PRDs específicos daquele projeto.
- `projects/<nome-do-projeto>/architecture/` — Arquitetura e ADRs específicos daquele projeto.
- `shared/prds/` e `shared/architecture/adr/` — PRDs e decisões que atravessam múltiplos projetos/times.
- `templates/` — Modelos para criar novos PRDs e ADRs.

## Quando usar este repo vs. o repo do projeto

- **Aqui**: PRDs, visão de arquitetura, ADRs — de um projeto específico ou cross-projeto.
- **No repo do projeto**: docs de setup/dev, coisas atreladas ao dia a dia do código daquele repo.

## Como contribuir

1. Copie o template relevante de `templates/`.
2. Se for específico de um projeto, salve em `projects/<nome-do-projeto>/prds/` ou `projects/<nome-do-projeto>/architecture/`. Se atravessa múltiplos projetos, salve em `shared/`.
3. Nomeie com `AAAA-MM-DD-titulo-curto.md` (PRDs) ou `NNNN-titulo-curto.md` (ADRs, número sequencial).
4. Abra um PR para revisão.
