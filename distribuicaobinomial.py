import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da simulação
n_funcionalidades = 50
p_falha = 0.05
n_simulacoes = 10_000

# Simulação Monte Carlo com distribuição binomial
falhas_por_versao = np.random.binomial(n=n_funcionalidades, p=p_falha, size=n_simulacoes)

# Estatísticas básicas
media_falhas = np.mean(falhas_por_versao)
desvio_padrao = np.std(falhas_por_versao)
prob_mais_de_5 = np.mean(falhas_por_versao > 5)
prob_nenhuma_falha = np.mean(falhas_por_versao == 0)

# Exibição
print(f"Média de falhas por versão: {media_falhas:.2f}")
print(f"Desvio padrão: {desvio_padrao:.2f}")
print(f"Probabilidade de mais de 5 falhas críticas: {prob_mais_de_5:.2%}")
print(f"Probabilidade de nenhuma falha: {prob_nenhuma_falha:.2%}")

# Histograma
plt.hist(falhas_por_versao, bins=range(0, max(falhas_por_versao)+1), edgecolor='black', alpha=0.7)
plt.title('Distribuição do Número de Falhas Críticas por Versão')
plt.xlabel('Número de falhas críticas')
plt.ylabel('Frequência')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()