# Será que meu investimento em milhas vale a pena?

*Como usei AI pra descobrir se estou jogando dinheiro fora com Clube LATAM Pass + cartão co-branded*

---

## O problema

Pessoal, vou ser direto: eu gasto mais de R$400/mês entre Clube LATAM Pass (Base+Turbo+Embarque) e anuidade do cartão Itaú LATAM Infinite. E por um bom tempo eu simplesmente... não sabia se isso fazia sentido.

O app do LATAM Pass te mostra um extrato cru. Tipo: "você ganhou 11.500 milhas do Clube", "você ganhou 3.955 milhas do Itaú LATAM Infinite". E aí? Isso é bom? Isso compensa o que eu pago? Quanto estou pagando por milha? Se eu tivesse um cartão sem anuidade, estaria melhor?

Essas perguntas ficavam na minha cabeça todo mês quando eu via a cobrança do clube. E a verdade é que a maioria das pessoas que acumula milhas provavelmente nunca fez essa conta.

## O que tentei antes

A primeira reação foi a planilha. Comecei a montar uma no Google Sheets: mês, fonte, milhas, custo. Funcionou por uns 2 meses e depois ficou desatualizada. A frieza da planilha não me dava a visão que eu queria — tipo entender o impacto das campanhas de bônus, ou comparar cenários entre cartões diferentes.

Pesquisei calculadoras de milhas online também. A maioria é genérica demais: você coloca quanto gasta por mês e ela te diz quantas milhas ganha. Não considera que eu tenho Clube + cartão co-branded + campanhas de bônus que mudam a cada trimestre + transferências de outros programas. Meu cenário é mais complexo do que um slider de "gasto mensal" resolve.

## A ideia — e se a AI fizesse isso pra mim?

Aí veio a ideia: ao invés de construir um app ou manter uma planilha, e se eu descrevesse o problema bem o suficiente pra que uma AI gerasse a análise automaticamente?

O conceito é o de uma **skill** — uma instrução estruturada que qualquer AI pode seguir. Não é um SaaS, não é um app que você instala. É mais uma receita: "dado meu extrato, meu cartão e meu clube, gere um dashboard de ROI com essas fórmulas e essas visualizações".

O approach foi: investir tempo descrevendo o problema (classificação de milhas, fórmulas de ROI, detecção de campanhas, benchmark entre cartões) e deixar a AI executar. A vantagem é que quando meus dados mudam — novo mês, novo cartão, nova campanha — eu só preciso alimentar os dados e a skill gera tudo de novo.

## Como funciona

O fluxo é simples:

1. **Onboarding**: a AI pergunta qual cartão você usa, qual clube, qual seu saldo, e pede o extrato de milhas
2. **Classificação**: cada linha do extrato é categorizada — milhas "baseline" (que você teria de graça), "extras" (que só existem porque você paga), e "externas" (voos, Amazon, etc.)
3. **Detecção de campanhas**: a skill identifica automaticamente quando há bônus ativo (ex: campanha Itaú +50%) comparando acúmulo base vs bônus
4. **Cálculo de ROI**: quanto paguei, quanto gerei de milha extra, qual o custo por milha vs o mercado (R$0,025/mi no Balcão de Milhas)
5. **Dashboard**: 4 abas interativas com gráficos — tudo num único arquivo HTML

![Dashboard — KPIs e evolução temporal](screenshot-temporal.jpg)
*KPIs principais: saldo, custo, R$/milha extra e ROI. Gráfico mostra evolução acumulada com faixas de campanha.*

## O que descobri

Aqui ficou interessante. Algumas coisas eu já esperava, outras me surpreenderam:

**O ROI é positivo, mas não tanto quanto eu imaginava.** No cenário dos dados demo, o custo por milha extra ficou em R$0,022 — abaixo do mercado (R$0,025), o que significa ROI positivo de ~16%. Mas não é aquele ROI absurdo que justifica qualquer investimento.

**Meses sem campanha de bônus são caros.** Quando não tem campanha ativa do Itaú, o custo por milha sobe significativamente. A campanha de +50% (ou +70% que tinha antes) é o que faz a conta fechar. Sem ela, o cenário muda completamente.

**O bench é revelador.** A aba de benchmark compara 18 combinações de cartão × clube, ordenadas por ROI. Tem cenário onde o ROI passa de +300% (cartão barato + clube mínimo) e cenário onde é negativo (cartão caro + clube caro com pouco gasto).

![Dashboard — Aba Bench](screenshot-bench.jpg)
*Comparação entre cenários: baseline (custo zero), plano atual, e todos os outros cenários possíveis ordenados por ROI.*

Isso é o tipo de análise que eu nunca teria feito na mão. São muitas variáveis: taxa do cartão com e sem clube, anuidade com e sem isenção, milhas fixas do clube, bônus de transferência...

## O que vem por aí

A skill já funciona, mas tem espaço pra melhorar:

- **Pesquisa de mercado automatizada com Perplexity (Sonar)**: ao invés de eu manter manualmente as taxas de cada cartão, um agente de pesquisa pode buscar as condições atuais — anuidade, taxa de acúmulo, promoções ativas
- **Simulador de gasto variável**: "e se eu gastasse R$5k/mês no cartão ao invés de R$3k?" — ver como o ROI muda com diferentes perfis de gasto
- **Mais cartões no bench**: BRB DUX, Centurion, e outros que fazem sentido pra quem acumula LATAM

## Pra fechar

A AI não substituiu minha decisão — me deu os dados pra decidir melhor. Antes eu tinha uma sensação vaga de "acho que vale a pena". Agora eu sei exatamente o custo por milha, o ROI acumulado, e o impacto de cada cenário.

Se você acumula milhas e paga por isso (clube, anuidade, ou ambos), vale entender se o investimento tá fazendo sentido. A conta pode te surpreender — pra melhor ou pra pior.

O repo é aberto e qualquer um pode usar:
- **Demo interativa**: [giancdm.github.io/latam-milhas-roi](https://giancdm.github.io/latam-milhas-roi/)
- **Código fonte**: [github.com/GianCdM/latam-milhas-roi](https://github.com/GianCdM/latam-milhas-roi)

---

*Dados do dashboard são fictícios (demo). A skill gera o dashboard personalizado com seus dados reais.*
