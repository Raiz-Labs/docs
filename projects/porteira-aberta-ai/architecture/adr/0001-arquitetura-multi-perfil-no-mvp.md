# 0001: Arquitetura multi-perfil desde o Sprint 1 do MVP

- **Status**: proposto
- **Data**: 2026-07-26

## Contexto

O PRD (`projects/porteira-aberta-ai/prds/PRD_PorteiraAbertaAI_v1.docx`, §13) deixa esta decisão de produto em aberto:

> "Definição: lançar multi-perfil no MVP ou habilitar apenas Produtor? — Decisão pendente."
>
> "Decisão de produto pendente: a arquitetura multi-perfil deve ser construída no Sprint 1 (banco, RLS, feature flags), mas os perfis não-produtor ficam desabilitados até validação do core com produtores reais. Habilitar via feature flag sem deploy."

O MVP atende exclusivamente o perfil Produtor (§5 do PRD). Os perfis futuros — Agrônomo, Agrocomércio, Cooperativa, Administrador (§5.2) — não têm escopo funcional definido para o MVP, mas o PRD já assume, em §8.1, que "toda a arquitetura de banco de dados, autenticação e permissões é construída para suportar múltiplos perfis (multi-tenant) desde o Sprint 1", com o RBAC de §8.4 (`owner`, `admin`, `agrônomo`, `viewer`, `super_admin`) e a modelagem de `organizations` / `org_members` de §8.3 já desenhados para isso.

A pergunta em aberto é se essa fundação multi-perfil deve mesmo ser construída já no Sprint 1 (custo antecipado, evita refatoração futura) ou se o MVP deveria simplificar para um schema single-tenant focado só em Produtor, adiando o custo de multi-tenant para quando um segundo perfil for realmente priorizado.

## Decisão

_A decidir — este é um stub gerado a partir do PRD. Preencher após alinhamento com o PO (Mario)._

## Consequências

_A preencher junto com a Decisão._
