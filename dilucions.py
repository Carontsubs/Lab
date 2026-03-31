#!/usr/bin/env python3
"""
Calculadora: quant afegir sobre un volum existent
perquè la solució final tingui el percentatge desitjat.

Tenint en compte TOTS els ingredients alhora:
X_i = pct_i / 100 * (V + sum(X_j)) per a cada i
=> resolució del sistema: V_final = V / (1 - sum(pct_i)/100)
=> X_i = pct_i/100 * V_final
"""

def calcular():
    print("\n=== Quant afegir sobre una solució ===\n")

    while True:
        try:
            volum = float(input("Volum inicial (ml): "))
            if volum > 0:
                break
            print("  Ha de ser positiu.")
        except ValueError:
            print("  Número no vàlid.")

    while True:
        try:
            n = int(input("Quants ingredients vols afegir? "))
            if n > 0:
                break
            print("  Ha de ser almenys 1.")
        except ValueError:
            print("  Introdueix un número enter.")

    print()
    ingredients = []
    total_pct = 0

    for i in range(n):
        nom = input(f"  Nom de l'ingredient {i+1}: ").strip() or f"Ingredient {i+1}"
        while True:
            try:
                pct = float(input(f"  Percentatge final de {nom} (%): "))
                if pct <= 0:
                    print("  Ha de ser positiu.")
                    continue
                if total_pct + pct >= 100:
                    print(f"  La suma dels percentatges ({total_pct + pct:.4g}%) no pot arribar al 100%.")
                    continue
                break
            except ValueError:
                print("  Número no vàlid.")
        ingredients.append((nom, pct))
        total_pct += pct

    # Càlcul: volum final i quantitat de cada ingredient
    # V_final = V_inicial / (1 - sum_pct/100)
    volum_final = volum / (1 - total_pct / 100)
    total_afegit = volum_final - volum

    print(f"\n{'─'*46}")
    print(f"  Volum inicial: {volum:.6g} ml")
    print(f"{'─'*46}")
    print(f"  {'Ingredient':<18} {'%':>6}   {'Afegir':>10}")
    print(f"{'─'*46}")
    for nom, pct in ingredients:
        x = pct / 100 * volum_final
        print(f"  {nom:<18} {pct:>6.2f}%   {x:>8.4g} ml")
    print(f"{'─'*46}")
    print(f"  Total afegit:          {total_afegit:>8.4g} ml")
    print(f"  Volum final:           {volum_final:>8.4g} ml")
    print(f"{'─'*46}\n")

    print("  Verificació:")
    for nom, pct in ingredients:
        x = pct / 100 * volum_final
        pct_real = x / volum_final * 100
        print(f"  {nom}: {x:.4g} ml / {volum_final:.4g} ml = {pct_real:.2f}%  ✓")
    print()


def main():
    while True:
        calcular()
        if input("Un altre càlcul? (s/n): ").strip().lower() not in ("s", "si", "sí", "y"):
            print("\nFins aviat!\n")
            break


if __name__ == "__main__":
    main()