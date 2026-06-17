# importe numpy
import numpy as np
# Função
def calcular_peso_sharpe(mu, sigma, fracao=1/3 * 0.20):
    #   - calcule mu**2 / sigma para cada ativo
    mu2 = mu**2/sigma
    #   - normalize dividindo pela soma
    w = mu2/(mu2.sum())
    #   - multiplique pela fracao
    #   - retorne array de shape (n_ativos,)
    return w*fracao

if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, TICKERS_ACOES
    from janela_movel import calcular_mu_diario, calcular_sigma_movel, calcular_sigma_hoje

    df, df_vol  = baixar_dados(TICKERS_ACOES, "1y")
    df_ret      = calcular_retornos(df)
    mu_hoje     = calcular_mu_diario(df_ret)
    sigma_movel = calcular_sigma_movel(df_ret)
    sigma_hoje  = calcular_sigma_hoje(sigma_movel)

    w = calcular_peso_sharpe(mu_hoje, sigma_hoje)
    print("pesos sharpe:", w)
    print("soma:", w.sum())
