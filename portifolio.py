# importe numpy
import numpy as np
# importe do analytics:
from analytics import calcular_energia_alpha, calcular_energia_total, calcular_energia_cin, calcular_energia_pot, calcular_temperatura, calcular_pesos_boltzmann
#   calcular_energia_cin, calcular_energia_pot
#   calcular_energia_total, calcular_temperatura
#   calcular_energia_alpha, calcular_pesos_boltzmann

# importe do criterio_drift:    calcular_peso_drift
from criterio_drift import calcular_peso_drift
# importe do criterio_sharpe:   calcular_peso_sharpe
from criterio_sharpe import calcular_peso_sharpe
# importe do criterio_momento:  calcular_peso_momento
from criterio_momento import calcular_peso_momento

# Função
def montar_portfolio(mu, sigma, P, V, alpha=0.5, f_estab=0.40, f_boltz=0.40, f_agress=0.20):
    # sistema 1 — estabilidade
    inv_sigma    = 1 / sigma
    weight_estab = (inv_sigma / inv_sigma.sum()) * f_estab

    # sistema 2 — Boltzmann
    E_cin        = calcular_energia_cin(P, V, mu)
    E_pot        = calcular_energia_pot(P, V, sigma)
    E_total      = calcular_energia_total(E_cin, E_pot)
    kT           = calcular_temperatura(E_total)
    E_alpha      = calcular_energia_alpha(E_cin, E_pot, alpha)
    weight_boltz = calcular_pesos_boltzmann(E_alpha, kT) * f_boltz

    # sistema 3 — agressivo
    w_drift      = calcular_peso_drift(mu)
    w_sharpe     = calcular_peso_sharpe(mu, sigma)
    w_momento    = calcular_peso_momento(mu, V)
    weight_agress = w_drift + w_sharpe + w_momento

    # peso final
    w_final = weight_estab + weight_boltz + weight_agress

    # verificação
    assert abs(w_final.sum() - 1.0) < 1e-6, f"Pesos não somam 1: {w_final.sum()}"

    return w_final

if __name__ == "__main__":
    from data_loader import baixar_dados, calcular_retornos, estatisticas, TICKERS_ACOES
    from janela_movel import calcular_mu_diario, calcular_sigma_movel, calcular_sigma_hoje, calcular_volume_hoje, calcular_preco_hoje

    df, df_vol  = baixar_dados(TICKERS_ACOES, "1y")
    df_ret      = calcular_retornos(df)
    mu, sigma   = estatisticas(df_ret)
    P           = df.mean().to_numpy()
    V           = df_vol.mean().to_numpy()

    w = montar_portfolio(mu, sigma, P, V)

    tickers = df_ret.columns.tolist()
    for ticker, peso in zip(tickers, w):
        print(f"{ticker}: {peso*100:.2f}%")
    print(f"Total: {w.sum()*100:.2f}%")
