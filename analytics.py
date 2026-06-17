# importe numpy
import numpy as np
# defina uma constante no topo do arquivo
N_IBOV = 90   # número aproximado de ativos do Ibovespa
VOL_B3_DIARIO = 20e9   # R$ 20 bilhões — volume médio diário B3 2024-2025

# Função calcular_energia_cin(P, V, mu):

def calcular_energia_cin(P, V, mu):
    #   - implementar E_cin = 0.5 * P * V * mu**2
    #   - P, V, mu são arrays numpy de shape (n_ativos,)
    E_cin = 0.5 * P * V * mu**2
    #   - retorne array de shape (n_ativos,) com a energia cinética de cada ativo
    return E_cin

# Função calcular_energia_pot(P, V, sigma):
def calcular_energia_pot(P, V, sigma):
    #   - implementar E_pot = 0.5 * P * V * sigma**2
    E_pot = 0.5 * P * V * sigma**2
    #   - retorne array de shape (n_ativos,) com a energia potencial de cada ativo
    return E_pot

# Função calcular_energia_total(E_cin, E_pot):
def calcular_energia_total(E_cin, E_pot):
    #   - some os dois arrays
    E_total= E_cin + E_pot
    #   - retorne array de shape (n_ativos,) com a energia total de cada ativo
    return E_total

# Função calcular_temperatura(E_total):
def calcular_temperatura(E_total):
    #   - calcule a média de E_total sobre todos os ativos
    #   - isto é o kT do ensemble
    #   - retorne um escalar
    kT = np.mean(E_total)
    return kT
# Função calcular_energia_alpha(E_cin, E_pot, alpha):
def calcular_energia_alpha(E_cin, E_pot, alpha):
    #   - implemente
    #   - alpha é um escalar entre 0 e 1
    E_alpha = alpha * E_cin + (1 - alpha) * E_pot
    #   - retorne array de shape (n_ativos,) com a energia combinada
    return E_alpha

# Função calcular_pesos_boltzmann(E, kT):
def calcular_pesos_boltzmann(E, kT):
    #   - implemente
    w_i = np.exp(-E / kT)
    #   - normalize ()dividindo pelo somatório
    w = w_i/(w_i.sum())
    #   - retorne array de shape (n_ativos,) com os pesos somando 1
    return w
def calcular_sensibilidade(w, sigma):
    delta_M_up = (w * sigma).sum()
    delta_M_down = -(w * sigma).sum()
    return  (delta_M_up, delta_M_down)
if __name__ == "__main__":
    # importe as funções do data_loader
    from data_loader import baixar_dados, calcular_retornos, estatisticas, TICKERS_ACOES
    # baixe os dados e calcule as estatísticas
    df, df_vol = baixar_dados(TICKERS_ACOES, "1y")
    df_ret = calcular_retornos(df)
    mu, sigma = estatisticas(df_ret)
    # extrair P e V como arrays numpy
    P = df.mean().to_numpy()        # preco medio
    V = df_vol.mean().to_numpy()    # volume medio
    # calcular lambda — fração do mercado que a amostra representa
    VOL_B3_DIARIO = 20e9
    m_i = P * V
    vol_amostra_reais = m_i.sum()
    lamb = vol_amostra_reais / VOL_B3_DIARIO
    print("volume amostra R$:", vol_amostra_reais)
    print("lambda:", lamb)
    # calcular energias
    E_cin = calcular_energia_cin(P, V, mu)
    E_pot = calcular_energia_pot(P, V, sigma)
    E_total = calcular_energia_total(E_cin, E_pot)
    print("E_cin:",   E_cin)
    print("E_pot:",   E_pot)
    print("E_total:", E_total)
    # temperatura do ensemble
    kT = calcular_temperatura(E_total)
    print("kT:", kT)
    # pesos de Boltzmann com alpha = 0.5
    E_alpha = calcular_energia_alpha(E_cin, E_pot, alpha=0.5)
    print("E_alpha:", E_alpha)
    w = calcular_pesos_boltzmann(E_alpha, kT)
    print("pesos Boltzmann:", w)
    print("soma dos pesos:", w.sum())
