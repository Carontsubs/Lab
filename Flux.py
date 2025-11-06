# Recolecta de Dades
A = float (input ("mL de EDTA: "))
P = float (input ("mL de AgNO3: "))

# Calculs
b = A * 13          # Zenc en g/l
c = b * 2.085       # Clorur de Zenc        
d = c * 0.52        # Clorurs provinents del zenc

q = P * 7.08        # Clorurs
r = 1.509 * (q - d) # Clorur d'Amoni

s = 2.55 * (r / c)  # Relacio Molar
t = c + r           # Sals Totals

if t < 450 and c < 250 and r < 200:
    y = (450 - t) * 70        # Sals Dobles que falta 
else:
     y = 0

if c < 250 and r > 200:
    z = r * 1.21
    u = z - c    # Clorur de Zenc que falta 
    u = u * 70
else:
     u = 0
     
if r < 200 and c > 250:
     v = 200 - r
     v = v *70      # Clorur de Amoni que falta 
else:
     v = 0

# Presentacio resultats
print()
print("Zn:", round(b, 1))
print("ZnCl2:", round (c, 1))
print("NH4Cl:", round(r, 1))
print("Relacio Molar:", round(s, 2))
print("Sals Totals:", round(t, 1))
print("\n Calculs Ingalsa \n")
print("ZnCl2 que falta:", round(u))
print("NH4Cl que falta:", round(v))
print("Sals Totals que falten:", round(y))