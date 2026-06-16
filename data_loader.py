# Importe yfinance e pandas
import yfinance as yf
import pandas as pd
import numpy as np
# Defina duas listas de strings: TICKERS_ACOES (15 ativos da B3, sufixo .SA)
# e TICKERS_RF (2 a 3 proxies de renda fixa do Yahoo, ex: ^IRX, ^TNX)

TICKERS_ACOES = [ "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA", "WEGE3.SA", "RENT3.SA", "MGLU3.SA", "SUZB3.SA", "GGBR4.SA", "RADL3.SA", "LREN3.SA", "EMBJ3.SA", "HAPV3.SA", "TOTS3.SA", ]

TICKERS_RF = [
    "^IRX",    # T-bill 13 semanas (proxy de taxa livre de risco)
    "^TNX",    # Treasury 10 anos (proxy de renda fixa longa)
]


# Função baixar_dados(tickers, periodo):
#   - Use yf.download() passando a lista inteira (não itere um por um)
#   - Selecione apenas a coluna "Close" do resultado
#   - Remova linhas completamente vazias com dropna(how="all")
#   - Retorne o DataFrame de preços: linhas = datas, colunas = tickers

def baixar_dados(tickers: list[str], periodo: str = "2y") -> pd.DataFrame:
    raw = yf.download(
        tickers,
        period=periodo,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    fechamento = raw["Close"]          # seleciona só o preço de fechamento
    volume = raw["Volume"]             # seleciona o volume de negociacao
    fechamento = fechamento.dropna(how="all")  # remove linhas totalmente vazias
    volume = volume.loc[fechamento.index]
    return fechamento, volume

#def baixar_volume(tickers: list[str], periodo: str = "2y") -> pd.DataFrame:
    #raw = yf.download(
        #tikers,
        #period = periodo,
        #interval=1d,
        #auto_adjust=True,
        #progress=False,
        #)


# Função calcular_retornos(df_precos):
#   - Aplique pct_change() sobre o DataFrame de preços
#   - Remova a primeira linha (NaN gerado pela diferença)
#   - Retorne o DataFrame de retornos diários no mesmo formato

def calcular_retornos(df_precos: pd.DataFrame) -> pd.DataFrame:
    return df_precos.pct_change().dropna()


# Função estatisticas(df_retornos):
#   - Calcule a média de cada coluna → vetor mu,    shape (n_ativos,)
#   - Calcule o desvio padrão de cada coluna → vetor sigma, shape (n_ativos,)
#   - Converta ambos para numpy array com .to_numpy()
#   - Retorne (mu, sigma) como tupla

def estatisticas(df_retornos: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    mu    = df_retornos.mean().to_numpy()   # retorno médio diário, shape (n,)
    sigma = df_retornos.std().to_numpy()    # vol diária,           shape (n,)
    return mu, sigma


#teste
if __name__ == "__main__":
    df = baixar_dados(TICKERS_ACOES, "1y")
    df_ret = calcular_retornos(df)
    mu, sigma = estatisticas(df_ret)

    # DataFrame auxiliar para inspecionar volatilidade por ativo
    tickers = df_ret.columns.tolist()
    df_aux = pd.DataFrame({'ticker': tickers, 'sigma': sigma})
    df_aux_sorted = df_aux.sort_values(by='sigma').reset_index(drop=True)
    print(df_aux_sorted)

    # 40% do capital nas 5 mais estáveis, ponderado por 1/sigma
    df_40 = df_aux_sorted.head(5)
    sigma_40 = df_40['sigma'].to_numpy()
    weight_40 = 1 / sigma_40
    weight_40 = (weight_40 / weight_40.sum()) * 0.4
    print(weight_40)
    print(weight_40.sum())



