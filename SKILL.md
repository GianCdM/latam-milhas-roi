---
name: latam-milhas-dashboard
user-invocable: true
description: "Gera um dashboard React interativo de análise de ROI de milhas LATAM Pass. Use quando o usuário mencionar milhas LATAM, ROI de milhas, Clube LATAM Pass, análise de custo de milhas, acúmulo de milhas, dashboard de milhas, comparação de cartões de milhas, ou quiser visualizar/analisar seu extrato de milhas LATAM Pass. Também use quando pedir para atualizar dados de milhas, adicionar novos meses ao extrato, ou comparar cenários de cartão+clube."
---

# LATAM Pass Milhas & ROI Dashboard

Gera um dashboard React (.jsx) com 4 abas (Temporal, ROI, Bench, Fontes) para análise de acúmulo de milhas LATAM Pass e ROI do investimento em cartão + clube.

## Passo 0: Detectar contexto do usuário (CRÍTICO)

Antes de qualquer coisa, verificar se já existem dados pessoais do usuário:

```bash
# 1. Checar se existe output anterior
ls personal/latam-milhas-roi.jsx 2>/dev/null || ls /mnt/user-data/outputs/latam-milhas-roi*.jsx 2>/dev/null

# 2. Checar se existe config pessoal
ls personal/config.json 2>/dev/null
```

### Se encontrou output anterior:
- Ler o arquivo existente com `view`
- Usar como template: manter toda a estrutura, componentes, estilos e lógica
- Apenas atualizar os dados solicitados com `str_replace`
- NÃO reescrever do zero

### Se encontrou config.json mas sem output:
- Ler o config.json para obter dados do usuário
- Gerar o dashboard seguindo as instruções abaixo

### Se NÃO encontrou nada (usuário novo):
- Iniciar o fluxo de onboarding (Passo 1)
- Fazer as perguntas necessárias para gerar o config.json
- Depois gerar o dashboard

## Passo 1: Onboarding (apenas para novos usuários)

Pergunte ao usuário, na ordem:

### 1.1 Saldo atual
> Qual seu saldo atual de milhas LATAM Pass?

### 1.2 Cartão principal
> Qual cartão de crédito você usa para acumular milhas? Opções comuns:
> - LATAM Pass Itaú (Infinite, Black, Platinum, Gold ou Internacional)
> - C6 Carbon
> - Nubank Ultravioleta
> - The One (Itaú)
> - BRB DUX
> - Outro (especifique taxa de acúmulo pts/USD e anuidade)

### 1.3 Anuidade e isenção
> Qual a anuidade do cartão? **Você paga ou tem isenção?**
> Se tem isenção, é por:
> - Gasto mínimo mensal (qual valor?)
> - Investimento no banco (qual valor investido?)
> - Promoção temporal (até quando?)
> - Outro motivo
>
> ⚠️ Isso é crítico para o cálculo de ROI — anuidade isenta = custo zero.

### 1.4 Clube LATAM Pass
> Você assina o Clube LATAM Pass? Se sim, qual plano?
> - Sem Clube
> - Base (R$40,90/mês, 1.000 mi)
> - Base+Mais (R$78,80/mês, 2.000–2.200 mi)
> - Base+Embarque (R$90,80/mês, 1.000 mi + 500–750 PQ)
> - Base+Acelere (R$187,80/mês, 5.000–5.500 mi)
> - Base+Turbo (R$356,80/mês, 10.000–11.500 mi)
> - Base+Turbo+Embarque (R$406,70/mês, 10.000–11.500 mi + 500–750 PQ)
>
> Nota: milhas e bônus variam conforme você tenha ou não cartão LATAM Pass Itaú.

### 1.5 Categoria Elite
> Qual sua categoria no LATAM Pass? (Padrão, Gold, Platinum, Black, Black Signature)

### 1.6 Outros cartões
> Tem outros cartões que transferem pontos pro LATAM? (C6, Nubank Ultravioleta, IUPP, BRB, etc.)
>
> **Para cada cartão adicional, pergunte sobre isenção de anuidade** (mesma lógica do 1.3).

### 1.7 Nubank Ultravioleta (se aplicável)
> Se mencionou Nubank Ultravioleta:
> - Está com o Modo LATAM Pass ativado? (transferência automática + 10% bônus + PQ)
> - Anuidade: paga (R$89/mês) ou isento? Se isento, por investimento (≥R$50k) ou gasto (≥R$8k/mês)?

### 1.8 Extrato
> Envie screenshots do extrato de milhas do app LATAM Pass, ou cole os dados manualmente.
> Preciso de: mês, fonte, tipo (acúmulo/bônus), quantidade de milhas.

