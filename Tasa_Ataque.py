# Recolecta de Dades
A = float (input ("Pes Inicial en gr: "))
B = float (input ("Pes Final en gr: "))
C = float (input ("Horas: "))

S = 1.4   #Superficie celula Hull en dm2

D = ((A - B)*1000) / (S * C)

print(f'{round(D,3)} mg/hdm2')