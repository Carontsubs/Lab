# Recolecta de Dades
A = float (input ("Concentracio Zincato gr/l: "))
E = float (input ("Concentracio Zn Original gr/l: "))
C = float (input ("Concentracio final desitjada gr/l: "))
B = float (input ("Volum final ml: ")) /1000

D = ((C - E) / (A - E)) * B

D = D *1000             #Converitr a mL

print(f'{round(D,1)} mL')