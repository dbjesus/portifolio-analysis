import numpy as np
import pandas as pd


def calcular_retorno_portfolio_diario(df_ret, w):
    retorno_array = df_ret.to_numpy() @ w
    retorno_serie = pd.Series(retorno_array, index=df_ret.index)
    return retorno_serie


def retorno_hoje(retorno_diario):
    return retorno_diario.iloc[-1]


def retorno_periodo(retorno_diario, inicio, fim):
    filtro = retorno_diario[inicio:fim]
    retorno_acumulado = (1 + filtro).prod() - 1
    return retorno_acumulado


def calcular_performance_resumo(retorno_diario):
    hoje = retorno_diario.index[-1]

    inicio_semana_atual    = hoje - pd.Timedelta(days=hoje.weekday())
    inicio_semana_anterior = inicio_semana_atual - pd.Timedelta(days=7)
    fim_semana_anterior    = inicio_semana_atual - pd.Timedelta(days=1)
    inicio_mes             = hoje.replace(day=1)

    resumo = {
        "hoje":             retorno_hoje(retorno_diario),
        "semana_atual":     retorno_periodo(retorno_diario, inicio_semana_atual, hoje),
        "semana_anterior":  retorno_periodo(retorno_diario, inicio_semana_anterior, fim_semana_anterior),
        "mes":              retorno_periodo(retorno_diario, inicio_mes, hoje),
    }
    return resumo


if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, estatisticas, TICKERS_ACOES
    from portfolio import montar_portfolio

    df, df_vol = baixar_dados(TICKERS_ACOES, "1y")
    df_ret     = calcular_retornos(df)
    mu, sigma  = estatisticas(df_ret)
    P          = df.mean().to_numpy()
    V          = df_vol.mean().to_numpy()

    w, _, _, _ = montar_portfolio(mu, sigma, P, V)

    retorno_diario = calcular_retorno_portfolio_diario(df_ret, w)
    resumo = calcular_performance_resumo(retorno_diario)

    for periodo, valor in resumo.items():
        print(f"{periodo}: {valor*100:.2f}%")
