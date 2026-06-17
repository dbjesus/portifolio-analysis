# importe numpy e pandas
import numpy as np
import pandas as pd
# Função
def calcular_sigma_movel(df_ret, janela=21):
    #   - aplique rolling(janela) sobre df_ret
    #   - calcule o desvio padrão com .std()
    sigma_movel = df_ret.rolling(janela).std()


    #   - retorne o DataFrame completo com o sigma móvel
    #   - shape igual ao df_ret: linhas = datas, colunas = tickers
    return sigma_movel

# Função
def calcular_mu_diario(df_ret):
    #   - pegue a última linha de df_ret com .iloc[-1]
    #   - converta para numpy array com .to_numpy()
    #   - retorne o vetor mu do dia corrente, shape (n_ativos,)
    return df_ret.iloc[-2].to_numpy()

# Função
def calcular_sigma_hoje(sigma_movel):
    #   - pegue a última linha de sigma_movel com .iloc[-1]
    #   - converta para numpy array com .to_numpy()
    #   - retorne o vetor sigma do dia corrente, shape (n_ativos,)
    return sigma_movel.iloc[-1].to_numpy()

# Função
def calcular_volume_hoje(df_vol):
    #   - pegue a última linha de df_vol com .iloc[-1]
    #   - converta para numpy array com .to_numpy()
    #   - retorne o vetor volume do dia corrente, shape (n_ativos,)
    return df_vol.iloc[-2].to_numpy()

# Função
def calcular_preco_hoje(df):
    #   - pegue a última linha de df com .iloc[-1]
    #   - converta para numpy array com .to_numpy()
    #   - retorne o vetor preco do dia corrente, shape (n_ativos,)
    return df.iloc[-2].to_numpy()

# bloco de teste:
if __name__ == "__main__":
    #   - importe baixar_dados, calcular_retornos, TICKERS_ACOES do data_loader
    from data_loader import baixar_dados, calcular_retornos, TICKERS_ACOES
    #   - baixe os dados
    df, df_vol= baixar_dados(TICKERS_ACOES, "1y")
    #   - calcule df_ret
    df_ret = calcular_retornos(df)
    #   - chame cada função e imprima os resultados
    sigma_movel = calcular_sigma_movel(df_ret)
    mu_hoje     = calcular_mu_diario(df_ret)
    sigma_hoje  = calcular_sigma_hoje(sigma_movel)
    vol_hoje    = calcular_volume_hoje(df_vol)
    preco_hoje  = calcular_preco_hoje(df)

     #   - confirme que todos os vetores têm shape (15,)

    print("mu_hoje shape:",    mu_hoje.shape)
    print("sigma_hoje shape:", sigma_hoje.shape)
    print("vol_hoje shape:",   vol_hoje.shape)
    print("preco_hoje shape:", preco_hoje.shape)
    print("mu_hoje:",    mu_hoje)
    print("sigma_hoje:", sigma_hoje)
    print("vol_hoje:",   vol_hoje)
    print("preco_hoje:", preco_hoje)

