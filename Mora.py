# Recolecta de Dades
A = float (input ("mL de EDTA: "))
P = float (input ("mL de NaOH: "))
D = float (input ("Densitat: "))

# Calculs
c = A * 1.27                # Cu en g/l
b = A * 3.74                # Pirofosat de Cu en g/l

q = P * 21.75               # Pirofosfat Total
r = 1.9 * (q - 1.37 * c)    # Pirofosfat tetrapotasic

s = 1 + ((r + b)/1350)      # Densitat teorica
t = 600 * (D - s)           # Ortofosfat.      Aquest calcul esta malament!!!!!!

# Presentacio resultats
print()
print("Cu:", round(c, 1))
print("PiroCu:", round (b, 1))
print("4K:", round(r, 1))
print("Orto:", round(t, 1))