import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import butter, lfilter, freqz

file_path = str(Path(__file__).parent.parent / "data/006-a-2_TS-04045_2024-12-12-10-01-46_aligned.csv")
df = pd.read_csv(file_path)
# df["acc"] = np.sqrt(df['ax_m/s/s'] ** 2 + (df['ay_m/s/s']-9.81) ** 2 + df['az_m/s/s'] ** 2)
df["acc"] = df["ax_m/s/s"]
datax = df[["time_s", "acc"]]

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order):
    return butter(order, cutoff, fs=fs, btype="high", analog=False)
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
#low pass filter inputs
order = 4
fe = 11
cutoff = 5

#high pass filter inputs
orderhigh = 1
cutoffhigh = 0.001

y = butter_lowpass_filter(datax[datax.columns[1]], cutoff, fe, order)
y = butter_highpass_filter(y, cutoffhigh, fe, orderhigh)
plt.subplot(2, 1, 1)
plt.plot(datax[datax.columns[0]], datax[datax.columns[1]], 'b-')
plt.plot(datax[datax.columns[0]], y, 'g-', linewidth=2)
plt.xlabel('Time [sec]')
plt.grid()


Vx = [0]
for i in range(1,len(y)):
    V_t = Vx[i-1] + y[i]*(df["time_s"][i]-df["time_s"][i-1])
    Vx.append(V_t)
    V_init_step = V_t
plt.subplot(2, 1, 2)
plt.plot(datax[datax.columns[0]], datax[datax.columns[1]], 'b-')
plt.plot(datax[datax.columns[0]], Vx, 'r', linewidth = 2)
plt.xlabel('Time [sec]')
plt.grid()
plt.show()
# immobile_data = data[data['time_s'] <= 2]

# acceleration_immobile = immobile_data['acc_norm'].mean()
# axl_immobile_max = immobile_data['acc_norm'].max() + 20 / 100 * acceleration_immobile
# axl_immobile_min = immobile_data['acc_norm'].min() - 7 / 100 * acceleration_immobile

# def detect_steps_with_visualization(data, axl_immobile_max, axl_immobile_min, min_time_between_steps=0.2):
#     is_immobile = True  # État initial : dans l'immobilité
#     step_count = 0
#     step_times = []  # Liste des temps où les pas sont détectés

#     for i, acc in enumerate(data['acc_norm']):
#         if is_immobile:
#             # Si on sort de l'immobilité
#             if acc > axl_immobile_max:
#                 is_immobile = False  # Entrée en mouvement
#         else:
#             # Si on revient à l'immobilité
#             if acc <= axl_immobile_min:
#                 current_time = data['time_s'].iloc[i]

#                 # Vérifie si le temps depuis le dernier pas est suffisant
#                 if not step_times or (current_time - step_times[-1]) > min_time_between_steps:
#                     step_count += 1  # Un pas valide détecté
#                     step_times.append(current_time)  # Sauvegarde du temps du pas

#                     #CALCUL DE LA VITESSE SUR CHAQUE SEGMENT DE PAS
                    
#                     # v = V0 + DiffAxl * DeltaTemps

#                     #La taille d'un segment = le temps du pas / 0.000625
#                     #V0 = 0
#                     #DiffAxl = Moyenne des Axl du segment de mtn - Moyenne des Axl du segment d'avant
#                     #DeltaTemps = Temps à la derniere ligne du segment - temps à la premiere ligne du segment





#                 is_immobile = True  # Retour à l'immobilité

#     # Exclure les 3 premiers et les 3 derniers pas
#     if len(step_times) > 6:
#         filtered_step_times = step_times[3:-3]  # On prend les pas sans les 3 premiers et les 3 derniers

#         # Calcul des statistiques sur les pas restants
#         time_between_steps = np.diff(filtered_step_times)
#         mean_time_step = np.mean(time_between_steps)
#         standard_deviation_tps_foulee = np.std(time_between_steps)
#         var_tps_foulee = standard_deviation_tps_foulee / mean_time_step * 100
#         tps_de_marche = step_times[-1] - step_times[0] + mean_time_step
#         step_count_filtered = len(filtered_step_times)
#     else:
#         mean_time_step = 0
#         standard_deviation_tps_foulee = 0
#         var_tps_foulee = 0
#         tps_de_marche = 0
#         step_count_filtered = 0

#     print(f"Durée de la passation : {len(data)*0.000625} secondes")
#     print(f"Temps de marche (filtré) : {tps_de_marche} secondes")
#     print(f"Moyenne du temps de foulée (filtré) : {mean_time_step} secondes")
#     print(f"Variabilité du temps de foulée (filtré) : {var_tps_foulee} %")
#     print(f"Nombre de pas détectés (filtré) : {step_count_filtered}")

#     return step_count_filtered, filtered_step_times

# # Appliquer le détecteur de pas
# nombre_de_pas, filtered_step_times = detect_steps_with_visualization(data, axl_immobile_max, axl_immobile_min)

# # 3. Visualisation graphique
# plt.figure(figsize=(12, 6))

# # Courbe de la norme d'accélération
# plt.plot(data['time_s'], data['acc_norm'], label="Norme de l'accélération", color='blue')

# # Seuils d'immobilité
# plt.axhline(axl_immobile_max, color='green', linestyle='dashed', label='Seuil max immobilité')
# plt.axhline(axl_immobile_min, color='red', linestyle='dashed', label='Seuil min immobilité')

# # Marquage des pas détectés
# for t in filtered_step_times:
#     plt.axvline(t, color='orange', linestyle=':',
#                 label='Pas détecté (filtré)' if 'Pas détecté (filtré)' not in plt.gca().get_legend_handles_labels()[1] else "")

# # Ajouter des labels et légendes
# plt.title(f"Détection des pas (Nombre de pas détectés : {nombre_de_pas})")
# plt.xlabel("Temps (s)")
# plt.ylabel("Norme de l'accélération (m/s²)")
# plt.legend()
# plt.grid(True)

# # Afficher la figure
# plt.show()
