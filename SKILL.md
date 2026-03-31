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
> - LATAM Pass Itaú (Infinite, Black ou Platinum)
> - C6 Carbon
> - The One (Itaú)
> - BRB DUX
> - Outro (especifique taxa de acúmulo pts/USD e anuidade)

### 1.3 Anuidade
> Qual a anuidade do cartão? Tem isenção por gasto ou investimento?

### 1.4 Clube LATAM Pass
> Você assina o Clube LATAM Pass? Se sim, qual plano?
> - Sem Clube
> - Base (R$40,90/mês, 1.000 mi)
> - Base+Embarque (R$90,80/mês, 1.000 mi + 750 PQ)
> - Base+Acelere (R$187,80/mês, 5.500 mi)
> - Base+Turbo (R$356,80/mês, 11.500 mi)
> - Base+Turbo+Embarque (R$406,70/mês, 11.500 mi + 750 PQ)

### 1.5 Categoria Elite
> Qual sua categoria no LATAM Pass? (Padrão, Gold, Platinum, Black, Black Signature)

### 1.6 Outros cartões
> Tem outros cartões que transferem pontos pro LATAM? (C6, IUPP, etc.)

### 1.7 Extrato
> Envie screenshots do extrato de milhas do app LATAM Pass, ou cole os dados manualmente.
> Preciso de: mês, fonte, tipo (acúmulo/bônus), quantidade de milhas.

### 1.8 Câmbio
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
| LATAM Pass Clube | Milhas fixas mensais do clube |
| C6 Bank Atomos | Transferência de pontos Átomos → LATAM (1:1) |
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

### Baseline
C6 Carbon sem clube: 2,5 pts/USD, anuidade R$0, custo zero.
Se o usuário não tem C6 Carbon, usar o cartão de menor custo dele como baseline.

### Milhas extras (geradas pelo investimento)
- **Clube fixo**: milhas mensais do plano
- **Bônus campanha***: % extra sobre acúmulo do cartão co-branded (requer cartão Itaú + clube)
- **Bônus transferência**: % extra sobre transferências externas (requer clube)

### Externas
Acúmulo base de fontes que não dependem do investimento.

### Detecção de campanhas
```
campanha_pct = itauBonus ÷ itauBase × 100
```

### Carência
Primeiro mês sem dados do cartão principal = carência. Excluído dos cálculos de ROI.

## Passo 5: Fórmulas

### ROI unificado (todas as páginas)
```
ROI = (milhas_extras × MKT − custo_extra) ÷ custo_extra × 100
```

- **MKT**: R$ 0,025/milha (cotação mercado, Balcão de Milhas). Pesquisar valor atualizado se possível.
- **milhas_extras**: total gerado − baseline
- **custo_extra**: anuidade + clube − custo baseline

### R$/milha extra
```
R$/mi = custo_total ÷ milhas_extras
```

### Bench
Para cada combinação cartão × clube, dado o gasto do último mês:
1. Milhas LATAM = taxa efetiva × USD + milhas fixas clube
2. Custo = anuidade + clube
3. Extras = total − baseline
4. ROI incremental

### Taxas efetivas COM clube

Consultar `references/cards.md` para taxas atualizadas. Exemplo:

| Cartão | Sem Clube | Com Clube |
|---|---|---|
| LATAM Infinite | 2,5 mi/USD | 3,75 mi/USD (*campanha +50%) |
| C6 Carbon | 2,5 pts/USD | 3,375 pts/USD (clube +35%) |
| The One | 3,0 pts/USD | 4,05 pts/USD (clube +35%) |
| BRB DUX | 5,0 pts/USD | 6,75 pts/USD (clube +35%) |

## Passo 6: Estrutura do Dashboard

### Aba Temporal
- AreaChart evolução acumulada com ReferenceArea (faixas de campanha)
- BarChart empilhado: Baseline × Extras × Externas
- Tabela de bônus detectados

### Aba ROI
- ComposedChart: Valor Extras vs Custo (Area + Line)
- BarChart R$/milha extra mensal (gradiente + ReferenceLine MKT)
- ComposedChart R$/milha extra acumulado (Area + ReferenceLine MKT)
- Tabela de detalhes mensais

### Aba Bench
- Card baseline
- Card plano atual
- Lista de cenários ordenados por ROI (expandíveis)
- Premissas documentadas

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
7. [ ] Baseline correto (menor custo)
8. [ ] Bench ordenado por ROI decrescente
9. [ ] Asterisco (*) em campanhas recorrentes
10. [ ] ReferenceLine visível nos gráficos (domínio Y inclui MKT)

## Passo 9: Output

Salvar em `personal/latam-milhas-roi.jsx` (local) e/ou `/mnt/user-data/outputs/latam-milhas-roi.jsx` (Claude.ai).

## Atualização mensal

1. Ler output existente
2. Adicionar transações ao array TX
3. Adicionar câmbio PTAX ao objeto UM
4. Atualizar saldo BAL
5. Verificar campanha ativa
6. Re-validar soma
7. Usar `str_replace` — NÃO recriar o arquivo
