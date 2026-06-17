# importe numpy
import numpy as np
# Função
def calcular_peso_drift(mu,fracao=1/3 * 0.20):
    #   - calcule mu**2 para cada ativo
    mu2=mu**2
    #   - normalize dividindo pela soma
    #   - multiplique pela fração agressiva desejada (padrão 1/3 * 0.20)
    w=(mu2/(mu2.sum()))*fracao
    #   - retorne array de shape (n_ativos,)
    return w
if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, TICKERS_ACOES
    from janela_movel import calcular_sigma_movel, calcular_mu_diario

    df, df_vol = baixar_dados(TICKERS_ACOES, "1y")
    df_ret     = calcular_retornos(df)
    mu_hoje    = calcular_mu_diario(df_ret)

    w = calcular_peso_drift(mu_hoje)
    print("pesos drift:", w)
    print("soma:", w.sum())
