import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações da página
st.set_page_config(page_title="Simulação Monte Carlo - Falhas Críticas por Versão", layout="centered")

st.title("Simulação de Monte Carlo com Distribuição Binomial - Silvia Branco")
st.subheader("Qualidade de Software - Estimativa de Falhas Críticas por Versão de Software")

st.markdown("""
Esta aplicação simula o número de **falhas críticas** em versõs de uma aplicativo após o deploy, 
usando a **distribuição binomial** e a **técnica de Simulação de Monte Carlo**.
""")

# Entradas do usuário
n_funcionalidades = st.slider("Número de funcionalidades por versão", min_value=1, max_value=100, value=10)
n_deploys = st.slider("Número de deploys por versão", min_value=5, max_value=50, value=15)
p_falha = st.slider("Probabilidade de falha crítica por deploy (%)", min_value=1, max_value=20, value=5) / 100
n_simulacoes = st.slider("Número de versões simuladas", min_value=1000, max_value=50000, value=10000, step=1000)

# Simulação de Monte Carlo
st.markdown("### Simulação de Falhas Críticas por Versão")
st.write(f"Simulando {n_simulacoes} versões do APP com {n_funcionalidades} funcionalidades, "
         f"{n_deploys} deploys por versão e probabilidade de falha crítica de {p_falha * 100:.1f}%.")
np.random.seed(42)
falhas = np.random.binomial(n=n_deploys * n_funcionalidades, p=p_falha, size=n_simulacoes)

## Estatísticas
media = np.mean(falhas)
desvio = np.std(falhas)
prob_5_ou_mais = np.mean(falhas >= 5)

st.markdown("""
### Resultados Estatísticos
- Média de falhas por versão: **{:.2f}**
- Desvio padrão: **{:.2f}**
- Probabilidade de ao menos 5 falha crítica por versão: **{:.1f}%**
""".format(media, desvio, prob_5_ou_mais* 100))


# Gráfico de distribuição
st.markdown("### Distribuição do Número de Falhas Críticas por Versão de Software")

# Estilo do gráfico
sns.set_theme(style="whitegrid", font_scale=1)

fig, ax = plt.subplots(figsize=(20, 12))

# Histograma com Seaborn
sns.histplot(falhas, 
             bins=range(0, max(falhas) + 2), 
             kde=True, 
             color="steelblue", 
             edgecolor="black", 
             ax=ax)

# Rótulos das barras
counts, bins, _ = ax.hist(falhas, bins=range(0, max(falhas) + 2), alpha=0)
for count, x in zip(counts, bins):
    if count > 0:
        ax.text(x + 0.5, count + 0.5, int(count), ha='center', va='bottom', fontsize=12)