### 1.9 Câmbio
> Vou usar a PTAX média de cada mês. Se tiver valores específicos, me passe.

Após coletar, salvar em `personal/config.json` seguindo o formato de `templates/config-example.json`.

## Passo 2: Mapear transações

Classificar cada linha do extrato:
- `d`: mês (YYYY-MM)
- `s`: fonte (ex: "Itaú LATAM Infinite", "C6 Bank Atomos", "LATAM Pass Clube")
- `t`: "A" = acúmulo base, "B" = bônus
- `m`: milhas

### Fontes conhecidas
| Fonte | Tipo |
|---|---|
| Itaú LATAM Infinite | Cartão co-branded (acumula direto no LATAM Pass) |
| Itaú LATAM Black | Cartão co-branded (acumula direto no LATAM Pass) |
| Itaú LATAM Platinum | Cartão co-branded (acumula direto no LATAM Pass) |
| Itaú LATAM Gold | Cartão co-branded (acumula direto no LATAM Pass) |
| LATAM Pass Clube | Milhas fixas mensais do clube |
| C6 Bank Atomos | Transferência de pontos Átomos → LATAM (1:1) |
| Nubank Ultravioleta | Transferência de pontos Nubank → LATAM (1:1) |
| Nubank UV Modo LATAM | Transferência automática semanal (1:1 + 10% bônus) |
| IUPP Itaú | Transferência de pontos IUPP → LATAM |
| LATAM Airlines | Acúmulo por voos |
| LATAM Travel | Acúmulo por compras LATAM Travel |
| Amazon | Acúmulo via Amazon |
| BRB Curtaí | Transferência de pontos BRB → LATAM (1:1) |

## Passo 3: Validar total

```python
total = sum(t['m'] for t in transactions)
assert total == SALDO_INFORMADO, f"Diferença: {total - SALDO_INFORMADO}"
```

Se não bater, investigar com o usuário antes de prosseguir.

## Passo 4: Classificação de milhas para ROI

### Baseline (dinâmico)
Determinado automaticamente a partir do perfil do usuário:
1. Filtrar cartões com custo efetivo = R$0 (isenção por investimento, gasto ou promoção)
2. Se há cartões gratuitos → baseline = o de maior taxa de acúmulo (pts/USD)
3. Se nenhum é gratuito → baseline = o de menor custo mensal
4. Sempre SEM clube

> **Crítico**: Perguntar sobre isenção de anuidade no onboarding para cada cartão. Isso muda completamente o baseline e o ROI.

Ver algoritmo completo em `references/formulas.md` (seção "Baseline dinâmico").

### Milhas extras (geradas pelo investimento)
- **Clube fixo**: milhas mensais do plano (usar valores com/sem Itaú conforme o cartão principal)
- **Bônus campanha***: % extra sobre acúmulo do cartão co-branded (requer cartão Itaú + clube)
- **Bônus transferência**: % extra sobre transferências externas (requer clube)
- **Bônus Modo LATAM (Nubank)**: 10% permanente sobre transferências automáticas

### Externas
Acúmulo base de fontes que não dependem do investimento.

### Detecção de campanhas
```
# Aplicável apenas para cartões "direct" (Itaú LATAM Pass)
campanha_pct = bonusCartaoDirect ÷ acumuloBaseCartaoDirect × 100
```
Se > 0% em um mês, há campanha ativa. Ver formulas.md para detalhes.

### Carência
Primeiro mês do extrato sem acúmulo base do cartão principal = carência.
Funciona para qualquer cartão principal (direct ou transfer). Excluído dos cálculos de ROI.

## Passo 5: Fórmulas

Consultar `references/formulas.md` para todas as fórmulas detalhadas. Resumo:

### ROI unificado (todas as páginas)
```
ROI = (milhas_extras × MKT − custo_extra) ÷ custo_extra × 100
```

- **MKT**: R$ 0,025/milha padrão (conservador, baseado em venda no mercado). Pesquisar valor atualizado se possível.
- **Valor de resgate**: pode ser 2-6× maior que MKT de venda. Dashboard deve permitir ajustar.
- **milhas_extras**: total gerado − baseline
- **custo_extra**: anuidade cartão (se paga) + clube − custo baseline

### R$/milha extra
```
R$/mi = custo_total ÷ milhas_extras
```

### Bench
Para cada combinação cartão × clube, dado o gasto do último mês:
1. Determinar se cartão é Itaú (direct) ou transfer
2. Usar milhas do clube corretas (com/sem Itaú)
3. Usar bônus de transferência correto (com/sem Itaú)
4. Considerar isenção de anuidade se aplicável
5. Calcular milhas LATAM, custo, extras, ROI incremental

