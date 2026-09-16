from MonteCarlo import MonteCarloEstimator, MeasurementSerie, Measurment
import numpy as np 



# Premier cas d'application : mesure d'une longueur avec une règle graduée au mm

# --- Incertitude de type A : mesure d'une longueur avec une règle, répétée N fois ---
mesures_longueur = MeasurementSerie([12.3, 12.4, 12.2, 12.35, 12.28, 12.31, 12.27])
mesure_A = mesures_longueur.to_measurment()  # Measurment(value=mean, uncertainty=uncertainty_on_mean)

print(f"Type A -> valeur: {mesure_A.value:.2f}, incertitude: {mesure_A.uncertainty:.2f}")

# --- Incertitude de type B : mesure unique avec une règle graduée au mm ---
# Δ = 0.5 mm (valeur entre deux graduations) -> u(x) = Δ/√3
delta_B = 0.5
mesure_B = Measurment(value=8.0, uncertainty=delta_B / np.sqrt(3))

print(f"Type B -> valeur: {mesure_B.value:.2f}, incertitude: {mesure_B.uncertainty:.2f}")

# --- Combinaison des deux via Monte-Carlo : par exemple L = mesure_A - mesure_B ---
f = lambda x1, x2: x1 - x2

estimateur = MonteCarloEstimator(f=f, N=100_000, measurment_list=[mesure_A, mesure_B])
u_L = estimateur.estimator()

print(f"Incertitude-type composée u(L) = {u_L:.4f}")
print("""

---------------------------------------------------------------------------------------

""")




# second cas d'application : résistance équivalente de deux résistances en parallèle

# R1 : mesuré plusieurs fois à l'ohmmètre (type A)
mesures_R1 = MeasurementSerie([220.4, 219.8, 220.1, 220.6, 219.9, 220.3])
R1 = mesures_R1.to_measurment()

print(f"R1 (type A) -> valeur: {R1.value:.2f} Ω, incertitude: {R1.uncertainty:.2f} Ω")

# R2 : mesure unique au multimètre numérique, précision constructeur Δ = 1.5 Ω
delta_R2 = 1.5
R2 = Measurment(value=330.0, uncertainty=delta_R2 / np.sqrt(3))

print(f"R2 (type B) -> valeur: {R2.value:.2f} Ω, incertitude: {R2.uncertainty:.2f} Ω")

# Résistance équivalente en parallèle : R_eq = (R1 * R2) / (R1 + R2)
f_parallele = lambda r1, r2: (r1 * r2) / (r1 + r2)

estimateur = MonteCarloEstimator(f=f_parallele, N=100_000, measurment_list=[R1, R2])
u_Req = estimateur.estimator()

# valeur centrale de R_eq (à partir des valeurs, pas des tirages)
Req_value = f_parallele(R1.value, R2.value)

print(f"R_eq = {Req_value:.2f} +- {u_Req:.2f} Ω")