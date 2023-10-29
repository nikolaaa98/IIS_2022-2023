"""
                    Zadatak – Simplex metod (5 bodova)

Maksimizovati količinu smeše (u kg) poštujući sledeća ograničenja:

-	Minimalna kalorijska vrijednost smeše je 5 MJ/kg
-	Maksimalna kalorijska vrijednost smeše je 20 MJ/kg
-	Target kalorična vrednost smeše je 16 MJ/kg 
-	Maksimalni sadržaj vode – 50 wt.%;
-	Maksimalni sadržaj hlora – 30 000 mg/kg;
-	Maksimalni sadržaj sumpora – 20 000 mg/kg;
-	Maksimalni sadržaj fluora – 200 mg/kg; 
-	Maksimalni sadržaj žive – 10 mg/kg; 
-	Maksimalni sadžaj Cd + Tl – 25 mg/kg 
-	Maksimalni sadržaj teških metala – 2000 mg/kg  
-	Maksimalni sadržaj pepela nakon sagorevanja – 40 wt.%;
-	Rezultirajuća smeša odgovarajućeg protoka ne smije da ima termalnu energiju manju od 19,8 MW (maseni protok materijala x kalorična vrijednost smeše);  
-	Rezultirajuća smeša odgovarajućeg protoka ne smije da ima ima termalnu energiju veću od 32,2 MW (maseni protok materijala x kalorična vrijednost smeše).  


Dodatne informacije:
-	Raditi simulacije za 24h.
-	Formula za termalnu energiju je Thp(W) = m(masa, kg)/t(vrijeme, s) x CalV (kalorijska vrijednost/moć, J/kg).
Biblioteke:
-	Apache Commons Math
-	OR Tool
"""

import numpy as np
from scipy.optimize import linprog

time = 24 * 3600

# Koeficijenti ciljne funkcije (za maksimizaciju količine smeše)
c = [-1, -1] # Z = X1 + X2 

# Koeficijenti matrice (Ax <= b)
A = [
    [-1, 0],   # X1 >= 5  Minimalna kalorijska vrijednost smeše
    [1, 0],    # X1 <= 20 ->  Maksimalna kalorijska vrijednost smeše 
    [1, 0],    # X1 = 16 -> Target kalorična vrednost smeše 
    [0, 1],    # X2 <= 0.5 -> Maksimalni sadržaj vode
    [0, 1],    # X2 <= 0.3 -> Maksimalni sadržaj hlora 
    [0, 1],    # X2 <= 0.2 -> Maksimalni sadržaj sumpora 
    [0, 1],    # X2 <= 0.002 -> Maksimalni sadržaj fluora 
    [0, 1],    # X2 <= 0.0001 ->  Maksimalni sadržaj žive 
    [0, 1],    # X2 <= 0.00025 -> Maksimalni sadžaj Cd + Tl 
    [0, 1],    # X2 <= 0.02 -> Maksimalni ssadržaj teških metala 
    [1, 1],    # X1 + X2 <= 0.4 -> Maksimalni sadržaj pepela nakon sagorevanja 
    [0, -1/time], # 1/time * X2 * X1 >= 19.8 -> Rezultirajuća smeša odgovarajućeg protoka ne smije da ima termalnu energiju manju od 19,8 MW
    [0, 1/time]  # 1/time * X2 * X1 <= 32.2 -> Rezultirajuća smeša odgovarajućeg protoka ne smije da ima ima termalnu energiju veću od 32,2 MW
]

# Desna strana matrice
#b = [5, 20, 16, 0.5, 30000, 20000, 200, 10, 25, 2000, 0.4, 19.8, 32.2] 
b = [5, 20, 16, 0.5, 0.3, 0.2, 0.002, 0.0001, 0.00025, 0.02, 0.4, 19.8, 32.2] # vrednosti koje su bile u mg sam pretvorio u kg


x_bounds = [(0, None), (0, None)]

#result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='simplex', options={"disp": True})
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='simplex')

if result.success:
    print("Optimalno resenje:") 
    print(result)
    print(f"Maksimizovana kolčinu smeša = {abs(result.fun)*100000} mg/kg ({abs(result.fun)}) kg")
else:
    print("Neuspela optimizacija, proveri unete podatke !")