### Taxas efetivas COM clube (campanha Itaú +50%* para direct)

| Cartão | Sem Clube | Com Clube |
|---|---|---|
| LATAM Infinite/Black (nac.) | 2,5 mi/USD | 3,75 mi/USD (*campanha +50%) |
| LATAM Infinite/Black (int.) | 3,5 mi/USD | 5,25 mi/USD (*campanha +50%) |
| LATAM Platinum | 2,0 mi/USD | 3,00 mi/USD (*campanha +50%) |
| LATAM Gold | 1,6 mi/USD | 2,40 mi/USD (*campanha +50%) |
| LATAM Internacional | 1,3 mi/USD | 1,95 mi/USD (*campanha +50%) |
| C6 Carbon | 2,5 pts/USD | 3,375 pts/USD (clube +35% c/ Itaú) |
| Nubank Ultravioleta | 2,2 pts/USD | 2,86–2,97 pts/USD (clube +30-35%) |
| Nubank UV (Modo LATAM) | 2,42 pts/USD | 3,15–3,27 pts/USD (modo +10% + clube) |
| The One | 3,0 pts/USD | 4,05 pts/USD (clube +35% c/ Itaú) |
| BRB DUX | 5,0 pts/USD | 6,75 pts/USD (clube +35% c/ Itaú) |

## Passo 6: Estrutura do Dashboard

### Aba Temporal
- AreaChart evolução acumulada com ReferenceArea (faixas de campanha)
- BarChart empilhado: Baseline × Extras × Externas
- Tabela de bônus detectados

### Aba ROI
- ComposedChart: Valor Extras vs Custo (Area + Line)
- BarChart R$/milha extra mensal (gradiente + ReferenceLine MKT)
- ComposedChart R$/milha extra acumulado (Area + ReferenceLine MKT)
- Nota explicativa: "ROI baseado em valor de mercado (venda). Valor de resgate em passagens pode ser 2-6× maior."
- Tabela de detalhes mensais

### Aba Bench
- Card baseline
- Card plano atual
- Lista de cenários ordenados por ROI (expandíveis)
- Incluir: todos os cartões Itaú (Infinite, Black, Platinum, Gold, Internacional) + C6 Carbon + Nubank Ultravioleta + The One + BRB DUX + Centurion
- Para cada cenário, mostrar com e sem isenção de anuidade
- Premissas documentadas (incluindo se usa valores com/sem Itaú)

### Aba Fontes
- PieChart por fonte
- Cards por fonte com % e barra

## Passo 7: Stack técnica

- React (JSX standalone, hooks: useState, useMemo)
- Recharts (AreaChart, BarChart, ComposedChart, PieChart, ReferenceLine, ReferenceArea)
- Google Fonts: Space Mono + Inter
- Tema dark
- Mobile-first (maxWidth: 520px)

### Gradiente de cores para R$/milha
```js
function cpmColor(value) {
  if (value == null) return "#475569";
  if (value >= MKT) return "#ef4444";     // acima do mercado = vermelho
  const t = Math.min(value / MKT, 1);
  return `rgb(${Math.round(4+t*106)},${Math.round(120+t*111)},${Math.round(87+t*96)})`;
}
```

## Passo 8: Validação

1. [ ] Soma de transações bate com saldo informado
2. [ ] Mês de carência detectado e excluído
3. [ ] Campanhas detectadas (% bônus por mês)
4. [ ] Cap de bônus 30.000 milhas/mês respeitado
5. [ ] MKT usa cotação de mercado (pesquisar atualizada)
6. [ ] ROI consistente nas 3 páginas
7. [ ] Baseline correto (menor custo, considerando isenções)
8. [ ] Bench ordenado por ROI decrescente
9. [ ] Bench usa valores corretos com/sem Itaú para cada cenário
10. [ ] Asterisco (*) em campanhas recorrentes
11. [ ] ReferenceLine visível nos gráficos (domínio Y inclui MKT)
12. [ ] Nubank Ultravioleta com/sem Modo LATAM tratado corretamente
13. [ ] Isenção de anuidade refletida no custo de cada cenário

## Passo 9: Output

Salvar em `personal/latam-milhas-roi.jsx` (local) e/ou `/mnt/user-data/outputs/latam-milhas-roi.jsx` (Claude.ai).

## Atualização mensal

1. Ler output existente
2. Adicionar transações ao array TX
3. Adicionar câmbio PTAX ao objeto UM
4. Atualizar saldo BAL
5. Verificar campanha ativa (% pode ter mudado)
6. Re-validar soma
7. Usar `str_replace` — NÃO recriar o arquivo
