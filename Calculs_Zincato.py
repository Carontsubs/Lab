# Recolecta de Dades
A = float (input ("Concetracio Zincato gr/l: "))
E = float (input ("Concetracio Zn Original gr/l: "))
C = float (input ("Concentracio final desitjada gr/l: "))
B = float (input ("Volum final ml: ")) /1000

D = ((C - E) / (A - E)) * B

D = D *1000             #Converitr a mL

print(f'{round(D,1)} mL')