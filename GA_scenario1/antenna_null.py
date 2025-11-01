import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# ====== Função de ganho com null steering ======
def realistic_antenna_gain(angle_deg, null_direction_deg):
    angle_diff = abs((angle_deg - null_direction_deg + 180) % 360 - 180)

    G_null = -30     # dB (no null)
    G_plateau = -15  # dB até ±40°
    G_max = 10       # dB (máximo nas costas)

    if angle_diff <= 40:
        return G_null + (G_plateau - G_null) * (angle_diff / 40)
    else:
        gain = G_plateau + (G_max - G_plateau) * np.tanh((angle_diff - 40) / 50)
        return gain

# ====== Função para desenhar o padrão de radiação ======
def plot_antenna_pattern(null_direction_deg=0):
    angles = np.linspace(0, 360, 360)
    gains_dB = np.array([realistic_antenna_gain(a, null_direction_deg) for a in angles])

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(np.radians(angles), gains_dB, color='crimson', linewidth=2)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(-35, 15)
    ax.set_rticks([-30, -20, -10, 0, 10])
    ax.set_title(f"Padrão de radiação (null @ {null_direction_deg}°)", va='bottom', fontsize=13)
    plt.show()





#----------------------------antena sirecional------------------------------------------------



def interpolated_directional_gain(angle_deg, main_lobe_direction_deg=0):
    # Ângulos relativos (0–360)
    relative_angles = np.array([0, 45, 90, 135, 150, 180, 210, 225, 270, 315, 360])
    gains_dB = np.array([10.0, 5.94, -22.5, -10.315, -14.38, -7.0, -14.38, -10.315, -22.5, 5.94, 10.0])

    # Corrigir ângulo para relativo ao lóbulo principal
    angle_rel = (angle_deg - main_lobe_direction_deg) % 360

    interpolator = interp1d(relative_angles, gains_dB, kind='linear')

    return float(interpolator(angle_rel))






def plot_interpolated_directional_pattern(main_lobe_direction_deg=0):
    angles = np.linspace(0, 360, 360)
    gains_dB = np.array([
        interpolated_directional_gain(a, main_lobe_direction_deg) for a in angles
    ])

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(np.radians(angles), gains_dB, color='navy', linewidth=2)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(-35, 15)
    ax.set_rticks([-30, -20, -10, 0, 10])
    ax.set_title(f"Padrão de radiação (lóbulo suave @ {main_lobe_direction_deg}°)", va='bottom', fontsize=13)
    plt.show()


