# Gasto R$400/mês com milhas. Fiz a AI calcular se tô jogando dinheiro fora.

*Como construí uma skill de AI que analisa meu extrato LATAM Pass e me diz se o investimento em Clube + cartão co-branded realmente compensa*

---

## 1. O problema

Pessoal, vou ser direto: eu gasto mais de **R$400/mês** entre Clube LATAM Pass e anuidade do cartão Itaú. E por um bom tempo eu simplesmente... não sabia se isso fazia sentido.

Sou engenheiro de software e EM. Meu instinto natural é olhar pra qualquer problema e pensar "isso deveria ter um dashboard". Mas o app do LATAM Pass te mostra um extrato cru — "você ganhou 11.500 milhas do Clube", "você ganhou 3.955 milhas do Itaú LATAM". E aí? Isso é bom? Compensa o que eu pago? Quanto estou pagando por milha? Se eu tivesse um cartão sem anuidade, estaria melhor?

Essas perguntas ficavam na minha cabeça todo mês quando eu via a cobrança do clube. E a verdade é que a maioria das pessoas que acumula milhas provavelmente nunca fez essa conta. Eu incluso — até agora.

## 2. O que não funcionou

**Planilha.** Comecei uma no Google Sheets: mês, fonte, milhas, custo. Funcionou por 2 meses e depois ficou desatualizada (surpresa de ninguém). A planilha não me dava a visão que eu queria — tipo entender o impacto das campanhas de bônus, ou comparar cenários entre cartões diferentes.

**Calculadoras de milhas online.** A maioria é genérica demais: você coloca quanto gasta por mês e ela te diz quantas milhas ganha. Não considera Clube + cartão co-branded + campanhas que mudam a cada trimestre + transferências de outros programas. Meu cenário é mais complexo do que um slider de "gasto mensal" resolve.

## 3. A ideia: e se a AI fizesse isso pra mim?

Ao invés de construir um app ou manter uma planilha, e se eu descrevesse o problema **bem o suficiente** pra que uma AI gerasse a análise automaticamente?

O conceito é o de uma **skill** — uma instrução estruturada que qualquer AI pode seguir. Não é um SaaS, não é um app. É mais uma receita: *"dado meu extrato, meu cartão e meu clube, gere um dashboard de ROI com essas fórmulas e essas visualizações"*.

O approach: investir tempo descrevendo o problema (classificação de milhas, fórmulas de ROI, detecção de campanhas, benchmark entre cartões) e deixar a AI executar. Quando meus dados mudam — novo mês, novo cartão, nova campanha — eu só alimento os dados e a skill gera tudo de novo.

Parece simples, mas o trabalho real é na engenharia do problema, não na execução. Faz sentido?

## 4. Como a skill funciona

O fluxo tem 5 etapas:

**1. Onboarding** — a AI pergunta qual cartão você usa, qual clube, se tem isenção de anuidade, e pede o extrato de milhas. Parece básico, mas a pergunta sobre isenção é crítica: se seu cartão tem anuidade grátis (por investimento, gasto mínimo, promoção), isso muda completamente o cálculo.

**2. Classificação** — cada linha do extrato é categorizada:
- **Baseline**: milhas que você teria de graça, sem pagar nada (o cartão mais barato com custo zero)
- **Extras**: milhas que só existem porque você paga (clube fixo + bônus campanha + bônus transferência)
- **Externas**: acúmulo independente do investimento (voos, Amazon, etc.)

**3. Detecção de campanhas** — a skill identifica automaticamente quando há bônus ativo (ex: campanha Itaú +50%) comparando acúmulo base vs bônus no extrato. Sem eu precisar informar nada.

**4. Cálculo de ROI** — quanto paguei, quanto gerei de milha extra, qual o custo por milha vs o mercado (**R$0,025/mi** no Balcão de Milhas, referência conservadora de venda).

**5. Dashboard** — 4 abas interativas com gráficos (Temporal, ROI, Bench, Fontes), tudo num único arquivo HTML com React + Recharts.

