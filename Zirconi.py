A = float (input ("Absrovancia Zr: "))  # Recolecta de Dades

B = A - 0.296   # Abs corregida

if B > 0:
    C = ((B * 158.2) + 0.4) * 10  #Calcul
    print(f'{round(C)} ppm Zr')
else:
    print('No es pot fer el càlcul ja que Abs correcio > Abs Zr') #Gestio d'errors