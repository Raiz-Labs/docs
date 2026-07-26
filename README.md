# docs

Documentação central da Raiz-Labs: PRDs, arquitetura e decisões técnicas que atravessam múltiplos repositórios.

## Estrutura

- `prds/` — Product Requirement Docs. Um arquivo por produto/feature relevante.
- `architecture/` — Visões de arquitetura de alto nível (diagramas, integrações entre sistemas).
- `architecture/adr/` — Architecture Decision Records. Decisões técnicas pontuais, numeradas e imutáveis.
- `templates/` — Modelos para criar novos PRDs e ADRs.

## Quando usar este repo vs. o repo do projeto

- **Aqui**: PRDs, visão de arquitetura cross-repo, decisões que afetam mais de um serviço/time.
- **No repo do projeto**: ADRs locais sobre implementação específica daquele serviço, docs de setup/dev.

## Como contribuir

1. Copie o template relevante de `templates/`.
2. Salve em `prds/` ou `architecture/adr/` com nome `AAAA-MM-DD-titulo-curto.md` (PRDs) ou `NNNN-titulo-curto.md` (ADRs, número sequencial).
3. Abra um PR para revisão.