![Dashboard — KPIs e evolução temporal](screenshot-temporal.jpg)
*KPIs principais: saldo, custo, R$/milha extra e ROI. Gráfico mostra evolução acumulada com faixas de campanha.*

## 5. O que descobri

Algumas coisas eu já esperava, outras me surpreenderam de verdade:

**O ROI é positivo, mas não tanto quanto eu imaginava.** O custo por milha extra ficou em **R$0,021** — abaixo do mercado (R$0,025), o que dá um ROI de **+17%**. Positivo, sim. Mas não é aquele ROI absurdo que justifica investir sem pensar.

**Sem campanha de bônus, a conta não fecha.** Quando não tem campanha ativa do Itaú, o custo por milha sobe pesado. A campanha de +50% (ou +70% que tinha antes) é literalmente o que faz o investimento valer. Isso mudou como eu decido se renovo o clube a cada trimestre — agora eu olho se a campanha foi renovada antes de manter.

**O bench é a aba mais reveladora.** São **60 combinações** de cartão × clube, ordenadas por ROI. Tem cenário onde o ROI passa de +90% (BRB DUX + Base) e cenário onde é negativo (cartão caro + clube caro com pouco gasto). Isso é o tipo de análise que eu nunca teria feito na mão.

![Dashboard — Aba Bench](screenshot-bench.jpg)
*60 cenários comparados: baseline (C6 Carbon, custo zero), plano atual, e todos os outros cenários ordenados por ROI.*

**O baseline dinâmico faz diferença.** A skill detecta automaticamente qual é o cartão de custo zero com maior taxa de acúmulo do usuário e usa como referência. Tudo que passa desse baseline = milha extra que você está pagando pra ter. Sem esse conceito, a conta de ROI não faz sentido.

## 6. Quer testar?

O repo é aberto. Se você acumula milhas LATAM e paga por isso (clube, anuidade, ou ambos), vale entender se o investimento tá fazendo sentido. A conta pode te surpreender — pra melhor ou pra pior.

**Checklist pra rodar:**

1. Acesse a **demo interativa** pra ver o dashboard com dados fictícios: [giancdm.github.io/latam-milhas-roi](https://giancdm.github.io/latam-milhas-roi/)
2. Clone o **repo**: [github.com/GianCdM/latam-milhas-roi](https://github.com/GianCdM/latam-milhas-roi)
3. Copie os templates de `templates/` pra `personal/` e preencha com seus dados
4. Abra uma conversa com a AI e diga "Quero analisar meu extrato de milhas LATAM Pass"
5. A skill faz o onboarding, classifica tudo e gera o dashboard personalizado

A skill roda com Claude (projects/skills) ou qualquer AI que suporte instruções estruturadas. Seus dados ficam em `personal/` e nunca sobem pro GitHub.

## 7. O que vem por aí

A skill já funciona, mas já estou trabalhando em:

- **Pesquisa de mercado automatizada**: ao invés de manter manualmente as taxas de cada cartão, um agente de pesquisa busca condições atuais — anuidade, taxa de acúmulo, promoções ativas. Já estou testando com Perplexity Sonar pra isso.
- **Simulador de gasto variável**: "e se eu gastasse R$5k/mês ao invés de R$3k?" — ver como o ROI muda com diferentes perfis de gasto
- **Alerta de campanha**: monitorar se a campanha de bônus Itaú foi renovada (a LATAM muda isso a cada trimestre e não avisa direito)

## Pra fechar

A AI não substituiu minha decisão — me deu os dados pra decidir melhor. Antes era uma sensação vaga de "acho que vale a pena". Agora eu sei que **sem campanha de bônus ativa, meu ROI fica negativo**. Isso por si só já justificou o tempo que gastei construindo a skill.

Se você tá no mesmo barco — pagando clube, anuidade, ou ambos — vale rodar os números. O repo tá aberto, é só usar.

---

*Dados do dashboard na demo são fictícios. A skill gera o dashboard personalizado com seus dados reais.*
