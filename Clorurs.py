import numpy as np
import pandas as pd

# Llegir les dades de y des d'un fitxer CSV
y = pd.read_csv('Lab\lectura_mv.csv', header=None).squeeze().to_numpy()

# Crear x amb increments de 0.5 i ajustar longitud
x = np.arange(0, 10.5, 0.5)[:len(y)]

# Calcular diferències (salts) entre valors consecutius
dy = np.diff(y)  # amb signe per veure el salt positiu o negatiu

# Trobar l'índex on hi ha el canvi absolut més gran
i = np.argmax(np.abs(dy))

salt_central = dy[i]

salt_anterior = dy[i-1] if i-1 >= 0 else None
salt_posterior = dy[i+1] if i+1 < len(dy) else None

# Calcular diferències respecte el salt central
diff_anterior = (salt_central - salt_anterior) if salt_anterior is not None else None
diff_posterior = (salt_central - salt_posterior) if salt_posterior is not None else None
sum_diff = diff_anterior + diff_posterior
Clorurs =x[i] + ((0.5*diff_anterior)/sum_diff)

# Mostrar resultats
print()
print(f"Punt d'inflexió entre x = {x[i]} i x = {x[i+1]}")
print(f"Salt central {x[i]} : {salt_central}")

if salt_anterior is not None:
    print(f"Salt anterior {x[i-1]} : {salt_anterior}")
else:
    print("No hi ha salt anterior (punt d'inflexió és a l'inici)")

if salt_posterior is not None:
    print(f"Salt posterior {x[i+1]} : {salt_posterior}")
else:
    print("No hi ha salt posterior (punt d'inflexió és al final)")

print()
print(f"E1 = {diff_anterior}")
print(f"E2 = {diff_posterior}")
print(f"E3 = {sum_diff}")
print()
print(f"Consum {round(Clorurs,2)} ml/l")
print(f"Clorurs {round(Clorurs*14.2,1)} ppm")
print()

