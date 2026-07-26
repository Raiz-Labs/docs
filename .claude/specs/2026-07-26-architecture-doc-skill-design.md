# Skill: architecture-doc — Design

- **Data**: 2026-07-26
- **Status**: aprovado

## Contexto

O repo `docs` (Raiz-Labs) já organiza PRDs por projeto em `projects/<slug>/prds/`. Faltava um fluxo padronizado para produzir o documento de arquitetura de cada projeto a partir do PRD já existente, sem depender de skills externas de baixa adoção (pesquisa de mercado mostrou que não existe uma skill dominante para isso — as mais estreladas no GitHub têm dezenas de estrelas, não milhares, e a maioria assume código já existente).

Padrão de mercado escolhido como base: **arc42** (estrutura de 12 seções) + **C4 model** (diagramas de contexto/container) + **ADR** (registro de decisões), que é a combinação mais usada na indústria para documentação de arquitetura.

## Objetivo

Uma skill de projeto (`docs/.claude/skills/architecture-doc/`) que gera `projects/<slug>/architecture/architecture.md` a partir do PRD do projeto, seguindo arc42, com diagramas C4 em Mermaid, perguntando ao usuário apenas o que não estiver coberto pelo PRD, e propondo stubs de ADR para decisões técnicas deixadas em aberto no PRD.

## Não-objetivos

- Não gera diagramas C4 a partir de código-fonte existente (fora do escopo — projetos aqui ainda não têm implementação).
- Não usa PlantUML/Structurizr (Mermaid renderiza nativo no GitHub e em artifacts, sem dependência externa).
- Não produz 12 arquivos arc42 separados — um `architecture.md` único por projeto.
- Não resolve conflitos entre múltiplos PRDs do mesmo projeto — usa o mais recente e avisa.

## Fluxo

1. **Input**: `/architecture-doc <slug-do-projeto>` (argumento obrigatório = pasta em `projects/`).
2. **Extração**: lê todo arquivo em `projects/<slug>/prds/*`.
   - `.md` lido diretamente.
   - `.docx` extraído via script stdlib (`zipfile` + `xml`/regex sobre `word/document.xml`) — mesma técnica usada manualmente na sessão anterior para o PRD da Porteira Aberta AI, sem dependência de `pandoc` ou `python-docx`.
3. **Mapeamento**: o conteúdo extraído é mapeado contra as 12 seções arc42:
   1. Introdução e Metas
   2. Restrições de Arquitetura
   3. Escopo e Contexto do Sistema
   4. Estratégia de Solução
   5. Visão de Building Blocks
   6. Visão de Runtime
   7. Visão de Deployment
   8. Conceitos Transversais
   9. Decisões de Arquitetura (ADRs)
   10. Requisitos de Qualidade
   11. Riscos e Dívida Técnica
   12. Glossário
4. **Gap-filling interativo**: para cada seção sem conteúdo suficiente no PRD, pergunta ao usuário (uma pergunta por vez, via `AskUserQuestion` quando aplicável). Se não houver PRD algum em `projects/<slug>/prds/`, todas as seções caem nesse caminho — sem branch especial para "sem PRD".
5. **Diagramas C4 (Mermaid)**: gera ao menos diagrama de Contexto e de Container a partir da stack/entidades identificadas (seção 5 do PRD, quando presente). Se a informação for insuficiente para um diagrama coerente, pergunta ao usuário os componentes principais antes de desenhar.
6. **Detecção de decisões pendentes**: varre o texto por sinalizadores ("decisão pendente", "a definir", "TBD", frases terminadas em "?") ligados a escolhas técnicas. Para cada uma, propõe um stub de ADR (usando `templates/ADR-template.md`) e pede confirmação antes de criar o arquivo em `projects/<slug>/architecture/adr/NNNN-titulo-curto.md` (numeração sequencial dentro da pasta), com status `proposto`.
7. **Escrita final**: grava `projects/<slug>/architecture/architecture.md` com as 12 seções preenchidas.
8. **Resumo**: ao final, lista o que foi gerado e quais ADRs propostos ainda aguardam decisão.

## Estrutura de arquivos da skill

```
docs/.claude/skills/architecture-doc/
├── SKILL.md                    # frontmatter + fluxo acima
└── scripts/
    └── extract_docx_text.py    # stdlib only: zipfile + regex sobre word/document.xml
```

## Casos de erro

- `projects/<slug>/` não existe → avisa e para (não cria projeto novo; isso é responsabilidade do fluxo já existente de criação de projeto).
- Mais de um arquivo em `prds/` → usa o de data de modificação mais recente, avisa qual foi usado.
- `architecture/architecture.md` já existe → pergunta se é para sobrescrever, mesclar (reaproveitar seções já preenchidas) ou cancelar.
