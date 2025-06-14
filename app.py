import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configurações da página
st.set_page_config(page_title="Simulação Monte Carlo - Falhas Críticas", layout="centered")

st.title("Simulação de Monte Carlo com Distribuição Binomial")
st.subheader("Qualidade de Software - Estimativa de Falhas Críticas Pós-Deploy")

st.markdown("""
Este app simula o número de **falhas críticas** em funcionalidades de software após o deploy,
usando a **distribuição binomial** e a **técnica de Simulação de Monte Carlo**.
""")

# Entradas do usuário
n_funcionalidades = st.slider("Número de funcionalidades por versão", 10, 200, 50, step=10)
p_falha = st.slider("Probabilidade de falha crítica (%)", 0.0, 20.0, 5.0, step=0.5) / 100
n_simulacoes = st.slider("Número de simulações (deploys)", 100, 10000, 1000, step=100)

# Simulação
falhas = np.random.binomial(n=n_funcionalidades, p=p_falha, size=n_simulacoes)

# Estatísticas
media = np.mean(falhas)
desvio = np.std(falhas)
prob_mais_de_5 = np.mean(falhas > 5)
prob_zero = np.mean(falhas == 0)

# Resultados
st.markdown("### Resultados da Simulação")
st.write(f"**Média de falhas por versão:** {media:.2f}")
st.write(f"**Desvio padrão:** {desvio:.2f}")
st.write(f"**Probabilidade de mais de 5 falhas:** {prob_mais_de_5:.2%}")
st.write(f"**Probabilidade de nenhuma falha:** {prob_zero:.2%}")

# Histograma
st.markdown("### Distribuição do Número de Falhas por Versão")

fig, ax = plt.subplots()
ax.hist(falhas, bins=range(0, max(falhas)+2), edgecolor='black', alpha=0.7)
ax.set_xlabel("Número de falhas críticas")
ax.set_ylabel("Frequência")
ax.set_title("Distribuição binomial simulada")
ax.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido usando Python + Streamlit")
