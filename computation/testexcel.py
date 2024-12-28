import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filenamecsv = "/home/coco/proj_jerem/Test2111-3_TS-04045_2024-11-21-11-19-27_aligned.csv"
df = pd.read_csv(filenamecsv)


nb_lignes = len(df)
segment_size = 2000
num_segments = nb_lignes // segment_size  # Nombre de segments


# Initialisation des variables
vx, vy, vz = 0, 0, 0
sum_vitesse = 0
moyennes_segment = []
tabax = []  # Stocker l'accélération X
inst_vitesse = []#Stock vitesse a T
time_subset = [] #stock time

max_value_seg = 0
dfx = df["az_m/s/s"]
dfy = df["ax_m/s/s"] - 9.81
dfz = df["ay_m/s/s"] 
dfxl = np.sqrt(dfx**2+dfy**2+dfz**2)
max_value_seg_min1 = 0 
acc_curr_mean_min1 = 0
v0 = 0
time_interval = df["time_s"].iloc[-1]/num_segments
list_mean_v = []
for seg in range(1,num_segments):
    # Initialiser les vitesses pour le segment courant
    v_seg_x, v_seg_y, v_seg_z = vx, vy, vz
    sum_v_seg = 0  # Somme des vitesses pour ce segment


    # Début et fin du segment
    start = seg * segment_size
    end = start + segment_size

    if(max_value_seg_min1<dfxl.iloc[start+1:end].max()):
        acc_curr_mean = dfxl.iloc[start+1:end].mean()
        v = v0 + (acc_curr_mean-acc_curr_mean_min1)*time_interval
        v0 = v
        list_mean_v.append(v*3.6)
        acc_curr_mean_min1 = acc_curr_mean
    max_value_seg_min1 = max_value_seg


print(np.array(list_mean_v).mean())


    # for ligne_tab in range(start + 1, end):
    #     # Lecture des accélérations
    #     ax = df.iloc[ligne_tab][3]
    #     ay = df.iloc[ligne_tab][1] - gravitational_constant  # Correction gravité
    #     az = df.iloc[ligne_tab][2]
        
    #     ax_min1 = df.iloc[ligne_tab-1][3]
    #     ay_min1 = df.iloc[ligne_tab-1][1] - gravitational_constant  # Correction gravité
    #     az_min1 = df.iloc[ligne_tab-1][2]

    #     #Norme de l'accélération
    #     axl = sqrt(ax**2 + ay**2 + az**2)
    #     axl_min1 = sqrt(ax_min1**2 + ay_min1**2 + az_min1**2)
    #     tabax.append(axl)
    #     time_subset.append(df['time_s'][ligne_tab])

    #     #Update mean_value_acc_seg
        

    #     # Calcul de l'intervalle de temps
    #     delta_temps = df['time_s'][ligne_tab] - df['time_s'][ligne_tab - 1]
    #     deltaxl = axl-axl_min1
        

#         # Intégration de l'accélération pour obtenir la vitesse
#         v_seg_x += (deltaxl * delta_temps)
#         print(v_seg_x)



#         # Calcul de la vitesse pour cet instant
#         v = sqrt(v_seg_x ** 2)
#         sum_v_seg += v
#         inst_vitesse.append(v)


#     # Calcul de la vitesse moyenne pour le segment
#     moyenne_v_seg = sum_v_seg / segment_size
#     moyennes_segment.append(moyenne_v_seg)  # Stocker la moyenne du segment


#     # Mise à jour de la vitesse globale pour le prochain segment
#     vx, vy, vz = v_seg_x, v_seg_y, v_seg_z


# # Calcul de la vitesse moyenne globale
# vitesse_moyenne_totale = np.mean(moyennes_segment)


# print(f"Nombre de paquets : {num_segments}")
# print(f"Vitesse moyenne totale en m/s : {vitesse_moyenne_totale}")
# print(f"Vitesse moyenne totale en km/h : {vitesse_moyenne_totale * 3.6}")




# #VISUALISATION EN GRAPHIQUE


# fig, ax1 = plt.subplots(figsize=(10, 6))


# # Courbe de l'accélération sur le premier axe Y
# ax1.plot(time_subset, tabax, label="Accélération X", color="blue")
# ax1.set_xlabel("Temps (s)")
# ax1.set_ylabel("Accélération (m/s²)", color="blue")
# ax1.tick_params(axis='y', labelcolor="blue")
# ax1.grid()


# # Second axe Y pour la vitesse
# ax2 = ax1.twinx()
# ax2.plot(time_subset, inst_vitesse, label="Vitesse", color="red")
# ax2.set_ylabel("Vitesse (m/s)", color="red")
# ax2.tick_params(axis='y', labelcolor="red")


# # Titre commun et affichage
# plt.title("Accélération et Vitesse en fonction du temps")
# fig.tight_layout()
# plt.show()


