# 0001: Modelo de cobrança e compliance fiscal (NFC-e) ainda não definidos

- **Status**: proposto
- **Data**: 2026-07-29

## Contexto

Não existe PRD para o Comandou em `projects/comandou/prds/` — esta arquitetura foi construída a partir da revisão direta do código (`comandou-api` e `comandou-web`).

O schema Prisma (`comandou-api/prisma/schema.prisma`) já modela o Comandou como um SaaS: `Tenant.plano` (String, default `"basic"`) e `Tenant.ativo` sugerem a existência de planos pagos e a possibilidade de suspender um tenant. Nenhuma das duas dependências (`comandou-api/package.json`) confirma isso, no entanto:

- Não há integração de pagamento (Stripe, Pagar.me, Mercado Pago, etc.) em nenhum módulo.
- Não há emissão de nota fiscal (NFC-e), que no Brasil é normalmente obrigatória para operações de venda em estabelecimentos comerciais como restaurantes.
- `masterService.criarTenant` cria o tenant com o `plano` recebido no DTO, mas nada no código valida, cobra ou expira esse plano.

O produto está em estágio de MVP, sem clientes reais em produção, então essa decisão pode estar deliberadamente fora do escopo atual — mas fica registrada aqui para não ser esquecida antes de qualquer lançamento comercial.

## Decisão

_A decidir — este é um stub. Preencher quando o modelo de cobrança (ex: cobrança manual, gateway de pagamento, ciclo de billing) e a postura sobre emissão fiscal (NFC-e obrigatória via integração terceira, ou fora do escopo do produto) forem definidos._

## Consequências

_A preencher junto com a Decisão._
