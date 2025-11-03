# Recolecta de Dades
A = float (input ("Pes Inicial en gr: "))
B = float (input ("Pes Final en gr: "))
# C = float (input ("Horas: "))

S = 0.0196   #Superficie proveta en m2

D = ((A - B)*1000) / S

print(f'{round(D)} mg/m2')