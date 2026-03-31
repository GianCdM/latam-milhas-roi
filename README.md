# LATAM Pass Milhas & ROI Dashboard

Skill para Claude que gera um dashboard React interativo de análise de ROI de milhas LATAM Pass.

## O que faz

- Analisa seu extrato de milhas LATAM Pass
- Calcula ROI do investimento em cartão + Clube LATAM Pass
- Compara cenários entre cartões (LATAM Itaú, C6 Carbon, The One, BRB DUX, Centurion)
- Detecta campanhas de bônus automaticamente
- Gera dashboard interativo com 4 abas: Temporal, ROI, Bench, Fontes

## Como usar

### No Claude.ai (mais simples)

1. Abra uma conversa no Claude.ai
2. Diga: "Quero analisar meu extrato de milhas LATAM Pass"
3. O Claude vai fazer as perguntas necessárias (saldo, cartão, clube, extrato)
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
│   ├── cards.md                  # Tabela de cartões (taxas, anuidades, benefícios)
│   ├── clubs.md                  # Tabela de clubes LATAM Pass (preços, milhas, bônus)
│   └── formulas.md               # Fórmulas de ROI, R$/milha, bench
├── templates/
│   ├── config-example.json       # Exemplo de configuração pessoal
│   └── transactions-example.json # Exemplo de extrato
├── scripts/
│   └── validate.py               # Script de validação de soma
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

2. Edite `personal/config.json` com seus dados (cartão, clube, saldo)
3. Preencha `personal/transactions.json` com seu extrato

Ou simplesmente converse com o Claude — ele faz as perguntas e gera tudo.

## Validação

```bash
python scripts/validate.py personal/transactions.json --saldo 415531
```

## Fórmula do ROI

```
ROI = (milhas_extras × R$0,025 − custo) ÷ custo × 100
```

- **Milhas extras**: o que você não teria sem pagar clube/anuidade
- **R$ 0,025**: cotação de mercado (Balcão de Milhas)
- **Custo**: anuidade do cartão + clube mensal

## Cartões suportados

| Cartão | Taxa nac. | Taxa int. | Com Clube |
|---|---|---|---|
| LATAM Infinite | 2,5 mi/USD | 3,5 mi/USD | 3,75* |
| C6 Carbon | 2,5 pts/USD | 2,5 pts/USD | 3,375 |
| The One | 3,0 pts/USD | 3,5 pts/USD | 4,05 |
| BRB DUX | 5,0 pts/USD | 7,0 pts/USD | 6,75 |
| Amex Centurion | 5,0 pts/USD | 7,0 pts/USD | 6,75 |

\* Campanha recorrente, sujeita a renovação

## Licença

MIT
