# Fórmulas — Referência

## ROI unificado

```
ROI = (milhas_extras × MKT − custo_extra) ÷ custo_extra × 100
```

- **MKT**: cotação de mercado da milha LATAM Pass (R$ 0,025 em mar/2026, fonte: Balcão de Milhas)
- **milhas_extras**: milhas geradas pelo investimento (clube + bônus) que não existiriam sem pagar
- **custo_extra**: anuidade cartão + clube − custo do baseline

## Classificação de milhas

### Baseline
Cartão de menor custo do usuário, sem clube. Exemplo: C6 Carbon (2,5 pts/USD, R$ 0).

### Milhas extras
Tudo que só existe porque o usuário paga:
- **Clube fixo**: milhas mensais do plano (ex: 11.500 com Turbo)
- **Bônus campanha***: % extra sobre acúmulo do cartão co-branded Itaú (requer cartão + clube)
- **Bônus transferência**: % extra sobre transferências externas (requer clube)

### Externas
Acúmulo base de fontes independentes do investimento (base do C6, IUPP, Amazon, voos).

## R$/milha extra

```
R$/mi = custo_total ÷ milhas_extras
```

Se R$/mi < MKT → ROI positivo (gerando milhas mais baratas que o mercado).

## Bench incremental

Para cada combinação cartão × clube:

```
cardMi = USD_gastos × taxa_efetiva_com_clube
clubMi = milhas_fixas_mensais
total = cardMi + clubMi
extras = total − baseline
custo = anuidade + clube
ROI = (extras × MKT − custo) ÷ custo × 100
```

### Taxas efetivas com clube

| Cartão | Tipo | Base | Com Clube | Fonte do bônus |
|---|---|---|---|---|
| LATAM Infinite | direct | 2,5 | 3,75 | *campanha +50% |
| C6 Carbon | transfer | 2,5 | 3,375 | clube +35% transf. |
| The One | transfer | 3,0 | 4,05 | clube +35% transf. |
| BRB DUX | transfer | 5,0 | 6,75 | clube +35% transf. |

## Detecção de campanhas

```
campanha_pct = itauBonus ÷ itauBase × 100
```

Se > 0% em um mês, há campanha ativa.

## Carência

Primeiro mês do extrato sem dados do cartão principal = carência.
Regra: `idx === 0 && itauBase === 0`
Excluído de todos os cálculos de ROI.

## Cap de bônus

30.000 milhas/mês (inclui todos os bônus do clube).
Verificar no extrato: ago/25 bateu exato (IUPP 4.761 + C6 25.239 = 30.000).

## Gradiente de cores

```js
const MKT = 0.025;
function cpmColor(value) {
  if (value == null) return "#475569";     // sem dados
  if (value >= MKT) return "#ef4444";      // acima do mercado
  const t = Math.min(value / MKT, 1);     // 0..1
  const r = Math.round(4 + t * 106);
  const g = Math.round(120 + t * 111);
  const b = Math.round(87 + t * 96);
  return `rgb(${r},${g},${b})`;            // verde escuro → claro
}
```

Verde escuro = muito eficiente, verde claro = próximo do mercado, vermelho = acima.

## Referência de mercado (MKT)

| Fonte | Valor | Contexto |
|---|---|---|
| Balcão de Milhas (venda) | R$ 0,025/mi | Preço que você receberia vendendo |
| LATAM compra direta (tabela) | R$ 0,070/mi | Preço cheio sem desconto |
| LATAM compra c/ 60% desc | R$ 0,028/mi | Promo mar/2026 (c/ Itaú) |
| LATAM Black Friday 2025 | R$ 0,024/mi | Melhor preço histórico recente |
| Melhores Destinos valor-alvo 2026 | R$ 0,025/mi | Referência editorial |

Usar R$ 0,025 como padrão. Pesquisar valor atualizado quando possível.
