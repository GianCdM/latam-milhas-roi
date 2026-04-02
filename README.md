# LATAM Pass Milhas & ROI Dashboard

Skill para Claude que gera um dashboard React interativo de análise de ROI de milhas LATAM Pass.

## O que faz

- Analisa seu extrato de milhas LATAM Pass
- Calcula ROI do investimento em cartão + Clube LATAM Pass
- Compara cenários entre cartões (LATAM Itaú, C6 Carbon, Nubank Ultravioleta, The One, BRB DUX, Centurion)
- Detecta campanhas de bônus automaticamente
- Considera isenção de anuidade (por gasto, investimento ou promoção)
- Diferencia benefícios do Clube com/sem cartão LATAM Pass Itaú
- Gera dashboard interativo com 4 abas: Temporal, ROI, Bench, Fontes

## Como usar

### No Claude.ai (mais simples)

1. Abra uma conversa no Claude.ai
2. Diga: "Quero analisar meu extrato de milhas LATAM Pass"
3. O Claude vai fazer as perguntas necessárias (saldo, cartão, clube, isenções, extrato)
4. Ele gera o dashboard como artefato interativo

### Com a Skill instalada (melhor experiência)

1. Baixe este repositório
2. Copie a pasta para suas skills do Claude
3. Abra uma conversa — o Claude vai usar a skill automaticamente
4. Seus dados ficam em `personal/` (nunca sobem pro GitHub)

## Estrutura

```
latam-milhas-dashboard/
├── SKILL.md                      # Instruções para o Claude
├── references/
│   ├── cards.md                  # Tabela de cartões (taxas, anuidades, isenções, benefícios)
│   ├── clubs.md                  # Tabela de clubes LATAM Pass (preços, milhas, bônus, com/sem Itaú)
│   └── formulas.md               # Fórmulas de ROI, R$/milha, bench, discussão ROI teórico vs. real
├── templates/
│   ├── config-example.json       # Exemplo de configuração pessoal (com isenções)
│   └── transactions-example.json # Exemplo de extrato
├── scripts/
│   └── validate.py               # Script de validação de soma
├── articles/
│   └── substack-milhas-roi.md    # Artigo sobre o projeto
├── personal/                     # Seus dados (no .gitignore)
│   ├── config.json               # Sua config
│   ├── transactions.json         # Seu extrato
│   └── latam-milhas-roi.jsx      # Dashboard gerado
├── .gitignore
└── README.md
```

## Configuração

1. Copie os templates:
```bash
cp templates/config-example.json personal/config.json
cp templates/transactions-example.json personal/transactions.json
```

2. Edite `personal/config.json` com seus dados (cartão, clube, saldo, isenções)
3. Preencha `personal/transactions.json` com seu extrato

Ou simplesmente converse com o Claude — ele faz as perguntas e gera tudo.

## Validação

```bash
python scripts/validate.py personal/transactions.json --saldo SEU_SALDO_AQUI
```

## Fórmula do ROI

```
ROI = (milhas_extras × R$0,025 − custo) ÷ custo × 100
```

- **Milhas extras**: o que você não teria sem pagar clube/anuidade
- **R$ 0,025**: cotação de mercado — venda (Balcão de Milhas, conservador)
- **Custo**: anuidade do cartão (se paga) + clube mensal
- **ROI real**: depende de como você usa a milha (venda vs. resgate). Resgate em passagens pode valer 2-6× mais.

## Cartões suportados

| Cartão | Taxa nac. | Taxa int. | Com Clube (Turbo) | Tipo |
|---|---|---|---|---|
| LATAM Infinite/Black | 2,5 mi/USD | 3,5 mi/USD | 3,75* (camp. +50%) | direct |
| LATAM Platinum | 2,0 mi/USD | 3,0 mi/USD | 3,00* (camp. +50%) | direct |
| LATAM Gold | 1,6 mi/USD | — | 2,40* (camp. +50%) | direct |
| LATAM Internacional | 1,3 mi/USD | — | 1,95* (camp. +50%) | direct |
| C6 Carbon | 2,5 pts/USD | 2,5 pts/USD | 3,375 (+35% c/ Itaú) | transfer |
| Nubank Ultravioleta | 2,2 pts/USD | 2,2 pts/USD | 2,97 (+35% c/ Itaú) | transfer |
| Nubank UV (Modo LATAM) | 2,42 pts/USD | 2,42 pts/USD | 3,27 (+35% c/ Itaú) | transfer |
| The One | 3,0 pts/USD | 3,5 pts/USD | 4,05 (+35% c/ Itaú) | transfer |
| BRB DUX | 5,0 pts/USD | 7,0 pts/USD | 6,75 (+35% c/ Itaú) | transfer |
| Amex Centurion | 5,0 pts/USD | 7,0 pts/USD | 6,75 (+35% c/ Itaú) | transfer |

\* Campanha recorrente, sujeita a renovação

## Licença

MIT