# Histograma e KDE
ax.set_title("Distribuição Binomial Simulada – Falhas Críticas por Versão", fontsize=14, weight='bold')
ax.set_xlabel("Número de Falhas Críticas", fontsize=12)
ax.set_ylabel("Frequência Observada", fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_xticks(range(0, max(falhas) + 1))

# Legenda
ax.legend(["KDE (Curva de densidade)", "Histograma"], loc='upper right')

st.pyplot(fig)

# Respoosta da Projeto AEDI
st.title("Cenário Realista: Probabilidade de ocorrência de falhas em uma nova versão de software após o deploy")

st.header("A) Modelo computacional que simule um Cenário Realista")

st.markdown("""
Uma versão de aplicativo geralmente representa um pacote de funcionalidades, correções ou mudanças que será liberado para o ambiente produtivo. Essa liberação pode ocorrer de forma única, com todas as alterações agrupadas, ou ser dividida em múltiplos deploys — por exemplo, por meio de *feature toggles* ou mesmo uma arquitetura de microserviços.

Em cenários com arquitetura distribuída, como microserviços, uma mesma versão de produto pode demandar múltiplos deploys. Por exemplo, a versão **v2.5.0** de um aplicativo bancário pode incluir mudanças em diferentes componentes, como o serviço de login, o serviço de notificações e o serviço de contas. Cada um desses componentes é implantado de forma independente.

Com foco em confiabilidade, o time responsável pela qualidade acompanha quantos desses deploys falham ou introduzem falhas críticas. Com base no histórico, foi estimada uma probabilidade aproximada de **5% de ocorrência de falha crítica por deploy**.

Nesse contexto, o total de oportunidades para a ocorrência de falhas em uma versão pode ser estimado por:""")

#st.markdown('<p style="text-align: center;">n = número de funcionalidades × número de deploys</p>', unsafe_allow_html=True)

st.latex(r"n = \text{número de funcionalidades} \times \text{número de deploys}")

st.markdown("""
A ocorrência de uma falha crítica em um desses deploys pode ser modelada como um evento binário: há falha (sucesso para o evento de interesse) ou não há falha (fracasso). Sendo assim, o número total de falhas críticas por versão pode ser modelado como uma variável aleatória binomial:
""")

st.latex(r"X \sim \text{Binomial}(n, p)")

st.markdown("""
**Onde:**  
- **n** representa o número de tentativas (deploys com funcionalidades);  
- **p** representa a probabilidade de falha crítica em cada tentativa (estimada em 5%).

Utilizamos a **Simulação de Monte Carlo** para gerar versões simuladas, com valores de falhas críticas ($X$) gerados conforme a distribuição binomial. Isso permite obter uma visão probabilística do risco de falhas por versão.
""")


st.header("B) Fundamentos Estatísticos e Justificativa da Distribuição Utilizada")

st.markdown("""
A **distribuição binomial** descreve o comportamento de uma variável dicotômica em amostras aleatórias (BUSSAB; MORETTIN, 2007).

Além disso, segundo **Bruce e Bruce (2020)**, a distribuição binomial é a distribuição de frequência do número de sucessos \\(x\\) em dado número de ensaios \\(n\\), com probabilidade especificada \\(p\\) de sucesso em cada ensaio.
""")

st.markdown("A média de uma distribuição binomial é dada por:")
st.latex(r"\mu = n \times p")

st.markdown("E a variância por:")
st.latex(r"\sigma^2 = n \times p \times (1 - p)")

st.markdown("""
Com um número grande de ensaios (especialmente quando \\(p\\) está próximo de 0,50), a distribuição binomial é virtualmente indistinguível da distribuição normal.

Nesse contexto, a justificativa para o uso da **distribuição binomial** no cenário escolhido se baseia em sua **adequação ao fenômeno modelado**, considerando que:

- **Os resultados são binários:** cada tentativa tem dois possíveis resultados (falha ou não-falha);
- **A probabilidade é constante:** supõe-se uma probabilidade \\(p = 0.5\\) (5%) constante de falha crítica por tentativa, ajustável conforme o histórico de incidentes da equipe;
- **Os eventos são independentes:** cada tentativa (deploy-funcionalidade) é considerada independente, devido à modularidade dos sistemas compostos por microserviços, onde uma falha não influencia diretamente outra.

Essas condições justificam formalmente o uso da distribuição binomial como **modelo estatístico para o total de falhas críticas por versão**.
""")

import streamlit as st

st.header("c) Análise Crítica dos Resultados da Simulação de Monte Carlo")

st.markdown("""
A escolha da **distribuição binomial** impacta diretamente os resultados da simulação, pois permite **modelar adequadamente a ocorrência de falhas críticas** com base em uma probabilidade de falhas associada ao número de funcionalidades, em um contexto de múltiplos deploys.

Dessa forma, a **Simulação de Monte Carlo** não apenas estima a média esperada de falhas, mas também gera a **distribuição dos possíveis cenários**.

### Implicações práticas e inferências:

A simulação permite derivar **inferências quantitativas úteis** para a tomada de decisão na engenharia de software. Por exemplo:

- **Planejamento de versões:** é possível estimar quantas funcionalidades ou versões podem ser lançadas mantendo-se dentro de um limite aceitável de falhas (por exemplo, no máximo 5 falhas críticas por versão);
- **Definição de metas de qualidade:** ao variar os parâmetros (número de funcionalidades por deploy, taxa de falha), a equipe pode simular **cenários futuros** e alinhar **expectativas de qualidade** com as áreas intervenientes.
""")

st.header("Referências")

st.markdown("""
- CALLEGARI-JACQUES, Sídia M. *Bioestatística: princípios e aplicações*. 2. ed. Porto Alegre: Artmed, 2003.  
- BRUCE, Peter; BRUCE, Andrew. *Estatística básica para cientistas de dados: 50 conceitos essenciais*. São Paulo: Alta Books, 2020.
""")

# Rodapé
st.markdown("---")
st.caption("Aluna: Sivia Branco")
