# Fórmulas — Referência

Última atualização: Abril 2026

## ROI unificado

```
ROI = (milhas_extras × MKT − custo_extra) ÷ custo_extra × 100
```

- **MKT**: cotação de mercado da milha LATAM Pass (referência: R$ 0,025 em abr/2026)
- **milhas_extras**: milhas geradas pelo investimento (clube + bônus) que não existiriam sem pagar
- **custo_extra**: anuidade cartão + clube − custo do baseline

### ⚠️ Sobre a natureza do ROI

Este ROI é uma **estimativa teórica baseada no valor de mercado** (preço de venda no mercado secundário). Ele responde à pergunta: "se eu vendesse essas milhas extras hoje, teria lucro sobre o que paguei?"

**O ROI real depende do uso final da milha:**

| Forma de uso | Valor equivalente por milha | Comentário |
|---|---|---|
| Venda no mercado (Balcão de Milhas, MaxMilhas, etc.) | R$ 0,020–0,030 | Valor líquido de venda |
| Resgate de passagem econômica doméstica | R$ 0,03–0,05 | Depende da rota e antecedência |
| Resgate de passagem econômica internacional | R$ 0,04–0,08 | Bons resgates LATAM podem superar R$0,10 |
| Resgate de executiva/primeira | R$ 0,08–0,15+ | Sweet spots podem dar R$0,15+ por milha |
| Compra direta LATAM (tabela cheia) | R$ 0,070 | Preço de referência da LATAM |

**Conclusão**: O ROI com MKT de R$0,025 é conservador. Se o usuário resgata passagens (especialmente internacionais ou executiva), o valor real da milha pode ser 2-6× maior, tornando o ROI muito mais positivo. Se vende milhas no mercado, R$0,025 é a referência correta.

**Recomendação para o dashboard**: Mostrar o ROI com MKT padrão (R$0,025) e oferecer um slider ou campo para o usuário ajustar o valor da milha conforme seu uso. Sugestões de preset:
- Conservador (venda): R$ 0,020
- Mercado (padrão): R$ 0,025
- Resgate econômico: R$ 0,040
- Resgate executiva: R$ 0,080

## Classificação de milhas

### Baseline
Cartão de menor custo do usuário, sem clube. Exemplo: C6 Carbon com isenção (2,5 pts/USD, custo R$ 0).

> **Importante**: Se o usuário tem isenção de anuidade por investimento ou gasto, o custo do cartão é R$0 para fins de baseline. Perguntar no onboarding.

### Milhas extras
Tudo que só existe porque o usuário paga:
- **Clube fixo**: milhas mensais do plano (ex: 11.500 com Turbo+Itaú)
- **Bônus campanha***: % extra sobre acúmulo do cartão co-branded Itaú (requer cartão + clube)
- **Bônus transferência**: % extra sobre transferências externas (requer clube)

### Externas
Acúmulo base de fontes independentes do investimento (base do C6, IUPP, Amazon, voos, Nubank base).

## R$/milha extra

```
R$/mi = custo_total ÷ milhas_extras
```

Se R$/mi < MKT → ROI positivo (gerando milhas mais baratas que o mercado).

## Bench incremental

Para cada combinação cartão × clube:

```
# Determinar se o cartão é LATAM Pass Itaú
isItau = cartao.tipo == "direct"

# Milhas do clube (diferente com/sem Itaú)
clubMi = isItau ? clube.milhas_com_itau : clube.milhas_sem_itau

# Taxa efetiva com clube
if isItau:
    taxaEfetiva = cartao.taxa_base × (1 + campanha_pct / 100)
else:
    bonusTransf = isItau ? clube.bonus_transf_com_itau : clube.bonus_transf_sem_itau
    taxaEfetiva = cartao.taxa_base × (1 + bonusTransf)

# Cálculo
cardMi = USD_gastos × taxaEfetiva
total = cardMi + clubMi
extras = total − baseline
custo = anuidade_cartao + clube_mensal  # anuidade=0 se isento
ROI = (extras × MKT − custo) ÷ custo × 100
```

### Taxas efetivas com clube (Turbo, o mais alto)

| Cartão | Tipo | Base | Com Clube (sem Itaú) | Com Clube (com Itaú) | Fonte do bônus |
|---|---|---|---|---|---|
| LATAM Infinite | direct | 2,5 | — | 3,75* | campanha +50%* |
| LATAM Black | direct | 2,5 | — | 3,75* | campanha +50%* |
| LATAM Platinum | direct | 2,0 | — | 3,00* | campanha +50%* |
| LATAM Gold | direct | 1,6 | — | 2,40* | campanha +50%* |
| LATAM Internacional | direct | 1,3 | — | 1,95* | campanha +50%* |
| C6 Carbon | transfer | 2,5 | 3,25 (30%) | 3,375 (35%) | clube transf. |
| Nubank Ultravioleta | transfer | 2,2 | 2,86 (30%) | 2,97 (35%) | clube transf. |
| Nubank UV (Modo LATAM) | transfer | 2,42 | 3,146 (30%) | 3,267 (35%) | modo LATAM +10% + clube |
| The One | transfer | 3,0 | 3,90 (30%) | 4,05 (35%) | clube transf. |
| BRB DUX | transfer | 5,0 | 6,50 (30%) | 6,75 (35%) | clube transf. |
| Centurion | transfer | 5,0 | 6,50 (30%) | 6,75 (35%) | clube transf. |

> **Nota**: Cartões "direct" (Itaú) recebem campanha* no acúmulo. Cartões "transfer" recebem bônus de transferência do clube. A coluna "com Itaú" para cartões transfer significa que o usuário TEM um cartão Itaú ativo, portanto o clube dá bônus maiores.

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

30.000 milhas/mês (inclui todos os bônus do clube: transferência + campanha + parceiros + Multiplica).
Verificar no extrato se algum mês bateu o cap.

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
| MaxMilhas (venda) | R$ 0,026/mi | Variável, pode chegar a R$0,029 |
| HotMilhas (venda) | R$ 0,024–0,029/mi | Range observado em 2026 |
| BankMilhas (venda) | R$ 0,018/mi | Abaixo do mercado |
| LATAM compra direta (tabela) | R$ 0,070/mi | Preço cheio sem desconto |
| LATAM compra c/ desconto | R$ 0,024–0,028/mi | Promos com 60-66% desc |
| Melhores Destinos valor-alvo 2026 | R$ 0,025/mi | Referência editorial |
| Manual das Milhas (valor resgate) | R$ 0,038/mi | Baseado em valor médio de resgate |

Usar R$ 0,025 como padrão (conservador, venda mercado). Pesquisar valor atualizado quando possível.
Para análise de valor de resgate, considerar R$ 0,038+ (depende do uso).
