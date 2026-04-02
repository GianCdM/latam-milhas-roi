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

### Baseline (dinâmico)

O baseline é determinado automaticamente a partir do perfil do usuário:

```
Algoritmo:
1. Filtrar todos os cartões do usuário onde custo_efetivo == 0
   (anuidade isenta por investimento, gasto mínimo, promoção, etc.)
2. Se há cartões com custo zero:
   → baseline = cartão com maior taxa de acúmulo (pts/USD) entre eles, sem clube
3. Se NENHUM cartão tem custo zero:
   → baseline = cartão com menor custo_efetivo_mensal, sem clube
4. baseline_milhas = gasto_USD × baseline_cartao.taxa_nac
5. baseline_custo = baseline_cartao.custo_efetivo_mensal (0 se isento)
```

> **Importante**: Isenção de anuidade (por investimento, gasto mínimo ou promoção) significa custo R$0 para fins de baseline. Sempre perguntar no onboarding.

Exemplos:
- Usuário tem C6 Carbon isento (2,5 pts/USD) e Nubank UV isento (2,2 pts/USD) → baseline = C6 Carbon (maior taxa, custo zero)
- Usuário tem apenas Itaú Infinite pagando R$105/mês → baseline = Itaú Infinite sem clube (único cartão)
- Usuário tem C6 Carbon isento (2,5 pts/USD) e BRB DUX pagando R$140/mês → baseline = C6 Carbon (custo zero, maior taxa entre os gratuitos)

### Milhas extras
Tudo que só existe porque o usuário paga:
- **Clube fixo**: milhas mensais do plano (usar valores com/sem Itaú conforme cartão principal do usuário)
- **Bônus campanha***: % extra sobre acúmulo do cartão co-branded Itaú (requer cartão + clube)
- **Bônus transferência**: % extra sobre transferências externas (requer clube)
- **Bônus Modo LATAM (Nubank)**: 10% permanente sobre transferências automáticas

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
# Determinar tipo do cartão no cenário
cartaoIsItau = cartao.tipo == "direct"

# ⚠️ IMPORTANTE: Para o bench, cada cenário simula um setup ISOLADO.
# Se o cenário usa cartão Itaú → benefícios "com Itaú" se aplicam.
# Se o cenário usa cartão transfer (C6, Nubank, etc.) SEM nenhum Itaú → benefícios "sem Itaú".
# Se o cenário usa cartão transfer MAS o usuário TAMBÉM tem Itaú → "com Itaú".
# Documentar essa premissa no dashboard.

temItauNoCenario = cartaoIsItau || cenario.inclui_cartao_itau

# Milhas fixas do clube (diferente com/sem Itaú)
clubMi = temItauNoCenario ? clube.milhas_com_itau : clube.milhas_sem_itau

# Taxa efetiva com clube
if cartaoIsItau:
    # Cartões direct recebem bônus de campanha* (recorrente, sujeita a renovação)
    taxaEfetiva = cartao.taxa_base × (1 + campanha_pct / 100)
else:
    # Cartões transfer recebem bônus de transferência do clube
    bonusTransf = temItauNoCenario ? clube.bonus_transf_com_itau : clube.bonus_transf_sem_itau
    taxaEfetiva = cartao.taxa_base × (1 + bonusTransf)

# Cálculo
cardMi = USD_gastos × taxaEfetiva
total = cardMi + clubMi
extras = total − baseline_milhas
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

Aplicável apenas quando o usuário tem cartão "direct" (Itaú LATAM Pass):

```
# Detectar automaticamente a partir do extrato
acumuloBase = soma de milhas tipo "A" da fonte do cartão Itaú no mês
bonusCampanha = soma de milhas tipo "B" da fonte do cartão Itaú no mês
campanha_pct = bonusCampanha ÷ acumuloBase × 100
```

Se > 0% em um mês, há campanha ativa. Se o usuário não tem cartão Itaú, este cálculo não se aplica.

## Carência

Primeiro mês do extrato sem dados do cartão principal = carência.
Regra:
```
# Genérico — funciona para qualquer cartão principal (não apenas Itaú)
cartaoPrincipalFonte = identificar_fonte(config.cartao_principal)
carencia = idx === 0 && acumulo_base_do_cartao_principal === 0
```
Excluído de todos os cálculos de ROI.

> **Nota**: O cartão principal pode ser qualquer tipo (direct ou transfer). A detecção verifica se houve acúmulo base daquele cartão no primeiro mês, independente de qual cartão seja.

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
