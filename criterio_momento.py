# importe numpy
import numpy as np
# Função
def calcular_peso_momento(mu, V, fracao=1/3 * 0.20):
    #   - calcule mu**2 * V para cada ativo
    f = mu**2 * V
    #   - normalize dividindo pela soma
    w = f/(f.sum())
    #   - multiplique pela fracao
    #   - retorne array de shape (n_ativos,)
    return w*fracao

if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, TICKERS_ACOES
    from janela_movel import calcular_mu_diario, calcular_volume_hoje
    df, df_vol = baixar_dados(TICKERS_ACOES, "1y")
    df_ret     = calcular_retornos(df)
    mu_hoje    = calcular_mu_diario(df_ret)
    vol_hoje   = calcular_volume_hoje(df_vol)
    print("mu_hoje:",  mu_hoje)
    print("vol_hoje:", vol_hoje)

    w = calcular_peso_momento(mu_hoje, vol_hoje)
    print("pesos momento:", w)
    print("soma:", w.sum())
