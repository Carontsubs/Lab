# Recolecta de Dades
A = float (input ("Concetracio Zincato gr/l: "))
E = float (input ("Concetracio Zn Original gr/l: "))
C = float (input ("Concentracio final desitjada gr/l: "))
B = float (input ("Volum final ml: "))

D = ((C - E) / (A - E)) * (B/1000)

D = D *1000             #Converitr a mL

print(f'{round(D)} mL')