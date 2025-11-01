import numpy as np
from antenna_null import realistic_antenna_gain

# Conversão de dBm para Watts
def dBm_to_watts(dBm):
    return 10 ** ((dBm - 30) / 10)

# Modelo de perda de percurso (path loss)
def path_loss(d, d0=1, L_d0=30, n=2.7, eps=1e-9):
    # garante que não se usa d == 0
    d_safe = np.maximum(d, eps)
    return L_d0 + 10 * n * np.log10(d_safe / d0)


# Potência recebida (Friis) em watts
def received_power(PT_dBm, GT_dB, GR_dB, lambda_0, d, L, eps=1e-9):
    d_safe = np.maximum(d, eps)
    free_space_loss = 20 * np.log10(lambda_0 / d_safe)
    PRx_dBm = PT_dBm + GT_dB + GR_dB - 21.98 - free_space_loss - L
    return dBm_to_watts(PRx_dBm)


# SINR em escala linear
def SINR(P_signal, P_interference, P_noise):
    return P_signal / (P_interference + P_noise)

# Capacidade do link (Shannon)
def link_capacity(bandwidth, sinr):
    return bandwidth * np.log2(1 + sinr)

# Função utilitária completa para calcular capacidade entre 2 UAVs
def calcular_capacidade_link(
    pos1, pos2, lambda_0,
    P_tx_dBm, G_tx_dB, G_rx_dB,
    P_interference_dBm, P_noise_dBm, bandwidth
):
    d = np.linalg.norm(pos1 - pos2)
    # evita d == 0 (mantém dinâmica; usa um eps pequeno)
    if d == 0 or np.isclose(d, 0.0):
        d = 1e-9
    L = path_loss(d)
    P_rx = received_power(P_tx_dBm, G_tx_dB, G_rx_dB, lambda_0, d, L)

    P_interf = dBm_to_watts(P_interference_dBm)
    P_noise = dBm_to_watts(P_noise_dBm)
    sinr = SINR(P_rx, P_interf, P_noise)

    return link_capacity(bandwidth, sinr)


# Potência de interferência recebida do jammer (coerente com received_power)
def interference_from_jammer(P_jammer_dBm, G_jammer_i, lambda_0, d_jammer_i):
    d_safe = np.maximum(d_jammer_i, 1e-9)
    L = path_loss(d_safe)
    free_space_loss = 20 * np.log10(lambda_0 / d_safe)
    P_interf_dBm = P_jammer_dBm + G_jammer_i - 21.98 - free_space_loss - L
    return P_interf_dBm


