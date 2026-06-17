import matplotlib.pyplot as plt
import numpy as np

CORES = {
    "estabilidade": "#3266ad",
    "boltzmann":    "#BA7517",
    "agressivo":    "#3B6D11",
}

LABELS = {
    "estabilidade": "Estabilidade (40%)",
    "boltzmann":    "Boltzmann (40%)",
    "agressivo":    "Agressivo (20%)",
}

# Função plot_pesos_finais(tickers, pesos):
def plot_pesos_finais(tickers, pesos):
    #   - crie uma figura com plt.subplots()
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,4))
    #   - plote um gráfico de barras: ax.bar(tickers, pesos)
    ax.bar(tickers, pesos)
    #   - rotacione os labels do eixo x para não sobrepor (rotation=45)
    ax.tick_params(axis='x', labelrotation=45)
    #   - adicione título "Composição final do portfólio"
    ax.set_title("Composição final do portfólio")
    #   - adicione label do eixo y "Peso (%)"
    ax.set_ylabel("Peso (%)")
    #   - retorne a figura
    plt.show()
    return fig
# Função plot_comparacao_sistemas(tickers, w_estab, w_boltz, w_agress):
def plot_comparacao_sistemas(tickers, w_estab, w_boltz, w_agress):
    fig, ax = plt.subplots(figsize=(12, 5))

    x = np.arange(len(tickers))
    width = 0.25

    ax.bar(x - width, w_estab,  width, label=LABELS["estabilidade"], color=CORES["estabilidade"])
    ax.bar(x,         w_boltz,  width, label=LABELS["boltzmann"],    color=CORES["boltzmann"])
    ax.bar(x + width, w_agress, width, label=LABELS["agressivo"],    color=CORES["agressivo"])

    ax.set_xticks(x)
    ax.set_xticklabels(tickers, rotation=45)
    ax.set_ylabel("Peso (%)")
    ax.set_title("Comparação dos três sistemas de alocação")
    ax.legend()

    plt.show()
    return fig
if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, estatisticas, TICKERS_ACOES
    from portfolio import montar_portfolio

    df, df_vol = baixar_dados(TICKERS_ACOES, "1y")
    df_ret     = calcular_retornos(df)
    mu, sigma  = estatisticas(df_ret)
    P          = df.mean().to_numpy()
    V          = df_vol.mean().to_numpy()

    #w       = montar_portfolio(mu, sigma, P, V)
    w, w_estab, w_boltz, w_agress = montar_portfolio(mu, sigma, P, V)
    tickers = df_ret.columns.tolist()

    plot_pesos_finais(tickers, w * 100)
    plot_comparacao_sistemas(tickers, w_estab * 100, w_boltz * 100, w_agress * 100)
